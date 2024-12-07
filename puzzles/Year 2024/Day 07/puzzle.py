import typing as t
from io import IOBase
from src.aoc.base_class import AOCBaseClass, AOCRunAsEnum
from itertools import product

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

  _log10_divisor = tuple((10**i for i in range(32)))

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.eval_path_part_1 = 'input_p1.txt'
    self.eval_path_part_2 = 'input_p1.txt'
    self.test_path_part_1 = 'test_p1.txt'
    self.test_path_part_2 = 'test_p2.txt'

  def process_test_answer(self, b: bytes) -> t.Any:
    return int(b.decode(self.default_encoding))

  def parser(self, buf_io: IOBase) -> t.Any:
    for b in buf_io.readlines():
      s = b.decode(self.default_encoding).strip()
      r, sets = s.split(':')
      r = int(r)
      sets = tuple(map(int, sets.split()))
      yield r, sets

  @classmethod
  def _fastlog10(cls, n):
    for i in range(32):
      if n - cls._log10_divisor[i] < 0:
        return i
    return 0

  @classmethod
  def concat_nums(cls, l, r):
    l *= 10 ** cls._fastlog10(r)
    return l + r

  def solution_part_1(self, parsed_input) -> t.Any:
    sums = 0
    for r, sets in parsed_input:
      perm = product('+*', repeat=len(sets))
      for p in perm:
        temp = 0
        for n, o in enumerate(p):
          if o == '+':
            temp += sets[n]
          elif o == '*':
            temp *= sets[n]
        if temp == r:
          sums += r
          break
    return sums

  def solution_part_2(self, parsed_input) -> t.Any:
    sums = 0
    for r, sets in parsed_input:
      perm = product('+*&', repeat=len(sets))
      for p in perm:
        temp = 0
        for n, o in enumerate(p):
          if o == '+':
            temp += sets[n]
          elif o == '*':
            temp *= sets[n]
          elif o == '&':
            temp = self.concat_nums(temp, sets[n])
        if temp == r:
          sums += r
          break
    return sums