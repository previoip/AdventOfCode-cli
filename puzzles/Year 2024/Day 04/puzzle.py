import typing as t
from io import IOBase
from src.aoc.base_class import AOCBaseClass, AOCRunAsEnum
from array import array
from math import copysign

class StringMatrix:
  empty = ' '

  def __init__(self, string: str, strict=False):
    self.data = None
    self.strict = strict
    self.width = 0
    self.height = 0
    self.length = 0
    if string:
      self.from_string(string)
    else:
      self.data = array('u', '')


  def from_string(self, string):
    string = string.strip()
    self.data = array('u', string.replace('\n', '').replace('\r', ''))
    rows = string.splitlines()
    self.width = len(rows[0])
    self.height  = len(rows)
    self.length = self.width * self.height
    for row in rows:
      assert self.width == len(row)
    return self

  def from_empty(self, w, h, c=' '):
    if not c:
      c = self.empty
    self.width = w
    self.height = h
    self.length = self.width * self.height
    self.data = array('u', c*self.length)
    return self

  def index_to_coo(self, n):
    return n % self.width, n // self.width
  
  def coo_to_index(self, x, y):
    return x + self.width * y

  def check_oob_from_coo(self, x, y):
    n = self.coo_to_index(x, y)
    return self.check_oob_from_index(n)

  def check_oob_from_index(self, n):
    return n < 0 or n >= self.length

  def get_cell_from_index(self, n):
    if self.check_oob_from_index(n):
      if self.strict:
        raise IndexError()
      return self.empty
    return self.data[n]

  def get_cell_from_coo(self, x, y):
    if self.check_oob_from_coo(x, y):
      if self.strict:
        raise IndexError()
      return self.empty
    return self.data[self.coo_to_index(x, y)]

  def get_col(self, n):
    if n >= self.height:
      if self.strict:
        raise IndexError()
      return array('u', self.empty*self.height)
    return self.data[n::self.width]

  def get_row(self, n):
    if n >= self.width:
      if self.strict:
        raise IndexError()
      return array('u', self.empty*self.width)
    return self.data[self.width*n:self.width*(n+1)]

  def get_line(self, x, y, n, octant=0):
    octant %= 8
    ind = array('i', range(n))
    buf = array('u', ' '*n)
    s = copysign(1, 4-octant) if octant % 4 != 0 else 0
    octant += 2
    octant %= 8
    c = copysign(1, 4-octant) if octant % 4 != 0 else 0
    for i in range(n):
      ix, iy = x+int(i*c), y+int(i*s)
      ind[i] = self.coo_to_index(ix, iy)
      buf[i] = self.get_cell_from_coo(ix, iy)
    return ind, buf

  def get_diag(self, x, y, n, quadrant=0):
    quadrant %= 4
    ind = array('i', range(n))
    buf = array('u', ' '*n)
    for i in range(n):
      if False: pass
      elif quadrant == 0: # q1
        ix, iy = x+i, y-i
      elif quadrant == 1: # q2
        ix, iy = x-i, y-i
      elif quadrant == 2: # q3
        ix, iy = x-i, y+i
      elif quadrant == 3: # q4
        ix, iy = x+i, y+i
      ind[i] = self.coo_to_index(ix, iy)
      buf[i] = self.get_cell_from_coo(ix, iy)
    return ind, buf

  def set_char(self, x, y, c):
    if self.check_oob_from_coo(x, y):
      return
    n = self.coo_to_index(x, y)
    self.set_char_from_index(n, c)

  def set_char_from_index(self, n, c):
    self.data[n] = c

  def iter_cell(self):
    for n, c in enumerate(self.data):
      yield n, c

  def iter_row(self):
    for n in range(self.height):
      yield n, self.get_row(n)

  def iter_col(self):
    for n in range(self.width):
      yield n, self.get_col(n)

  def __repr__(self):
    r = ''
    for _, arr in self.iter_row():
      r += arr.tounicode()
      r += '\n'
    return r


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
    self.eval_path_part_2 = 'input_p2.txt'
    self.test_path_part_1 = 'test_p1.txt'
    self.test_path_part_2 = 'test_p2.txt'
    self.xmas_set = 'XMAS'
    self.frame_char_null = ' '
    self.frame_char_searched = '.'
    self.frame_arr_searched = array('u', self.frame_char_searched*4)

  def process_test_answer(self, b: bytes) -> t.Any:
    return int(b.decode(self.default_encoding))

  def parser(self, buf_io: IOBase) -> t.Any:
    return buf_io.read().decode(self.default_encoding)

  def playground(self):
    test_string = ''
    n = 33
    for i in range(9):
      for j in range(9):
        test_string += chr(n)
        n += 1
      test_string += '\n'
    test_matrix = StringMatrix(test_string)
    print(test_matrix)
    for i in range(8):
      print(test_matrix.get_line(4,4,4,i))

  def solution_part_1(self, parsed_input) -> t.Any:
    # self.playground()
    count = 0
    string_matrix = StringMatrix(parsed_input)
    print(string_matrix)
    frame_matrix = StringMatrix('').from_empty(string_matrix.width, string_matrix.height, self.frame_char_null)
    for n, cel in string_matrix.iter_cell():
      x, y = string_matrix.index_to_coo(n)
      for i in range(8):
        indices, line = string_matrix.get_line(x,y,4,i)
        if line.tounicode() == self.xmas_set:
          # print(line, indices)
          # indices, frame = frame_matrix.get_line(x,y,4,i)
          # if frame == self.frame_arr_searched:
          #   for j in indices:
          #     frame_matrix.set_char_from_index(j, '#')
          # else:
          #   for j in indices:
          #     frame_matrix.set_char_from_index(j, self.frame_char_searched)
          count += 1
    # print(frame_matrix)
    return count

  def solution_part_2(self, parsed_input) -> t.Any:
    return parsed_input
