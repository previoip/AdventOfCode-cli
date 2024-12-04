import typing as t
import struct
from collections import OrderedDict

def sizeof(c: "_AOCStateFrag"):
  return c.calcsize()

class _AOCStateFrag:
  
  def read(self, fo):
    self.unpack(fo.read(self.calcsize()))

  @classmethod
  def calcsize(cls):
    return struct.calcsize(cls.fmt)


class AOCMeta(_AOCStateFrag):
  fmt = '<4sII'

  def __init__(self):
    self.signature: bytes
    self.total_length: int
    self.num_year_entries: int 
    self.latest_year: int 

  def pack(self):
    return struct.pack(
      self.fmt,
      self.signature,
      self.num_year_entries,
      self.latest_year
    )

  def unpack(self, b):
    self.signature, \
    self.num_year_entries, \
    self.latest_year = struct.unpack(self.fmt, b)


class AOCYearEntry(_AOCStateFrag):
  fmt = '<ILL'

  def __init__(self):
    self.year: int
    self.offset: int
    self.length: int

  def pack(self):
    return struct.pack(
      self.fmt,
      self.year,
      self.offset,
      self.length
    )

  def unpack(self, b):
    self.year, \
    self.offset, \
    self.length = struct.unpack(self.fmt, b)


class AOCDayEntry(_AOCStateFrag):
  flag_failed = 0b01
  flag_passed = 0b10
  mask_p1 = 0b0011
  mask_p2 = 0b1100
  fmt = '<h'


  def __init__(self):
    self.part_1: int
    self.part_2: int
    self.reset_state()

  def reset_state(self):
    self.part_1 = 0
    self.part_2 = 0

  @classmethod
  def state_to_vals(cls, st):
    p1 = (st & cls.mask_p1)
    p2 = (st & cls.mask_p2)
    return int(p1), int(p2)

  @classmethod
  def vals_to_state(cls, vp1, vp2):
    st = 0
    st |= vp1
    st |= vp2
    return int(st)

  @classmethod
  def val_to_flag(cls, v):
    v &= 0b1111
    if not v >> 2 == 0:
      v = v >> 2
    return int(v)

  @classmethod
  def flag_repr(cls, fl):
    fl = cls.val_to_flag(fl)
    if fl & cls.flag_failed == cls.flag_failed:
      return 'x'
    elif fl & cls.flag_passed == cls.flag_passed:
      return '*'
    return ' '

  def set_state(self, v: int):
    self.part_1, self.part_2 = self.state_to_vals(v)

  def get_state(self):
    return self.vals_to_state(self.part_1, self.part_2)

  @classmethod
  def get_flag_value(cls, part: int, choice: str):
    if choice.lower().startswith('fail'):
      b = cls.flag_failed
    elif choice.lower().startswith('pass'):
      b = cls.flag_passed
    else:
      return 0
    if part == 2:
      b = b << 2
    return b

  def pack(self):
    return struct.pack(self.fmt, self.get_state())

  def unpack(self, b):
    self.set_state(struct.unpack(self.fmt, b)[0])


