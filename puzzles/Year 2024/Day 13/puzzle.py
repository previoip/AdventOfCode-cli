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
    self.t_xy = namedtuple('Coo', ['x', 'y'])
    self.t_set = namedtuple('Butts', ['button_a', 'button_b', 'prize'])

  def process_test_answer(self, b: bytes) -> t.Any:
    return int(b)

  def parser(self, buf_io: IOBase) -> t.Any:
    sets = [list()]
    for line in buf_io.read().decode(self.default_encoding).splitlines():
      line = line.strip()
      if not line:
        sets.append(list())
        continue
      sets[-1].append(line)
    for n in range(len(sets)):
      subset = sets[n]
      sets[n] = dict()
      for m in range(len(subset)):
        kw, va = subset[m].split(':')
        kw = kw.lower().replace(' ', '_')
        if kw == 'prize':
          va = va.replace('=', '')
        va = map(lambda i: i.lower(), va.strip().split(','))
        va = map(lambda i: i.strip(), va)
        va = map(lambda i: (i[0], int(i[1:])), va)
        sets[n][kw] = self.t_xy(**dict(va))
      sets[n] = self.t_set(**sets[n])
    return sets

  @staticmethod
  def iter_bivariant_roots(a, b, f):
    la = f // a + 1
    lb = f // b + 1
    ia = la
    ib = 0
    while ia>=0 and ib<lb:
      f_i = (ia * a) + (ib * b)
      if f_i == f:
        yield (ia, ib)
      if f_i >= f:
        ia -= 1
      if f_i < f:
        ib += 1

  @staticmethod
  def ls_a_in_b(a, b):
    for n in range(len(a)):
      if a[n] in b:
        yield n, b.index(a[n])

  @staticmethod
  def race(iter_1, iter_2):
    try:
      a1, b1 = next(iter_1)
      a2, b2 = next(iter_2)
      while True:
        a1, b1 = next(iter_1)
        a2, b2 = next(iter_2)
        yield (a1, b1)
    except IndexError:
      pass



  def solution_part_1(self, parsed_input) -> t.Any:
    tok_price_a = 3
    tok_price_b = 1
    scores = list()
    for n, butts in enumerate(parsed_input):
      print('>>>', n)
      valid_x = tuple(self.iter_bivariant_roots(butts.button_a.x, butts.button_b.x, butts.prize.x))
      valid_y = tuple(self.iter_bivariant_roots(butts.button_a.y, butts.button_b.y, butts.prize.y))
      for i, _ in self.ls_a_in_b(valid_x, valid_y):
        p_a, p_b = valid_x[i]
        print('   >>', p_a, p_b)
        scores.append(p_a*tok_price_a + p_b*tok_price_b)
    print(scores)
    return sum(scores)


  def solution_part_2(self, parsed_input) -> t.Any:
    tok_price_a = 3
    tok_price_b = 1
    scores = list()
    def offset_prize(n):
      # return int('1{:013d}'.format(n))
      return n 

    for n, butts in enumerate(parsed_input):
      print('>>>', n)
      iter_x = self.iter_bivariant_roots(butts.button_a.x, butts.button_b.x, offset_prize(butts.prize.x))
      iter_y = self.iter_bivariant_roots(butts.button_a.y, butts.button_b.y, offset_prize(butts.prize.y))
      try:
        while True:
          ax, bx = next(iter_x)
          ay, by = next(iter_y)
          print('??', ax, bx, '|', ay, by) 

          # while ax < ay:
          #   ax, bx = next(iter_x)

          if ax==ay and bx==by:
            print('match:', ax, bx)
      except StopIteration:
        pass
    return sum(scores)

