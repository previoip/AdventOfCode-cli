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

  def _lsmv(self, attr, src, dst):
    inst = getattr(self, attr)
    temp = inst.pop(src)
    inst.insert(dst, temp)

  def move(self, src, dst):
    print('moved', src, dst)
    self._lsmv('disk_map', src, dst)
    self._lsmv('tally', src, dst)
    self._lsmv('index', src, dst)

  def pop(self, i):
    self.disk_map.pop(i)
    self.tally.pop(i)
    self.index.pop(i)

  def insert_null(self, i, n):
    self.disk_map.insert(i, -1)
    self.tally.insert(i, n)
    self.index.insert(i, -1)
    self.length += 1
    if i < self.r_cr:
      self.r_cr += 1
    if i < self.l_cr:
      self.l_cr += 1

  def defrag_nulls(self):
    def predicate():
      for i in range(1, self.length-1):
        if self.index[i] < 0 and self.index[i+1] < 0:
          return i
      return -1

    while True:
      i = predicate()
      if i < 0:
        break
      print('defragging nulls', i)
      left = self.tally[i+1]
      self.tally[i] += left
      self.pop(i+1)
      self.length -= 1

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
    s = f'{self.counter:04d}, cksum:{self.checksum:4d}, id(l):{self.l_id}, id(r):{self.r_id}, cu(l):{self.l_cr}, cu(r):{self.r_cr}, ta(l):{self.tally[self.l_cr]}, ta(r):{self.tally[self.r_cr]}'
    if self.length < 50_000:
      fmt = ('{:3d} |' * self.length)[:-2]
      i = fmt.format(*range(self.length))
      print(i)
      print('-'*len(i))
      print(fmt.format(*self.index))
      print(fmt.format(*self.tally))
      r = ''
      for n in range(self.length):
        r += ('.' if self.index[n] < 0 else chr(self.index[n]+48)) * self.tally[n]
      print(r)
    print()
    print(s)
    print()

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

  def search_lowest_left_tally(self):
    for j in range(self.length-1, self.l_cr, -1):
      if self.index[j] < 0:
        continue
      for i in range(self.tally[self.l_cr], 0, -1):
        if self.tally[j] == i:
          return j 
    return None



  def solution_part_2(self, parsed_input) -> t.Any:
    import time
    runtime = 0
    while not self.out_of_bound():    
      runtime += 1
      if runtime > 2:
        break

      for r_cr in set(reversed(self.index)):
        self.print_stat()
        time.sleep(.5)
        if r_cr == -1:
          continue
        print(r_cr)
        self.r_cr = self.index.index(r_cr)
        if self.r_is_allocated:
          for n in range(self.length):
            if self.index[n] >= 0:
              continue
            elif self.tally[n] >= self.tally[self.r_cr]:
              print('found candidate:', n)
              size = self.tally[self.r_cr]
              self.tally[n] -= size 
              self.disk_map[n] -= size
              self.move(self.r_cr, n)
              self.insert_null(self.r_cr, size)
              # self.defrag_nulls() 
              self.r_cr -= 1
              break
          else:
            self.r_cr -= 1
        else:
          self.r_cr -= 1
        # r_cr_lw = self.search_lowest_left_tally()
        # if r_cr_lw is None:
        #   self.l_cr += 1
        #   continue
        # self.r_cr = r_cr_lw
        # removed_block = self.tally[self.r_cr]
        # self.move(self.r_cr, self.l_cr+1)
        # self.insert_null(self.r_cr, removed_block)
        # self.r_cr = self.l_cr + 1
        # self.defrag_nulls()
        # while self.tally[self.r_cr] > 0 and self.tally[self.l_cr] > 0:
        #   self.tally[self.l_cr] -= 1
        #   self.tally[self.r_cr] -= 1
        #   self.add_checksum(self.r_id)
        # if self.tally[self.l_cr] == 0:
        #   self.l_cr += 1
    return self.checksum
