import typing as t
from io import IOBase
from src.aoc.base_class import AOCBaseClass, AOCRunAsEnum
from collections import namedtuple, Counter
from functools import cache

class CARD_ORD:
  card_index = ' AKQJT98765432'
  five_of_a_kind   = 7
  four_of_a_kind   = 6
  full_house       = 5
  three_of_a_kind  = 4
  two_pair         = 3
  one_pair         = 2
  high_card        = 1

  @staticmethod
  @cache
  def sort_string(s):
    return ''.join(sorted(s))

  @classmethod
  def get_ord(cls, s):
    s = cls.sort_string(s)
    s_counter = Counter(s)
    c = map(lambda x: s_counter[x], set(s))
    c = sorted(c, reverse=True)
    if c == [5]:
      return cls.five_of_a_kind
    elif c == [4, 1]:
      return cls.four_of_a_kind
    elif c == [3, 2]:
      return cls.full_house
    elif c[0] == 3:
      return cls.three_of_a_kind
    elif c == [2, 2, 1]:
      return cls.two_pair
    elif c == [2, 1, 1, 1]:
      return cls.one_pair
    elif c == [1, 1, 1, 1, 1]:
      return cls.high_card
    else:
      return 0

  @classmethod
  def get_char_score(cls, c):
    if c not in cls.card_index:
      return 0
    return len(cls.card_index) - cls.card_index.index(c)

  @classmethod
  def get_score_all(cls, s):
    r = 0
    for c in s:
      r += cls.get_char_score(c)
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
    self.eval_path_part_2 = 'input_p1.txt'
    self.test_path_part_1 = 'test_p1.txt'
    self.test_path_part_2 = 'test_p2.txt'

  def process_test_answer(self, b: bytes) -> t.Any:
    return int(b.decode(self.default_encoding))

  def parser(self, buf_io: IOBase) -> t.Any:
    nt = namedtuple('CardSet', field_names=['cards', 'bid'])
    inp = buf_io.read().decode(self.default_encoding).splitlines()
    inp = map(lambda x: x.split(), inp)
    inp = map(lambda x: (x[0], int(x[1])), inp)
    inp = map(lambda x: nt(*x), inp)
    return list(inp)

  def solution_part_1(self, parsed_input) -> t.Any:
    nt = namedtuple('CardTypeSet', field_names=['cards', 'bid', 'ord'])
    card_types = list(map(lambda x: nt(x.cards, x.bid, CARD_ORD.get_ord(x.cards)), parsed_input))

    for i in range(5):
      print(i)
      card_types = sorted(card_types, key=lambda x: CARD_ORD.get_char_score(x.cards[4-i]))
    card_types = sorted(card_types, key=lambda x: x.ord)
    card_types = list(card_types) 

    res = 0
    for i, c in enumerate(card_types):
      res += c.bid * (i+1)
      print(c.cards, c.bid, c.ord)

    return res

  def solution_part_2(self, parsed_input) -> t.Any:
    CARD_ORD.card_index = ' AKQT98765432J'
    nt = namedtuple('CardTypeSet', field_names=['cards', 'cards_repl', 'bid', 'ord'])

    card_types = []
    for card_set in parsed_input:
      if 'J' in card_set.cards:
        char_set = list(set(card_set.cards))
        char_ords = []
        for c in char_set:
          char_ords.append(CARD_ORD.get_ord(card_set.cards.replace('J', c)))
        cards_repl = card_set.cards.replace('J', char_set[char_ords.index(max(char_ords))])
        card_types.append(nt(card_set.cards, cards_repl, card_set.bid, CARD_ORD.get_ord(cards_repl)))
      else:
        card_types.append(nt(card_set.cards, card_set.cards, card_set.bid, CARD_ORD.get_ord(card_set.cards)))

  

    for i in range(5):
      print(i)
      card_types = sorted(card_types, key=lambda x: CARD_ORD.get_char_score(x.cards[4-i]))
    card_types = sorted(card_types, key=lambda x: x.ord)
    card_types = list(card_types) 

    res = 0
    for i, c in enumerate(card_types):
      res += c.bid * (i+1)
      print(c.cards, c.bid, c.ord)

    return res
