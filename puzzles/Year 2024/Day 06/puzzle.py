import typing as t
from io import IOBase
from src.aoc.base_class import AOCBaseClass, AOCRunAsEnum
from src.shared.containers import StringMatrixV2
from array import array

class GuardsChallenge:
  def __init__(self, string):
    self.world = StringMatrixV2(string)
    self.frame = StringMatrixV2('').from_empty(self.world.width, self.world.height, '.')
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
    self.step_cur = None

    for c in self.guard_cycle:
      if self.world.has_char(c):
        self.guard_char = c
        break
    self.guard_pos_x, self.guard_pos_y = self.world.index_to_coo(self.world.get_char_index(self.guard_char))
    _, self.guard_heading = self.guard_moveset.get(self.guard_char)
    self.scan_view()


  def clone(self):
    i = self.__class__(str(self.world))
    return i

  def obstructed(self):
    return self.char_obstacle in self.buf_view_front and self.buf_view_front.index(self.char_obstacle) == 1

  def out_of_bound(self):
    return self.world.check_oob_from_coo(self.guard_pos_x, self.guard_pos_y)

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
    step_stack = list()
    found_coos = list()
    temp_guard_pos_x = 0
    temp_guard_pos_y = 0
    looped_obstacle_count = 0

    while not self.game.out_of_bound():
      self.game.step()
      turn_heading = self.game.guard_heading + 2
      self.game.world.fetch_line(self.game.guard_pos_x, self.game.guard_pos_y, buf_view_left, turn_heading)
      if not self.game.obstructed() and self.game.char_obstacle in buf_view_left:
        test_game = self.game.clone()

        temp_guard_pos_x = self.game.guard_pos_x
        temp_guard_pos_y = self.game.guard_pos_y
        s0, c0 = self.game.world._octant_to_cosine_sign(turn_heading)
        si, ci = self.game.world._octant_to_cosine_sign(self.game.guard_heading)

        self.game.world.set_char(self.game.guard_pos_x+ci, self.game.guard_pos_y+si, self.game.char_obstacle)
        # print(self.game.world)
        while self.game.char_obstacle in buf_view_left:
          step_info = (temp_guard_pos_x, temp_guard_pos_y, turn_heading)
          # print(step_info, buf_view_left, step_stack)

          if step_info in step_stack:
            looped_obstacle_count += 1
            found_coo = (self.game.guard_pos_x+ci, self.game.guard_pos_y+si)
            duped = found_coo in found_coos
            found_coos.append(found_coo)
            print('found:', looped_obstacle_count, 'coo:', found_coo, 'duped' if duped else '')
            self.game.frame.set_char(self.game.guard_pos_x+ci, self.game.guard_pos_y+si, self.game.char_obstacle)
            for ox, oy, _ in step_stack:
              if not self.game.frame.get_cell_from_coo(ox, oy) == self.game.char_obstacle:
                self.game.frame.set_char(ox, oy, 'X')
            break

          s, c = self.game.world._octant_to_cosine_sign(turn_heading)
          offset = buf_view_left.index(self.game.char_obstacle) - 1
          for o in range(offset):
            step_stack.append((temp_guard_pos_x+(o*c), temp_guard_pos_y+(o*s), turn_heading))

          dx, dy = offset*c, offset*s
          temp_guard_pos_x += dx
          temp_guard_pos_y += dy
          turn_heading += 2
          turn_heading %= 8
          self.game.world.fetch_line(temp_guard_pos_x, temp_guard_pos_y, buf_view_left, turn_heading)
        step_stack.clear()
        self.game.world.set_char(self.game.guard_pos_x+ci, self.game.guard_pos_y+si, self.game.char_empty)

      # print(self.game.world, looped_obstacle_count)
      self.game.frame.replace('X', '.')
    # return looped_obstacle_count
    # for x, y in self.game.world.get_occurrences(self.game.char_obstacle):
    #   self.game.frame.set_char(x, y, '+')
    print(self.game.frame)
    return self.game.frame.count_char(self.game.char_obstacle)
