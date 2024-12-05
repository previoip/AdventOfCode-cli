import typing as t
from io import IOBase
from src.aoc.base_class import AOCBaseClass, AOCRunAsEnum
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

  class toks:
    sep = b','
    lparen = b'('
    rparen = b')'
    fndef_mul = b'mul'

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.eval_path_part_1 = 'input_p1.txt'
    self.eval_path_part_2 = 'input_p1.txt'
    self.test_path_part_1 = 'test_p1.txt'
    self.test_path_part_2 = 'test_p2.txt'
    self.regexp_mul = re.compile(br'^mul\((?P<a>\d+),(?P<b>\d+)\)')
    self.regexp_dos = re.compile(br'^(do|don\'t)\(\)')
    self.data = b''
    self.sums = 0

  def parser(self, buf_io: IOBase):
    self.data = buf_io.read()

  def process_test_answer(self, b: bytes) -> t.Any:
    return int(b.decode(self.default_encoding))

  def search_mul_expr(self):
    return self.regexp_mul.search(self.data)

  def search_dos_expr(self):
    return self.regexp_dos.search(self.data)

  def consume_mul(self):
    m = self.search_mul_expr()
    if not m:
      return False
    a, b = map(int, m.groups())
    self.sums += a*b
    return True

  def solution_part_1(self, parsed_input) -> t.Any:
    while self.data:
      if self.data.startswith(b'mul'):
        self.consume_mul()
      self.data = self.data[1:]
    return self.sums

  def solution_part_2(self, parsed_input) -> t.Any:
    flag = True
    while self.data:
      if self.data.startswith(b'do'):
        m = self.search_dos_expr()
        if m:
          if m.group().startswith(b'don'):
            flag = False
          else:
            flag = True
      if flag and self.data.startswith(b'mul'):
        self.consume_mul()
      self.data = self.data[1:]
    return self.sums
