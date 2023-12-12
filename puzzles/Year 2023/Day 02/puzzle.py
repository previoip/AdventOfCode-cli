import typing as t
from io import IOBase
from src.aoc.base_class import AOCBaseClass, AOCRunAsEnum
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

  def parser(self, buf_io: IOBase) -> t.Any:
    cubes_namedtuple = namedtuple('Cubes', field_names=['count', 'color'], defaults=[None, None])
    game_set_namedtuple = namedtuple('GameSet', field_names=['game_id', 'sets'], defaults=[None, None])
    inp = buf_io.read().decode(self.default_encoding)
    ret = list()

    for i in inp.splitlines(): 
      delim_index = i.find(':')
      game_id, i = i[:delim_index], i[delim_index+1:]
      game_id = int(game_id.split()[-1])
      sets = map(lambda x: tuple(map(lambda y: cubes_namedtuple(*y.split()), x.strip().split(','))), i.split(';'))
      sets = list(sets)
      ret.append(game_set_namedtuple(game_id, sets))
    return ret

  def solution_part_1(self, parsed_input) -> t.Any:
    sums = 0
    game_sets = dict()
    for game_id, sets in parsed_input:
      if not game_sets.get(game_id):
        game_sets[game_id] = dict()
      
      for n, set_n in enumerate(sets):
        for count, color in set_n:
          if not game_sets[game_id].get(color):
            game_sets[game_id][color] = 0
          game_sets[game_id][color] = max(int(count), game_sets[game_id][color])

    ret = 0
    for game_id, res in game_sets.items():
      det = True
      det = det and res.get('red', 0) <= 12
      det = det and res.get('green', 0) <= 13
      det = det and res.get('blue', 0) <= 14
      if det:
        ret += int(game_id)
    return ret

  def solution_part_2(self, parsed_input) -> t.Any:
    sums = 0
    game_sets = dict()
    for game_id, sets in parsed_input:
      if not game_sets.get(game_id):
        game_sets[game_id] = dict()
      
      for n, set_n in enumerate(sets):
        for count, color in set_n:
          if not game_sets[game_id].get(color):
            game_sets[game_id][color] = 0
          game_sets[game_id][color] = max(int(count), game_sets[game_id][color])

    ret = 0
    for game_id, res in game_sets.items():
      p = 1
      p *= res.get('red', 0)
      p *= res.get('green', 0)
      p *= res.get('blue', 0)
      ret += p
    return ret

  def process_test_answer(self, b: bytes) -> t.Any:
    return int(b.decode(self.default_encoding))