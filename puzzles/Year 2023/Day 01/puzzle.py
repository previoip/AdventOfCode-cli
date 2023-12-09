import typing as t
from io import IOBase
from src.aoc_base_class import AOCBaseClass, AOCRunAsEnum
import re


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
    self.regexp_non_digit = re.compile(r'[^\d]*')
    self.digit_lit_map = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
    self.digit_lit_map_reversed = list(reversed(list(map(lambda x: ''.join(reversed(x)), self.digit_lit_map))))

    self.regexp_lit_digit = re.compile(r'([0-9]|{})'.format('|'.join(self.digit_lit_map)))
    self.regexp_lit_digit_reversed = re.compile(r'([0-9]|{})'.format('|'.join(self.digit_lit_map_reversed)))

  def parser(self, buf_io: IOBase) -> t.Any:
    return buf_io.read().decode(self.default_encoding)
     
  def process_test_answer(self, b: bytes) -> t.Any:
    return int(b.decode(self.default_encoding))

  def solution_part_1(self, parsed_input) -> t.Any:
    inp = parsed_input.splitlines()
    o = map(lambda i: self.regexp_non_digit.sub('', i), inp)
    o = map(lambda i: int(i[0] + i[-1]), o)
    x = sum(o)
    return x

  def solution_part_2(self, parsed_input) -> t.Any:
    inp = parsed_input.splitlines()
    o1 = map(lambda x: self.regexp_lit_digit.findall(x.lower())[0], inp)
    o1 = map(lambda x: str(self.digit_lit_map.index(x)) if x in self.digit_lit_map else x, o1)
    o1 = list(o1)
    o2 = map(lambda x: self.regexp_lit_digit_reversed.findall(''.join(reversed(x)).lower())[0], inp)
    o2 = map(lambda x: str(9 - self.digit_lit_map_reversed.index(x)) if x in self.digit_lit_map_reversed else x, o2)
    o2 = map(lambda x: ''.join(reversed(x)), o2)
    o2 = list(o2)
    o = map(lambda x: int(x[0] + x[-1]), zip(o1, o2))
    o = sum(o)

    return o