class AOCStateManager:
  signature = b'\x42\x00\x69\x69'
  num_days_in_session = 25

  def __init__(self, filepath):
    self.filepath = filepath
    self._meta: AOCMeta = AOCMeta()
    self._meta.signature = self.signature
    self._table: t.Mapping[int, list] = OrderedDict()

  @property
  def table(self):
    return self._table

  def init_table(self, year):
    if self._table.get(year) is None:
      self._table[year] = list(map(lambda _: 0, range(self.num_days_in_session)))

  def update(self, year, day, part, choice):
    assert isinstance(year, int)
    assert isinstance(day, int)
    assert isinstance(part, int)

    self.init_table(year)
    self._meta.latest_year = year
    day -= 1

    v = AOCDayEntry.get_flag_value(part, choice)
    v1, v2 = AOCDayEntry.state_to_vals(self._table[year][day])
    if part == 1:
      new_state = AOCDayEntry.vals_to_state(v, v2)
    elif part == 2:
      new_state = AOCDayEntry.vals_to_state(v1, v)
    self._table[year][day] = new_state

  def load(self):
    with open(self.filepath, 'rb') as fo:
      self._meta.read(fo)
      assert self._meta.signature == self.signature
      
      ls_c_years = list()

      for _ in range(self._meta.num_year_entries):
        c_year = AOCYearEntry()
        c_year.read(fo)
        ls_c_years.append(c_year)
      
      latest_cursor = fo.tell()

      for c_year in ls_c_years:
        fo.seek(latest_cursor + c_year.offset)
        self._table[c_year.year] = list()
        for _ in range(c_year.length):
          c_day = AOCDayEntry()
          c_day.read(fo)
          self._table[c_year.year].append(c_day.get_state())


  def save(self):
    buf = []
    
    ls_years = list(sorted(self._table.keys()))

    self._meta.latest_year = int(ls_years[0]) if ls_years else 0

    ls_c_years = list()
    ls_c_day = list()
    for year in ls_years:
      c_year = AOCYearEntry()
      c_year.year = int(year)
      c_year.length = len(self._table.get(year))
      c_year.offset = sizeof(AOCDayEntry) * len(ls_c_day)
      ls_c_years.append(c_year)

      for state in self._table.get(year):
        c_day = AOCDayEntry()
        c_day.set_state(state)
        ls_c_day.append(c_day)

    self._meta.num_year_entries = len(ls_c_years)

    buf.append(self._meta.pack())
    for c_year in ls_c_years:
      buf.append(c_year.pack())
    for c_day in ls_c_day:
      buf.append(c_day.pack())

    with open(self.filepath, 'wb') as fo:
      fo.writelines(buf)
  

  def to_repr_table(self, year):

    table = [[['  ', '', ''] for _ in range((self.num_days_in_session//7)+1)] for _ in range(7)]

    days = self._table.get(year)
    if days is None:
      return table

    for n in range(len(days)):
      i = n // 7
      j = n % 7

      table[j][i][0] = '{}.'.format(n+1).rjust(1)
      v1, v2 = AOCDayEntry.state_to_vals(days[n])
      v1, v2 = AOCDayEntry.val_to_flag(v1), AOCDayEntry.val_to_flag(v2)

      table[j][i][1] = AOCDayEntry.flag_repr(v1).ljust(2)
      table[j][i][2] = AOCDayEntry.flag_repr(v2).ljust(2)
    return table

  def stat_year_repr(self, year):
    days = self._table.get(year)
    if days is None:
      return ''

    table = self.to_repr_table(year)
    r = ''

    for m, i in enumerate(table):
      for n, j in enumerate(i):
        if n == 0:
          r += '|'
        r += ' '.join(j).rjust(10)
        r += '|'
      r += '\n'
    return r


  def stats_repr(self, year_select=0):
    r = ''
    for i, year in enumerate(self._table.keys()):
      if year_select and year != year_select:
        continue
      t = self.stat_year_repr(year)
      strlen = len(t.splitlines()[0])
      r += ': AoC {} :'.format(year).center((strlen), '=')
      r += '\n'
      r += t
      r += '=' * strlen
      r += '\n'
    r += '\n'
    return r

if __name__ == '__main__':
  import os
  a = AOCStateManager('tmpstate')
  a.update(2023, 1, 1, 'fail')
  a.update(2023, 1, 2, 'pass')

  a.update(2023, 2, 1, 'fail')
  a.update(2023, 2, 2, 'fail')
  
  a.update(2024, 3, 1, 'pass')
  a.update(2024, 3, 2, 'pass')

  a.update(2024, 4, 1, 'pass')
  a.update(2024, 4, 2, 'fail')

  a.save()

  b = AOCStateManager('tmpstate')
  b.load()
  os.remove('tmpstate')

  assert a.table == b.table

  print(b.stats_repr())
