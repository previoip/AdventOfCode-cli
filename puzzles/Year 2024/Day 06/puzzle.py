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
    self.eval_path_part_2 = 'input_p2.txt'
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

    obstructed = self.viewbuf.count(self.char_obstacle) > 0
    if obstructed:
      self.guard_current_char = self.guard_char_cycle_90deg.get(self.guard_current_char)

    (dx, dy), _ = self.guard_moveset.get(self.guard_current_char)
    ix, iy = x+dx, y+dy
    self.frame.set_char(x, y, self.char_visited)
    self.world.set_char(x, y, self.char_visited)
    self.world.set_char(ix, iy, self.guard_current_char)
    self.guard_current_pos = self.world.coo_to_index(ix, iy)
    return not self.world.check_oob_from_index(self.guard_current_pos)

  def solution_part_1(self, parsed_input) -> t.Any:
    self.guard_current_pos = self.world.get_char_index(self.guard_current_char)
    c = 0
    while self.update():
      c += 1
    return self.world.count_char(self.char_visited)

  def solution_part_2(self, parsed_input) -> t.Any:
    raise NotImplementedError('puzzle part 2 is not yet implemented')
    return parsed_input
