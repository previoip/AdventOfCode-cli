import typing as t
from io import IOBase
from src.aoc.base_class import AOCBaseClass, AOCRunAsEnum
from src.shared.containers import StringMatrixV2 as StringMatrix

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
    self.char_empty = '.'
    self.char_visited = '%'
    self.char_trail_end = 'O'
    self.world = StringMatrix('')
    self.frame = StringMatrix('')
    self.step_queue = list()
    self.nums_queue = list()

  def process_test_answer(self, b: bytes) -> t.Any:
    return int(b)

  def parser(self, buf_io: IOBase) -> t.Any:
    self.world.from_string(buf_io.read().decode(self.default_encoding))
    self.frame.from_empty(self.world.width, self.world.height, self.char_empty)
    self.step_queue.clear()
    self.nums_queue.clear()
    self.step_queue.extend(self.world.get_occurrences('0'))
    self.nums_queue.extend([0 for _ in range(len(self.step_queue))])

  def solution_part_1(self, parsed_input) -> t.Any:
    viewbuf = [0]
    starting_step = list(self.step_queue)
    starting_nums = list(self.nums_queue)
    starting_tots = len(starting_nums)
    scores = [0 for _ in range(starting_tots)]
    for n in range(starting_tots):
      for x, y in self.frame.get_occurrences(self.char_trail_end):
        self.frame.set_char(x, y, self.char_empty)
      for x, y in self.frame.get_occurrences(self.char_visited):
        self.frame.set_char(x, y, self.char_empty)
      self.step_queue.clear()
      self.nums_queue.clear()
      self.step_queue.append(starting_step[n])
      self.nums_queue.append(starting_nums[n])
      while self.step_queue:
        x, y = self.step_queue.pop(0)
        curr_h = self.nums_queue.pop(0)
        next_h = curr_h + 1
        for octant in (0, 2, 4, 6):
          s, c = self.world._octant_to_cosine_sign(octant)
          ix, iy = int(x+c), int(y+s)
          self.world.fetch_line(x, y, viewbuf, octant, 1)
          if not viewbuf[0].isnumeric():
            continue
          viewnum = int(viewbuf[0])
          if viewnum == 9 and curr_h==8 :
            self.frame.set_char(ix, iy, self.char_trail_end)
          if viewnum == next_h:
            self.step_queue.append((ix, iy))
            self.nums_queue.append(viewnum)
        # self.frame.set_char(x, y, self.char_visited)
      # print(self.world)
      # print(self.frame)
      scores[n] += self.frame.count_char(self.char_trail_end)
    return sum(scores)

  def solution_part_2(self, parsed_input) -> t.Any:
    viewbuf = [0]
    starting_step = list(self.step_queue)
    starting_nums = list(self.nums_queue)
    starting_tots = len(starting_nums)
    scores = [0 for _ in range(starting_tots)]
    for n in range(starting_tots):
      for x, y in self.frame.get_occurrences(self.char_trail_end):
        self.frame.set_char(x, y, self.char_empty)
      for x, y in self.frame.get_occurrences(self.char_visited):
        self.frame.set_char(x, y, self.char_empty)
      self.step_queue.clear()
      self.nums_queue.clear()
      self.step_queue.append(starting_step[n])
      self.nums_queue.append(starting_nums[n])
      while self.step_queue:
        x, y = self.step_queue.pop(0)
        curr_h = self.nums_queue.pop(0)
        next_h = curr_h + 1
        for octant in (0, 2, 4, 6):
          s, c = self.world._octant_to_cosine_sign(octant)
          ix, iy = int(x+c), int(y+s)
          self.world.fetch_line(x, y, viewbuf, octant, 1)
          if not viewbuf[0].isnumeric():
            continue
          viewnum = int(viewbuf[0])
          if viewnum == 9 and curr_h==8 :
            scores[n] += 1
          if viewnum == next_h:
            self.step_queue.append((ix, iy))
            self.nums_queue.append(viewnum)
    return sum(scores)