import typing as t
from io import IOBase
from src.aoc.base_class import AOCBaseClass, AOCRunAsEnum
from src.shared.containers import StringMatrixV2
from array import array, ArrayType
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
    self.warehouse: StringMatrixV2 = None
    self.instr_set = ''
    self.instr_cursor = 0
    self.instr_len = 0
    self.instr_curr = ''
    self.char_robot = '@'
    self.char_null = StringMatrixV2.empty
    self.moveset = {
      '^': (( 0,-1), 6),
      'v': (( 0, 1), 2),
      '<': ((-1, 0), 4),
      '>': (( 1, 0), 0),
    }
    self.view_buff: ArrayType = None
    self.view_buff_len = 0
    self.robot_curr_x = 0
    self.robot_curr_y = 0
    self.robot_curr_h = 0

  def process_test_answer(self, b: bytes) -> t.Any:
    return int(b)

  def parser(self, buf_io: IOBase) -> t.Any:
    line = buf_io.readline().decode(self.default_encoding)
    mapstr = ''
    while line.strip():
      mapstr += line
      line = buf_io.readline().decode(self.default_encoding)
    self.warehouse = StringMatrixV2(mapstr)

    line = buf_io.readline().decode(self.default_encoding)
    self.instr_set = ''
    while line.strip():
      self.instr_set += line
      line = buf_io.readline().decode(self.default_encoding)
    self.instr_len = len(self.instr_set.rstrip())
    self.instr_cursor = 0
    self.view_buff_len = max(self.warehouse.width, self.warehouse.height)
    self.view_buff = array('u', self.char_null*self.view_buff_len)

    self.robot_curr_x, self.robot_curr_y = self.warehouse.index_to_coo(
      self.warehouse.get_char_index(self.char_robot)
    )
    return

  def get_next_instruction(self):
    while not self.instr_set[self.instr_cursor].strip():
      self.instr_cursor += 1
    self.instr_curr = self.instr_set[self.instr_cursor]
    self.instr_cursor += 1
    return self.instr_curr

  @staticmethod
  def _get_occurrences(arr: ArrayType, c: str):
    n = arr.count(c)
    offset = -1
    for _ in range(n):
      offset = arr.index(c, offset+1)
      yield offset

  def view_buff_index_to_coo(self, i):
    s, c = self.warehouse._octant_to_cosine_sign(self.robot_curr_h)
    return (i * c + self.robot_curr_x, i * s + self.robot_curr_y)

  def exhausted(self):
    return self.instr_cursor < 0 or self.instr_cursor >= self.instr_len

  def solution_part_1(self, parsed_input) -> t.Any:
    char_wall = '#'
    char_box = 'O'
    char_empty = '.'
    print(self.warehouse)
    while not self.exhausted():
      (dx, dy), self.robot_curr_h = self.moveset.get(self.get_next_instruction())
      self.warehouse.fetch_line(self.robot_curr_x, self.robot_curr_y, self.view_buff, self.robot_curr_h)
      if self.view_buff[1] == char_wall:
        continue
      if self.view_buff[1] == char_empty:
        self.warehouse.set_char(self.robot_curr_x, self.robot_curr_y, char_empty)
        self.robot_curr_x += dx
        self.robot_curr_y += dy
        self.warehouse.set_char(self.robot_curr_x, self.robot_curr_y, self.char_robot)
        continue
      if self.view_buff[1] == char_box:
        view_cursor = 1
        view_stack = list()
        while self.view_buff[view_cursor] == char_box:
          view_stack.append(view_cursor)
          view_cursor += 1
        if self.view_buff[view_cursor] == char_wall:
          continue
        if self.view_buff[view_cursor] == char_empty:
          for i in reversed(view_stack):
            bx, by = self.view_buff_index_to_coo(i)
            self.warehouse.set_char(bx, by, char_empty)
            self.warehouse.set_char(bx+dx, by+dy, char_box)
          self.warehouse.set_char(self.robot_curr_x, self.robot_curr_y, char_empty)
          self.robot_curr_x += dx
          self.robot_curr_y += dy
          self.warehouse.set_char(self.robot_curr_x, self.robot_curr_y, self.char_robot)
    print(self.warehouse)

    scores = 0
    for x, y in self.warehouse.get_occurrences(char_box):
      scores += x + y * 100
    return scores

  def solution_part_2(self, parsed_input) -> t.Any:
    s = str(self.warehouse)
    s = s.replace(char_wall, char_wall*2)
    s = s.replace(char_box, '[]')
    s = s.replace(char_empty, '..')
    s = s.replace(self.char_robot, '@.')
    self.warehouse.from_string(s)

    raise NotImplementedError('puzzle part 2 is not yet implemented')
    scores = 0
    for x, y in self.warehouse.get_occurrences('['):
      scores += x + y * 100
    return scores
