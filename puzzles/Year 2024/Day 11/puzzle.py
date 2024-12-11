import typing as t
from io import IOBase
from src.aoc.base_class import AOCBaseClass, AOCRunAsEnum
from collections import deque


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
    return int(b)

  def parser(self, buf_io: IOBase) -> t.Any:
    return tuple(map(int, buf_io.read().decode(self.default_encoding).strip().split()))

  _10th_power = [10**n for n in range(4299)]

  @classmethod
  def _fast_log10(cls, n):
    for i in range(4299):
      if n-cls._10th_power[i] < 0:
        return i

  @classmethod
  def split_even_number(cls, n):
    i = cls._fast_log10(n) // 2
    return divmod(n, cls._10th_power[i])

  @classmethod
  def predicate(cls, engraving):
    if engraving == 0:
      yield 1
    elif cls._fast_log10(engraving) % 2 == 0:
      yield from cls.split_even_number(engraving)
    else:
      yield engraving * 2024

  def solution_part_1(self, parsed_input) -> t.Any:
    stone_queue = deque()
    stone_count = 0
    # stone_logs = dict()
    for engraving in parsed_input:
      stone_queue.append((engraving, 25))

    while stone_queue:
      engraving, tally = stone_queue.pop()
      # if not stone_logs.get(tally):
      #   stone_logs[tally] = list()
      # stone_logs[tally].append(engraving)
      if tally == 0:
        stone_count += 1
      else:
        tally -= 1
        for new_engraving in self.predicate(engraving):
          stone_queue.append((new_engraving, tally))
    # print(stone_logs)
    return stone_count

  def solution_part_2(self, parsed_input) -> t.Any:
    stone_queue = deque()
    stone_count = 0
    for engraving in parsed_input:
      stone_queue.append((engraving, 75))

    peek_length = 100
    peek_averager = [0 for _ in range(peek_length)]
    peek_counter = 0

    count = 0
    while stone_queue:

      if count % 100000 == 0:
        peek_averager[peek_counter] = len(stone_queue)
        peek_counter += 1
        peek_counter %= peek_length
        print('deque len: {:.2f}\tfound stones: {}'.format(sum(peek_averager)/peek_length, stone_count))

      count += 1
      engraving, tally = stone_queue.pop()
      if tally == 0:
        stone_count += 1
      else:
        tally -= 1
        for new_engraving in self.predicate(engraving):
          stone_queue.append((new_engraving, tally))
    print('iterated for', count, 'times')
    return stone_count
