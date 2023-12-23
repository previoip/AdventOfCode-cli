import typing as t
from io import IOBase
from src.aoc.base_class import AOCBaseClass, AOCRunAsEnum

class Series:
  def __init__(self, ls, _ancestor=None, _descend=None):
    self.ls = ls
    self.ancestor = _ancestor
    self.descend = _descend

  def reduce_diff(self):
    new_ls = [self.ls[i+1] - self.ls[i] for i in range(len(self.ls) - 1)]
    obj = self.__class__(new_ls, _ancestor=self)
    self.descend = obj
    return obj

  def eval(self, fn):
    return map(fn, self.ls)

  def iter_descendants(self):
    inst = self
    while not inst is None:
      yield inst
      inst = inst.descend

  def iter_ancestors(self):
    inst = self
    while not inst is None:
      yield inst
      inst = inst.ancestor

  def __repr__(self):
    return '[ {} ]'.format(', '.join(map(str, self.ls)))


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
    inp = buf_io.read().decode(self.default_encoding).splitlines()
    inp = map(lambda x: [int(i) for i in x.split()], inp)
    return list(inp)

  def solution_part_1(self, parsed_input) -> t.Any:
    res = 0
    for series_set in parsed_input:
      series = Series(series_set)
      root_series = series
      leaf_series = series
      while not all(series.eval(lambda x: x==0)):
        series = series.reduce_diff()
        leaf_series = series
      leaf_series.ls.append(0)

      for series in leaf_series.iter_ancestors():
        if series.ancestor is None:
          continue
        series.ancestor.ls.append(series.ancestor.ls[-1] + series.ls[-1])

      for series in root_series.iter_descendants():
        print(series)
      print()

      res += root_series.ls[-1]

    return res

  def solution_part_2(self, parsed_input) -> t.Any:
    return self.solution_part_1([list(reversed(i)) for i in parsed_input])