import typing as t
from io import IOBase
from src.aoc.base_class import AOCBaseClass, AOCRunAsEnum


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
    self.disk_map = list()
    self.tally = list()
    self.index = list()
    self.length = 0
    self.checksum = 0
    self.counter = 0
    # cursor
    self.l_cr = 0
    self.r_cr = 0

  def process_test_answer(self, b: bytes) -> t.Any:
    return int(b)

  def parser(self, buf_io: IOBase) -> t.Any:
    self.disk_map.extend(map(int, buf_io.read().decode(self.default_encoding).strip()))
    self.tally.extend(self.disk_map)
    self.length = len(self.disk_map)
    self.index.extend(self.disk_map)
    for i in range(self.length):
      self.index[i] = i//2 if i%2==0 else -1
    self.r_cr = self.length - 1
    return None

  def _lssw(self, attr, src, dst):
    inst = getattr(self, attr)
    temp = inst[dst]
    inst[dst] = inst[src]
    inst[src] = temp

  def swap(self, src, dst):
    self._lssw('disk_map', src, dst)
    self._lssw('tally', src, dst)
    self._lssw('index', src, dst)

  def insert_null(self, i):
    self.disk_map.insert(i, -1)
    self.tally.insert(i, 0)
    self.index.insert(i, -1)

  @property
  def l_id(self):
    return self.index[self.l_cr]
  
  @property
  def r_id(self):
    return self.index[self.r_cr]

  @property
  def l_is_allocated(self):
    return self.index[self.l_cr] >= 0

  @property
  def r_is_allocated(self):
    return self.index[self.r_cr] >= 0

  def add_checksum(self, n):
    self.checksum += self.counter * n
    self.counter += 1

  def out_of_bound(self):
    return self.l_cr < 0 or self.l_cr >= self.length or self.r_cr < 0 or self.r_cr >= self.length

  def print_stat(self):
    s = f'{self.counter:4d} | {self.checksum:4d} | {self.r_id} | {self.l_id} |'
    _ = print(s, self.tally) if self.length < 50 else print(s)

  def solution_part_1(self, parsed_input) -> t.Any:
    while not self.out_of_bound():
      self.print_stat()
      if self.l_is_allocated:
        while self.tally[self.l_cr]:
          self.tally[self.l_cr] -= 1
          self.add_checksum(self.l_id)
        self.l_cr += 1
      else:
        if self.tally[self.l_cr] == 0:
          self.l_cr += 1
        else:
          if not self.r_is_allocated or self.tally[self.r_cr] == 0:
            self.r_cr -= 1
          else:
            self.add_checksum(self.r_id)
            self.tally[self.l_cr] -= 1
            self.tally[self.r_cr] -= 1
    return self.checksum

  def solution_part_2(self, parsed_input) -> t.Any:
    raise NotImplementedError('puzzle part 2 is not yet implemented')
    return parsed_input
