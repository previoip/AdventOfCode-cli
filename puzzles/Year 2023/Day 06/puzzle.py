import typing as t
from io import IOBase
from src.aoc.base_class import AOCBaseClass, AOCRunAsEnum
from functools import partial, reduce
import math

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
    inp = map(lambda x: x.split(':'), inp)
    inp = map(lambda x: tuple(map(int, x[-1].split())), inp)
    return list(zip(*inp))

  def solution_part_1(self, parsed_input) -> t.Any:
    # f(x, t) = x * (t-x)
    # f(x, t) = -x**2 + x*t
    # d(f(x, t))/dx = -2x + t

    # f(x, t, x0) = -x**2 + x*t - x0
    # a=-1, b=t, c=-x0
    # -b=-t, sqrt(b^2-4ac)=sqrt(t^2 - (4*x0)), 2a=-2

    def quad_roots(a, b, c):
      sqrt_abc = math.sqrt(b**2 - (4*a*c))
      quadratic_roots = (-b - sqrt_abc)/(2*a), (-b + sqrt_abc)/(2*a)
      return min(quadratic_roots), max(quadratic_roots)

    fn_max_dist_construct = lambda t: lambda x: (-(x)**2 + (x)*t)

    res = []
    for allocated_time, rec_dist in parsed_input:
      fn = fn_max_dist_construct(allocated_time)
      roots_lw, roots_up = quad_roots(-1, allocated_time, rec_dist*-1)
      roots_lw, roots_up = round(roots_lw), round(roots_up)

      while True:
        if fn(roots_lw) <= rec_dist:
          roots_lw += 1
        else:
          break

      while True:
        if fn(roots_up) <= rec_dist:
          roots_up -= 1
        else:
          break
      res.append(roots_up - roots_lw + 1)

      # for i in range(allocated_time):
      #   print('[{}]'.format(i), fn(i), fn(i) > rec_dist)

    return reduce(lambda x, y: x*y, res)

  def parser_part_2(self, buf_io: IOBase) -> t.Any:
    inp = buf_io.read().decode(self.default_encoding).splitlines()
    inp = map(lambda x: x.split(':'), inp)
    inp = map(lambda x: int(x[-1].replace(' ', '')), inp)
  
    return [tuple(inp)]

  def solution_part_2(self, parsed_input) -> t.Any:
    return self.solution_part_1(parsed_input)
