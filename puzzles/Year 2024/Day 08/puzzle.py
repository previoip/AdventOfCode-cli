import typing as t
from io import IOBase
from src.aoc.base_class import AOCBaseClass, AOCRunAsEnum
from src.shared.containers import StringMatrixV2 as StringMatrix

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
    self.char_empty = '.'
    self.char_antinode = '#'
    self.world = StringMatrix('')
    self.frame = StringMatrix('')
    self.antennas = set()

  def process_test_answer(self, b: bytes) -> t.Any:
    return int(b)

  def get_occurrences(self, c):
    n = self.world.count_char(c)
    if n <= 1:
      return []
    indices = [None for _ in range(n)]
    offset = -1
    for i in range(n):
      offset = self.world.data.index(c, offset+1)
      indices[i] = self.world.index_to_coo(offset)
    return indices

  def parser(self, buf_io: IOBase) -> t.Any:
    self.antennas.clear()
    self.world.from_string(buf_io.read().decode(self.default_encoding).strip())
    self.frame.from_empty(self.world.width, self.world.height, self.char_empty)
    self.antennas.update(self.world.data)
    self.antennas.remove(self.char_empty)

  def solution_part_1(self, parsed_input) -> t.Any:
    import itertools
    for c in self.antennas:
      for (x0, y0), (x1, y1) in itertools.permutations(self.get_occurrences(c), r=2):
        dx, dy = x0-x1, y0-y1
        dx, dy = dx*2, dy*2
        ix, iy = x0-dx, y0-dy
        print((x0, y0), (x1, y1), (dx, dy), (ix, iy))
        if self.world.check_oob_from_coo(ix, iy):
          print('oob\'d')
          continue
        self.frame.set_char(ix, iy, self.char_antinode)
    print(self.world)
    print(self.frame)
    return self.frame.count_char(self.char_antinode)

  def solution_part_2(self, parsed_input) -> t.Any:
    import itertools
    for c in self.antennas:
      for (x0, y0), (x1, y1) in itertools.permutations(self.get_occurrences(c), r=2):
        self.frame.set_char(x0, y0, self.char_antinode)
        self.frame.set_char(x1, y1, self.char_antinode)
        dx, dy = x0-x1, y0-y1
        for i in range(2, 10_000_000):
          dxi, dyi = dx*i, dy*i
          ix, iy = x0-dxi, y0-dyi
          print(i, (x0, y0), (x1, y1), (dxi, dyi), (ix, iy))
          if self.world.check_oob_from_coo(ix, iy):
            print('done')
            break
          self.frame.set_char(ix, iy, self.char_antinode)
    print(self.world)
    print(self.frame)
    return self.frame.count_char(self.char_antinode)
