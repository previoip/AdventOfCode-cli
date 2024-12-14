import typing as t
from io import IOBase
from src.aoc.base_class import AOCBaseClass, AOCRunAsEnum
from collections import namedtuple
from array import array, ArrayType
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
    self.test_path_part_1 = 'test_p1.txt'
    self.test_path_part_2 = 'test_p1.txt'
    self.t_robot = namedtuple('Roomba', ['index', 'pos', 'vel', 'n_repeat'])
    self.t_coord = namedtuple('XY', ['x', 'y'])
    self.regexp_parse_robot = re.compile(br'^p\=(?P<px>\-?\d+),(?P<py>\-?\d+)\s+v\=(?P<vx>\-?\d+),(?P<vy>\-?\d+)')
    self.room_width = 0
    self.room_height = 0
    self.timer = 0
    self.robots = list()
    self.robots_proxy = list()

  def process_test_answer(self, b: bytes) -> t.Any:
    return int(b)

  @staticmethod
  def n_until_wraps(n, l):
    c = 0
    n0 = n
    while n != 0:
      n += n0
      n %= l
      c += 1
    return c + 1

  def parser(self, buf_io: IOBase) -> t.Any:
    self.room_width, self.room_height = map(int, buf_io.readline().split())
    for i, line in enumerate(buf_io.readlines()):
      m = self.regexp_parse_robot.match(line).groups()
      px, py, vx, vy = map(int, m)
      nx = self.n_until_wraps(vx, self.room_width)
      ny = self.n_until_wraps(vy, self.room_height)
      robot = self.t_robot(
        i,
        self.t_coord(px, py),
        self.t_coord(vx, vy),
        self.t_coord(nx, ny)
        )
      self.robots.append(robot)
      self.robots_proxy.append(robot)

  def step(self, t):
    self.timer += t
    min_x = self.room_width
    min_y = self.room_height
    for i, robot in enumerate(self.robots):
      new_x = (robot.pos.x + robot.vel.x * t) % self.room_width
      new_y = (robot.pos.y + robot.vel.y * t) % self.room_height
      min_x = min(min_x, new_x)
      min_y = min(min_y, new_y)
      self.robots[i] = self.t_robot(
        robot.index, self.t_coord(new_x, new_y), robot.vel, robot.n_repeat
      )
    for i, robot in enumerate(self.robots):
      self.robots_proxy[i] = self.t_robot(
        robot.index, self.t_coord(robot.pos.x - min_x, robot.pos.y - min_y), robot.vel, robot.n_repeat
      )

  def reset(self):
    self.step(-self.timer)
    self.t = 0

  def solution_part_1(self, parsed_input) -> t.Any:
    qlx = self.room_width // 2
    qly = self.room_height // 2
    print('w:{} h:{} qx:{} qy:{}'.format(self.room_width, self.room_height, qlx, qly))
    quad = {i:0 for i in range(4)}
    self.step(100)
    for robot in self.robots:
      if robot.pos.x == qlx:
        continue
      if robot.pos.y == qly:
        continue
      qx = robot.pos.x // (qlx+1)
      qy = robot.pos.y // (qly+1)
      quad[qx+(qy*2)] += 1
    res = 1
    for v in quad.values():
      res *= v
    self.robots.clear()
    self.reset()
    return res

  @staticmethod
  def pascal_width_generator():
    n = 1
    while True:
      yield n
      n += 2

  @classmethod
  def christmas_tree_coo_generator(cls, n, offset):
    counter = 0
    width_generator = cls.pascal_width_generator()
    y = 0
    while counter < n:
      w = next(width_generator)
      w_halved = w // 2
      for i in range(w):
        counter += 1
        if counter > n:
          break
        x = offset - w_halved + i
        yield (x, y)
      y += 1

  def solution_part_2(self, parsed_input) -> t.Any:
    from src.shared.containers import StringMatrixV2
    from array import array
    import time
    string_matrix = StringMatrixV2('').from_empty(self.room_width, self.room_height, '.')
    robot_selected = list()
    robot_count = len(self.robots)
    inv_common_factor = 1
    for robot in self.robots:
      if not inv_common_factor % robot.n_repeat.x == 0:
        inv_common_factor *= robot.n_repeat.x
      if not inv_common_factor % robot.n_repeat.y == 0:
        inv_common_factor *= robot.n_repeat.y

    w = 0
    h = 0
    pascal_generator = self.pascal_width_generator()
    c = 0
    while c < robot_count:
      w = next(pascal_generator)
      c += w
      h += 1
    christmas_coos = list(self.christmas_tree_coo_generator(robot_count, w//2))

    dumbass_sample_indices = tuple(range(string_matrix.length))
    skip = 0
    self.step(skip)
    step_count = 0
    for step_count in range(skip+1, inv_common_factor+1):
      if step_count % 1000 == 0: print(step_count)
      self.step(1)
      for robot in self.robots_proxy: string_matrix.set_char(robot.pos.x, robot.pos.y, '#')

      found = False
      for i in dumbass_sample_indices:
        if string_matrix.data[i] == '.': continue
        congregated_count = len(string_matrix.flood_fill_indices(*string_matrix.index_to_coo(i)))
        if congregated_count > 25:
          print(string_matrix)
          print(step_count)
          print(congregated_count)
          found = True
          break
      if found: break
      for robot in self.robots_proxy: string_matrix.set_char(robot.pos.x, robot.pos.y, '.')

    for robot in self.robots:
      string_matrix.set_char(robot.pos.x, robot.pos.y, '#')
    print(string_matrix)
    self.robots.clear()
    self.robots_proxy.clear()
    self.reset()
    return step_count
