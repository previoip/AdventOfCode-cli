import typing as t
from io import IOBase
from src.aoc.base_class import AOCBaseClass, AOCRunAsEnum
from src.shared.containers import StringMatrixV2
from array import array

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
    self.world = StringMatrixV2('')
    self.frame = StringMatrixV2('')
    self.char_empty = '.'
    self.char_visited = 'X'
    self.char_obstacle = '#'
    self.guard_current_pos = None
    self.guard_current_char = ''
    self.guard_moveset = {
      '^': (( 0,-1), 3),
      '>': (( 1, 0), 0),
      'v': (( 0, 1), 1),
      '<': ((-1, 0), 2),
    }
    self.guard_char_cycle_90deg = {
      '^': '>',
      '>': 'v',
      'v': '<',
      '<': '^',
    }
    self.viewbuf = array('u', '  ')
    self.frame_viewbuf = array('u', '  ')

  def process_test_answer(self, b: bytes) -> t.Any:
    return int(b.decode(self.default_encoding))

  def parser(self, buf_io: IOBase) -> t.Any:
    self.world.from_string(buf_io.read().decode(self.default_encoding))
    self.frame.from_empty(self.world.width, self.world.height, self.char_empty)
    for c in '^><v':
      if self.world.has_char(c):
        self.guard_current_char = c
        break
    return None

  def update(self):
    x, y = self.world.index_to_coo(self.guard_current_pos)
    _, quadrant = self.guard_moveset.get(self.guard_current_char)

    self.world.fetch_line(
      x, y,
      self.viewbuf,
      quadrant * 2
    )

    self.frame.fetch_line(
      x, y,
      self.frame_viewbuf,
      quadrant * 2
    )

    obstructed = self.viewbuf.count(self.char_obstacle) > 0
    if obstructed:
      self.guard_current_char = self.guard_char_cycle_90deg.get(self.guard_current_char)

    (dx, dy), _ = self.guard_moveset.get(self.guard_current_char)
    ix, iy = x+dx, y+dy
    self.frame.set_char(ix, iy, self.guard_current_char)
    self.world.set_char(x, y, self.char_visited)
    self.world.set_char(ix, iy, self.guard_current_char)
    self.guard_current_pos = self.world.coo_to_index(ix, iy)
    return not self.world.check_oob_from_coo(ix, iy)

  def solution_part_1(self, parsed_input) -> t.Any:
    self.guard_current_pos = self.world.get_char_index(self.guard_current_char)
    self.frame.set_char_from_index(self.guard_current_pos, self.guard_current_char)
    c = 0
    import time
    while self.update():
      if c % 10 == 0:
        print(self.frame)
        time.sleep(.01)
      c += 1
      print(self.frame)
    return self.world.count_char(self.char_visited)

  def solution_part_2(self, parsed_input) -> t.Any:
    self.guard_current_pos = self.world.get_char_index(self.guard_current_char)
    self.frame.set_char_from_index(self.guard_current_pos, self.guard_current_char)
    obstacle_frame = StringMatrixV2('').from_empty(self.world.width, self.world.height, self.char_empty)
    scan_loop_buf = array('u', ' '*(max(self.world.width, self.world.height)))
    counter = 0

    while self.update():
      # print(counter)

      while obstacle_frame.count_char(self.char_visited) > 0:
        obstacle_frame.set_char_from_index(obstacle_frame.data.index(self.char_visited), self.char_empty)

      _, quadrant = self.guard_moveset.get(self.guard_current_char)
      x0, y0 = self.world.index_to_coo(self.guard_current_pos)
      x, y = x0, y0
      octant0 = quadrant * 2
      octant0 += 2
      octant = octant0
      self.world.fetch_line(x, y, scan_loop_buf, octant0)
      indefinitely_stuck_in_loop = False
      indefinitely_stuck_in_loop_counter = 0
      while self.char_obstacle in scan_loop_buf:
        jump = scan_loop_buf.index(self.char_obstacle) - 1
        if jump < 1:
          break
        s, c = self.world._octant_to_cosine_sign(octant)
        x, y = x+int(jump*c), y+int(jump*s)

        if not obstacle_frame.get_cell_from_coo(x, y) == self.char_obstacle:
          obstacle_frame.set_char(x, y, self.char_visited)

        if self.world.check_oob_from_coo(x, y):
          break

        octant += 2
        self.world.fetch_line(x, y, scan_loop_buf, octant)

        indefinitely_stuck_in_loop_counter += 1

        if self.guard_current_char in scan_loop_buf:
          print(counter, 'found!')
          jump = scan_loop_buf.index(self.guard_current_char) + 1
          s, c = self.world._octant_to_cosine_sign(octant)
          x, y = x+int(jump*c), y+int(jump*s)
          obstacle_frame.set_char(x, y, self.char_obstacle)
          break
        if indefinitely_stuck_in_loop_counter > 10000:
          print(counter, 'stuck in internal loop?')
          # s, c = self.world._octant_to_cosine_sign(octant0-2)
          # x, y = x0+int(c), y0+int(s)
          # obstacle_frame.set_char(x, y, self.char_obstacle)
          break

      counter += 1
    print(obstacle_frame)
    return obstacle_frame.count_char(self.char_obstacle)
