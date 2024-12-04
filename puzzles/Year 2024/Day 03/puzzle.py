import typing as t
from io import IOBase
from src.aoc.base_class import AOCBaseClass, AOCRunAsEnum
from collections import deque
from array import array

class BytesBuffer:
  def __init__(self, maxlen):
    self.maxlen = maxlen
    self.buf = b''

  def append(self, b):
    self.buf += b
    l = len(self.buf)
    if l > self.maxlen:
      d = l - self.maxlen
      self.buf = self.buf[d:]

  def len(self):
    return len(self.buf)

  def endswith(self, b):
    return self.buf.endswith(b)

  def fetch(self, l):
    r = self.buf[-l:]
    self.buf = self.buf[:-l]
    return r

  def fetchleft(self, l):
    r = self.buf[:l]
    self.buf = self.buf[l:]
    return r


  def clear(self):
    self.buf = b''

  def isnumeric(self):
    return self.buf.isdigit()

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
    self.eval_path_part_2 = 'input_p2.txt'
    self.test_path_part_1 = 'test_p1.txt'
    self.test_path_part_2 = 'test_p2.txt'
    self.stack = deque(maxlen=1024)
    self.instr = list()
    self.stream = None
    self.eof = False
    self.buf = BytesBuffer(256)
    self.c = 0

  def read(self):
    b = self.stream.read(1)
    if not b:
      self.eof = True
      return False
    self.buf.append(b)
    return True

  def process_test_answer(self, b: bytes) -> t.Any:
    return int(b.decode(self.default_encoding))

  def parser(self, buf_io: IOBase) -> t.Any:
    self.stream = buf_io

  def ckstack(self, b):
    t = self.stack.pop()
    r = t == b
    return r

  def ckstack_last_fndef(self):
    if len(self.stack) == 0:
      return False
    r = False
    t = self.stack.pop()
    r |= t == self.toks.fndef_mul
    self.stack.append(t)
    return r

  def ckarg_numeric(self):
    self.buf.clear()
    self.read()
    while self.buf.isnumeric():
      self.read()
    if self.buf.len() > 0:
      c = self.buf.len()-1
      b = self.buf.fetchleft(c)
      print(b)
      self.stack.append(int(b))
      return True
    return False

  def cktok(self):
    if self.buf.endswith(self.toks.fndef_mul):
      if self.ckstack_last_fndef():
        self.stack.pop()
      self.stack.append(self.toks.fndef_mul)
    elif self.ckstack_last_fndef():
      if self.buf.endswith(self.toks.lparen):
        ok = self.ckarg_numeric()
        if ok and self.buf.endswith(self.toks.sep):
          ok = self.ckarg_numeric()
          if not ok:
            self.stack.pop()
        if not self.buf.endswith(self.toks.rparen):
          self.buf.clear()
          self.stack.pop()
          self.stack.pop()
          self.stack.pop()
      elif self.ckstack_last_fndef():
        self.stack.pop()

  def compute(self):
    reg_a = self.stack.pop()
    reg_b = self.stack.pop()
    instr = self.stack.pop()
    print(reg_a, reg_b, instr)

  def solution_part_1(self, parsed_input) -> t.Any:
    while self.read():
      self.cktok()
    self.cktok()
    instr = None
    reg = deque(maxlen=2)
    sums = 0
    while len(self.stack) > 0:
      self.compute()

    return sums

  def solution_part_2(self, parsed_input) -> t.Any:
    raise NotImplementedError('puzzle part 2 is not yet implemented')
    return parsed_input
