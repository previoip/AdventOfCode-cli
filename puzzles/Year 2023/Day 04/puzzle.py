import typing as t
from io import IOBase
from src.aoc.base_class import AOCBaseClass, AOCRunAsEnum
from collections import namedtuple

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
    struct_card_set = namedtuple('CardSet', field_names=['card', 'win_set', 'cur_set'])
    ret = list()
    inp = buf_io.read().decode(self.default_encoding)
    for line in inp.splitlines():
      card, sets = line[5:].split(':')
      set_win, set_cur = sets.split('|')
      set_win = list(map(int, set_win.split()))
      set_cur = list(map(int, set_cur.split()))
      ret.append(struct_card_set(int(card), set_win, set_cur))
    return list(sorted(ret, key=lambda x: x.card))


  def solution_part_1(self, parsed_input) -> t.Any:
    temp = list()
    for card_set in parsed_input:
      res = 1
      card, win_set, cur_set = card_set
      for win_num in win_set:
        if win_num in cur_set:
          res <<= 1
      res >>= 1
      temp.append(res)
    print(temp)
    return sum(temp)

  def solution_part_2(self, parsed_input) -> t.Any:
    _cache_fn_n_matches = dict()
    def n_matches(cards, n):
      if not _cache_fn_n_matches.get(n) is None:
        return _cache_fn_n_matches.get(n)
      else:
        _cache_fn_n_matches[n] = 0
      card, win_set, cur_set = cards[n]
      for win_num in win_set:
        if win_num in cur_set:
          _cache_fn_n_matches[n] += 1
      return _cache_fn_n_matches[n]

    res = {i.card:1 for i in parsed_input}

    def rec(res, n, card_set):
      match_c = n_matches(parsed_input, card_set.card - 1)
      if match_c > 0:
        for i in range(match_c):
          next_card_set = parsed_input[min(card_set.card + i, len(parsed_input))]
          res[n] += 1
          rec(res, n, next_card_set)

    for n, card_set in enumerate(reversed(parsed_input)):
      rec(res, n, card_set)

    return sum(res.values())
