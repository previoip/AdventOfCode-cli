import typing as t
from io import IOBase
from src.aoc.base_class import AOCBaseClass, AOCRunAsEnum

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
    for line in buf_io.readlines():
      yield tuple(map(int, line.decode(self.default_encoding).strip().split()))

  @staticmethod
  def ckrow(row):
    d0 = None
    for i in range(1, len(row)):
      dt = row[i-1] - row[i]
      if i == 1:
        d0 = dt
      if dt*d0 < 0:
        return False
      elif abs(dt) < 1 or abs(dt) > 3:
        return False
    return True

  def solution_part_1(self, parsed_input) -> t.Any:
    c = 0
    for row in parsed_input:
      if self.ckrow(row):
        c += 1
    return c

  def solution_part_2(self, parsed_input) -> t.Any:
    c = 0
    for row in parsed_input:
      if self.ckrow(row):
        c += 1
      else:
        for i in range(len(row)):
          row_trunc = [j for n, j in enumerate(row) if n!=i]
          if self.ckrow(row_trunc):
            c += 1
            break
    return c
