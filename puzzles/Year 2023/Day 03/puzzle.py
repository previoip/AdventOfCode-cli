import typing as t
from io import IOBase
from src.aoc_base_class import AOCBaseClass, AOCRunAsEnum

def is_symbol(char):
  return char != '.' and not char.isnumeric()


class StringMatrix:
  empty = ' '

  def __init__(self, str_):
    spl = str_.splitlines()
    self.width = len(spl[0])
    self.height = len(spl)
    self.length = self.width * self.height
    self._buf = str_.replace('\r\n', '').replace('\n', '').replace('\r', '')
    if len(self._buf) < self.length:
      self._buf += self.empty * (self.length - len(self._buf))

  def coord_to_index(self, x, y):
    return x + (y * self.width)

  def index_to_coord(self, i):
    return i % self.width, i // self.width

  def check_oob(self, x, y):
    i = self.coord_to_index(x, y)
    return i >= self.length or i < 0

  def set_char(self, x, y, char):
    if self.check_oob(x, y):
      return
    i = self.coord_to_index(x, y)
    self._buf = self._buf[:i] + char + self._buf[i+1:]

  def query_cel(self, x, y):
    if self.check_oob(x, y):
      return self.empty
    return self._buf[self.coord_to_index(x, y)]

  def query_row(self, y):
    l = self.width * y
    return self._buf[l : l + self.width]

  def query_col(self, x):
    return self._buf[x : : self.width]

  def query_kernel(self, x, y, w, h, nl='\n'):
    r = ''
    mx = (w // 2)
    my = (h // 2)
    for dy in range(h):
      dy = dy + y - my
      for dx in range(w):
        dx = dx + x - mx
        r += self.query_cel(dx, dy)
      r += nl
    return r

  def __repr__(self):
    return self.to_str(nl='\n')

  def to_str(self, nl=''):
    r = ''
    for i in range(self.height):
      r += self.query_row(i)
      r += nl
    return r

  def iter_cells(self):
    for n, char in enumerate(self._buf):
      yield char, self.index_to_coord(n)


def flood_fill(mat: "StringMatrix", char_target, char_fill):
  done = False
  c = 0
  while c < 1000_000:
    done = True
    for char, (x, y) in mat.iter_cells():
      if char == char_fill:
        kern = StringMatrix(mat.query_kernel(x, y, 3, 3))
        kerns = list(kern.iter_cells())[1::2]
        kerns = filter(lambda t: t[0] != mat.empty and t[0] == char_target, kerns)
        kerns = list(kerns)
        if len(kerns) > 0:
          done = False
        for _, (kx, ky) in kerns:
          mat.set_char(x+kx-1, y+ky-1, char_fill)
    if done:
      return
    c += 1
class AOC(AOCBaseClass):

  # overridable methods:
  #   def loader(self, part=1, run_as: AOCRunAsEnum=AOCRunAsEnum.test, *args, **kwargs) -> IOBase:
  #   def parser_part_1(self, buf_io: IOBase) -> t.Any:
  #   def parser_part_2(self, buf_io: IOBase) -> t.Any:
  #   def process_test_answer(self, b: bytes) -> t.Any:
  #
  # overridable attrs:
  #   self.eval_path_part_1 = 'input_p1.txt'
  #   self.eval_path_part_2 = 'input_p2.txt'
  #   self.test_path_part_1 = 'test_p1.txt'
  #   self.test_path_part_2 = 'test_p2.txt'

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.eval_path_part_1 = 'input_p1.txt'
    self.eval_path_part_2 = 'input_p1.txt'
    self.test_path_part_1 = 'test_p1.txt'
    self.test_path_part_2 = 'test_p2.txt'

  def process_test_answer(self, b: bytes) -> t.Any:
    return int(b.decode(self.default_encoding))

  def parser(self, buf_io: IOBase) -> t.Any:
    inp = buf_io.read().decode(self.default_encoding)

    # inp = ''
    # chars = [chr(i) for i in range(ord('1'), ord('z')+1)]
    # for i in range(8):
    #   inp += ''.join(chars[i*8:(i*8)+8])
    #   inp += '\n'
    # print()
    # print(inp)
    # print()
    
    mat = StringMatrix(inp)
    return mat

  def solution_part_1(self, parsed_input) -> t.Any:
    mat = parsed_input
    mask = StringMatrix(str(mat))
    symbols = list()

    for char, (x, y) in mat.iter_cells():
      mask.set_char(x, y, '#' if char.isnumeric() else ' ')
      if is_symbol(char):
        symbols.append((char, (x, y)))

    for char, (x, y) in symbols:
      kern = StringMatrix(mat.query_kernel(x, y, 3, 3))
      for kern_char, (kx, ky) in kern.iter_cells():
        if kern_char.isnumeric():
          mask.set_char(kx+x-1, ky+y-1, '%')

    flood_fill(mask, '#', '%')

    res = StringMatrix(str(mat))
    for char, (x, y) in mask.iter_cells():
      if char != '%':
        res.set_char(x, y, res.empty)

    res = res.to_str().split()
    res = map(int, res)
    return sum(res)

  def solution_part_2(self, parsed_input) -> t.Any:
    mat = parsed_input
    mask = StringMatrix(str(mat))
    gears = list()

    for char, (x, y) in mat.iter_cells():
      mask.set_char(x, y, '#' if char.isnumeric() else ' ')
      if char == '*':
        gears.append((char, (x, y)))

    valid_gears = list()
    for char, (x, y) in gears:
      kern = StringMatrix(mat.query_kernel(x, y, 3, 3))
      kern_nums = list()
      for row in map(kern.query_row, range(3)):
        row = map(int, row.replace('.', ' ').replace('*', ' ').split())
        row = list(row)
        kern_nums.extend(row)
      if len(kern_nums) > 1:
        for c, (kx, ky) in kern.iter_cells():
          if c.isnumeric():
            mask.set_char(x+kx-1, y+ky-1, '%')
        mask.set_char(x, y, '*')
        valid_gears.append((x, y))

    flood_fill(mask, '#', '%')

    res = StringMatrix(str(mat))
    for char, (x, y) in mask.iter_cells():
      if char != '%' and char != '*':
        res.set_char(x, y, res.empty)

    ret = 0

    for x, y in valid_gears:
      kern = StringMatrix(res.query_kernel(x, y, 3, 3))
      adj_part_nums = list()
      for char, (kx, ky) in kern.iter_cells():
        if char.isnumeric():
          dx, dy = x+kx-1, y+ky-1
          start, stop = 0, 0
          temp = char

          while temp.isnumeric():
            dx -= 1
            temp = res.query_cel(dx, dy)
          dx += 1
          start_index = res.coord_to_index(dx, dy)

          temp = char
          while temp.isnumeric():
            dx += 1
            temp = res.query_cel(dx, dy)
          stop_index = res.coord_to_index(dx, dy)

          has_index = False
          for t_start, t_stop in adj_part_nums:
            if t_start == start_index and t_stop == stop_index:
              has_index = True

          if has_index:
            continue

          adj_part_nums.append((start_index, stop_index))
      i = 1
      for start, stop in adj_part_nums:
        part_no = res._buf[start:stop]
        i *= int(part_no)
      ret += i

    return ret


