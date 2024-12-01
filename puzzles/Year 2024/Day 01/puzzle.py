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
    s = buf_io.read().decode(self.default_encoding)
    left, right = zip(*[map(int, i.split()) for i in s.splitlines()])
    return left, right

  def solution_part_1(self, parsed_input) -> t.Any:
    from itertools import starmap
    left, right = parsed_input
    left, right = sorted(left), sorted(right)
    sub = lambda x, y: abs(x-y)
    res = starmap(sub, zip(left, right))
    return sum(res)

  def solution_part_2(self, parsed_input) -> t.Any:
    import numpy as np
    left, right = parsed_input
    right = np.array(right)
    sums = 0
    for i in left:
      c = (right==i).astype(int).sum()
      sums += i * c
    return sums
