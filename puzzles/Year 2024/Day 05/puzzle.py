import typing as t
from io import IOBase
from src.aoc.base_class import AOCBaseClass, AOCRunAsEnum
from itertools import permutations

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
    self.ordering_ruleset_afters = None
    self.ordering_ruleset_priors = None

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

    self.ordering_ruleset_afters = self.pairs_to_tree(ordering_rules)
    self.ordering_ruleset_priors = self.pairs_to_tree([(i[1], i[0]) for i in ordering_rules])

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
    for n, i in enumerate(left):
      if i in right:
        return (n, right.index(i)), True
    return (None, None), False

  def validate_pages(self, page_set):
    empty = list()
    for i, page in enumerate(page_set):
      l_set = page_set[:i]
      r_set = page_set[i+1:]

      rule_after = self.ordering_ruleset_afters.get(page, empty)
      rule_prior = self.ordering_ruleset_priors.get(page, empty)
      (r_index, rule_index), test = self.ck_left_in_right(r_set, rule_prior)
      if test:
        return False, ('prior', r_index+i, rule_index, rule_after, rule_prior)
      (l_index, rule_index), test = self.ck_left_in_right(l_set, rule_after)
      if test:
        return False, ('after', l_index, rule_index, rule_after, rule_prior)
    return True, (None, None, None, None)

  def solution_part_1(self, parsed_input) -> t.Any:
    _, update_sets = parsed_input
    sums = 0
    for p, page_set in enumerate(update_sets):
      print(page_set)
      test, _ = self.validate_pages(page_set)
      if test:
        sums += page_set[len(page_set) // 2]
    return sums

  def solution_part_2(self, parsed_input) -> t.Any:
    _, update_sets = parsed_input
    sums = 0
    for p, page_set in enumerate(update_sets):
      page_set = list(page_set)
      page_length = len(page_set)
      print()
      print(page_set)
      test, info = self.validate_pages(page_set)
      if not test:
        for _ in range(10_000):
          test, info = self.validate_pages(page_set)
          if test: break
          which, page_index, rule_index, _, _ = info
          page_invalid = page_set[page_index]
          if which == 'prior':
            rule = self.ordering_ruleset_priors[page_invalid]
            for i in range(page_index+1, page_length):
              if page_set[i] in rule:
                page_set[page_index] = page_set[i]
                page_set[i] = page_invalid
                break
            else:
              print('waoawafgahffaaghhgao')
          else:
            print('!!!!!!!!!!!!!!!!!!')
          print('<<', page_set)
        sums += page_set[len(page_set) // 2]
    return sums

    return parsed_input
