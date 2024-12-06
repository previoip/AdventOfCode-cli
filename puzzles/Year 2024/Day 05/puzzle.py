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
    self.eval_path_part_2 = 'input_p2.txt'
    self.test_path_part_1 = 'test_p1.txt'
    self.test_path_part_2 = 'test_p2.txt'

  def process_test_answer(self, b: bytes) -> t.Any:
    return int(b.decode(self.default_encoding))

  def parser(self, buf_io: IOBase) -> t.Any:
    ordering_rules = list()
    update_sets = list()
    flag = False
    for line in buf_io.readlines():
      line = line.decode(self.default_encoding)
      if not line.strip():
        flag = True
        continue
      if not flag:
        ordering_rules.append(tuple(map(int, line.split('|'))))
      else:
        update_sets.append(tuple(map(int, line.split(','))))
    return ordering_rules, update_sets

  @staticmethod
  def pairs_to_tree(ls):
    d = dict()
    for a, b in ls:
      if not a in d:
        d[a] = list()
      d[a].append(b)
    return d

  @staticmethod
  def ck_left_in_right(left, right):
    for i in left:
      if i in right:
        return True
    return False

  def solution_part_1(self, parsed_input) -> t.Any:
    ordering_rules, update_sets = parsed_input
    empty = list()
    ruleset_afters = self.pairs_to_tree(ordering_rules)
    ruleset_priors = self.pairs_to_tree([(i[1], i[0]) for i in ordering_rules])
    sums = 0
    for p, update_set in enumerate(update_sets):
      print(update_set)
      for i, page in enumerate(update_set):
        print(page, ruleset_afters.get(page), ruleset_priors.get(page))
        rule_after = ruleset_afters.get(page, empty)
        rule_prior = ruleset_priors.get(page, empty)
        l = update_set[:i]
        r = update_set[i+1:]
    return sums

  def solution_part_2(self, parsed_input) -> t.Any:
    raise NotImplementedError('puzzle part 2 is not yet implemented')
    return parsed_input
