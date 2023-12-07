import typing as t
import struct
from collections import OrderedDict


class AOCStateFlag:
  p1_idle = 2 ** 0
  p1_fail = 2 ** 1
  p1_pass = 2 ** 2
  p2_idle = 2 ** 3
  p2_fail = 2 ** 4
  p2_pass = 2 ** 5

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
  fmt = '<h'
  def __init__(self):
    self.part_1_idle: bool
    self.part_1_fail: bool
    self.part_1_pass: bool
    self.part_2_idle: bool
    self.part_2_fail: bool
    self.part_2_pass: bool
    self.reset_state_flag()

  def reset_state_flag():
    self.part_1_idle = False
    self.part_1_fail = False
    self.part_1_pass = False
    self.part_2_idle = False
    self.part_2_fail = False
    self.part_2_pass = False
    
  def set_state_flag(self, v: int):
    self.part_1_idle = bool(v & AOCStateFlag.p1_idle)
    self.part_1_fail = bool(v & AOCStateFlag.p1_fail)
    self.part_1_pass = bool(v & AOCStateFlag.p1_pass)
    self.part_2_idle = bool(v & AOCStateFlag.p2_idle)
    self.part_2_fail = bool(v & AOCStateFlag.p2_fail)
    self.part_2_pass = bool(v & AOCStateFlag.p2_pass)

  def get_state_flag(self):
    res = 0
    res |= AOCStateFlag.p1_idle if self.part_1_idle else 0
    res |= AOCStateFlag.p1_fail if self.part_1_fail else 0
    res |= AOCStateFlag.p1_pass if self.part_1_pass else 0
    res |= AOCStateFlag.p2_idle if self.part_2_idle else 0
    res |= AOCStateFlag.p2_fail if self.part_2_fail else 0
    res |= AOCStateFlag.p2_pass if self.part_2_pass else 0
    return res

  def pack(self):
    return struct.pack(self.fmt, self.get_state_flag())

  def unpack(self, b):
    self.set_state_flag(struct.unpack(self.fmt, b)[0])


class AOCStateManager:
  signature = b'\x42\x00\x69\x69'

  def __init__(self, filepath):
    self.filepath = filepath
    self._meta: AOCMeta = AOCMeta()
    self._meta.signature = self.signature
    self._table: t.Mapping[int, list] = OrderedDict()

  def update(self, year, day, part, state):
    self._table[year][day] = state

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
          self._table[c_year.year].append(c_day.get_state_flag())


  def save(self):
    buf = []
    
    ls_years = list(sorted(self._table.keys()))

    self._meta.latest_year = ls_years[0] if ls_years else 0

    ls_c_years = list()
    ls_c_day = list()
    for year in ls_years:
      c_year = AOCYearEntry()
      c_year.year = year
      c_year.length = len(self._table.get(year))
      c_year.offset = sizeof(AOCDayEntry) * len(ls_c_day)
      ls_c_years.append(c_year)

      for day in self._table.get(year):
        c_day = AOCDayEntry()
        c_day.set_state_flag(day)
        ls_c_day.append(c_day)

    self._meta.num_year_entries = len(ls_c_years)

    buf.append(self._meta.pack())
    for c_year in ls_c_years:
      buf.append(c_year.pack())
    for c_day in ls_c_day:
      buf.append(c_day.pack())

    with open(self.filepath, 'wb') as fo:
      fo.writelines(buf)
  

if __name__ == '__main__':
  a = AOCStateManager('tmpstate')
  a._table[2023] = [1,2,3,4,5]
  a._table[2024] = [6,7,8,9,10]
  a.save()
  print(a._table)

  b = AOCStateManager('tmpstate')
  b.load()
  print(b._table)

  assert a._table == b._table