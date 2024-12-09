import typing as t
from io import IOBase
from src.aoc.base_class import AOCBaseClass, AOCRunAsEnum
from src.shared.containers import StringMatrixV2
from array import array

class GuardsChallenge:
  def __init__(self, string):
    self.world = StringMatrixV2(string)
    self.frame = StringMatrixV2('').from_empty(self.world.width, self.world.height)
    self.char_empty = '.'
    self.char_visited = 'X'
    self.char_obstacle = '#'
    self.guard_pos_x = 0
    self.guard_pos_y = 0
    self.guard_char = ''
    self.guard_heading = 0
    self.guard_moveset = {
      '^': (( 0,-1), 6),
      '>': (( 1, 0), 0),
      'v': (( 0, 1), 2),
      '<': ((-1, 0), 4),
    }
    self.guard_cycle = {
      '^': '>',
      '>': 'v',
      'v': '<',
      '<': '^',
    }
    self.buf_view_front = array('u', self.char_empty*max(self.world.width, self.world.height))
    self.step_log = list()
    self.step_cur = None

    for c in self.guard_cycle:
      if self.world.has_char(c):
        self.guard_char = c
        break
    self.guard_pos_x, self.guard_pos_y = self.world.index_to_coo(self.world.get_char_index(self.guard_char))
    _, self.guard_heading = self.guard_moveset.get(self.guard_char)
    self.scan_view()


  def clone(self):
    return self.__class__(str(self.world))

  def obstructed(self):
    return self.char_obstacle in self.buf_view_front and self.buf_view_front.index(self.char_obstacle) == 1

  def out_of_bound(self):
    return self.world.check_oob_from_coo(self.guard_pos_x, self.guard_pos_y)

  def looped(self):
    return self.step_cur in self.step_log[:-1]

  def scan_view(self):
    self.world.fetch_line(self.guard_pos_x, self.guard_pos_y, self.buf_view_front, self.guard_heading)

  def step(self):
    if self.obstructed():
      self.guard_char = self.guard_cycle.get(self.guard_char)
    (dx, dy), self.guard_heading = self.guard_moveset.get(self.guard_char)
    self.world.set_char(self.guard_pos_x, self.guard_pos_y, self.char_visited)
    self.guard_pos_x += dx
    self.guard_pos_y += dy
    self.world.set_char(self.guard_pos_x, self.guard_pos_y, self.guard_char)
    self.scan_view()
    self.step_cur = (self.world.coo_to_index(self.guard_pos_x, self.guard_pos_y), self.guard_heading)
    self.step_log.append(self.step_cur)



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
    self.game = None


  def process_test_answer(self, b: bytes) -> t.Any:
    return int(b.decode(self.default_encoding))

  def parser(self, buf_io: IOBase) -> t.Any:
    self.game = GuardsChallenge(buf_io.read().decode(self.default_encoding).strip())
    return None

  def solution_part_1(self, parsed_input) -> t.Any:
    while not self.game.out_of_bound():
      self.game.step()
      print(self.game.world)
    return self.game.world.count_char(self.game.char_visited)

  def solution_part_2(self, parsed_input) -> t.Any:
    buf_view_left = array('u', self.game.char_empty*max(self.game.world.width, self.game.world.height))
    loop_count = 0
    while not self.game.out_of_bound():
      self.game.step()
      self.game.world.fetch_line(self.game.guard_pos_x, self.game.guard_pos_y, buf_view_left, self.game.guard_heading + 2)
      if not self.game.obstructed() and self.game.char_obstacle in buf_view_left:
        test_game = self.game.clone()
        (dx, dy), _ = test_game.guard_moveset.get(test_game.guard_char)
        test_game.world.set_char(test_game.guard_pos_x+dx, test_game.guard_pos_y+dy, test_game.char_obstacle)
        test_game.scan_view()
        while not test_game.out_of_bound():
          test_game.step()
          if test_game.looped():
            loop_count += 1
            print('looped!', loop_count)
            for step_index, _ in test_game.step_log[test_game.step_log.index(test_game.step_cur):]:
              test_game.world.set_char(*test_game.world.index_to_coo(step_index), '+')
            print(test_game.world)
            self.game.frame.set_char(self.game.guard_pos_x+dx, self.game.guard_pos_y+dy, self.game.char_obstacle)
            break
    return self.game.frame.count_char(self.game.char_obstacle)
