import typing as t
from io import IOBase
from src.aoc.base_class import AOCBaseClass, AOCRunAsEnum
from collections import namedtuple
import re



def cast(map_type, val, print_=True):

  for m_range in map_type.ranges:
    if val >= m_range.src and val < (m_range.src + m_range.len):
      p_val = val
      val = m_range.dst + (val - m_range.src)
      if print_: print(map_type.src.center(14), '->', map_type.dst.center(14), m_range, p_val, '->', val)
      return val
  else:
    if print_: print(map_type.src.center(14), '->', map_type.dst.center(14), m_range, val, '==', val)

  return val


_cache = dict()
def cast_cached(map_type, val, print_=True):
  src_cache = _cache.get(map_type.src)
  if src_cache is None:
    _cache[map_type.src] = dict()
  src_cache = _cache[map_type.src]

  dst_cache = src_cache.get(map_type.dst)
  if dst_cache is None:
    _cache[map_type.src][map_type.dst] = dict()
  dst_cache = _cache[map_type.src][map_type.dst]

  ret = dst_cache.get(val)
  if ret is None:
    ret = cast(map_type, val, print_)
    _cache[map_type.src][map_type.dst][val] = ret

  return ret






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
    return int(b.decode(self.default_encoding))

  def parser(self, buf_io: IOBase) -> t.Any:
    re_map_tok = re.compile(r'^(\w*?)\-(\w*?)\-(\w*?)\smap\:')
    inp = buf_io.read().decode(self.default_encoding)
    struct_seeds = namedtuple('Seed', field_names=['items'])
    struct_map_t = namedtuple('MapType', field_names=['src', 'dst', 'ranges'])
    struct_range = namedtuple('MapRange', field_names=['dst', 'src', 'len'])
    
    it = list(filter(lambda x: x, inp.splitlines()))
    seeds, seed_items = it.pop(0).split(':')
    seed = struct_seeds(list(map(int, seed_items.split())))
    maps = list(filter(lambda x: x, it))
    toks = map(lambda x: (x[0], not re_map_tok.match(x[1]) is None), enumerate(maps))
    toks = filter(lambda x: x[1], toks)
    toks = list(map(lambda x: x[0], toks))

    temp = list()
    for n, i in enumerate(toks):
      tok = maps[i]
      tok = re_map_tok.match(tok).groups()

      next_i = toks[n+1] if n < len(toks)-1 else 0
      map_ranges = maps[i+1:next_i] if next_i != 0 else maps[i+1:]
      map_ranges = [list(map(int, i.split())) for i in map_ranges]
      map_ranges = list(map(lambda x: struct_range(*x), map_ranges))

      tok = struct_map_t(tok[0], tok[-1], map_ranges)
      temp.append(tok)

    return seed, temp

  def solution_part_1(self, parsed_input) -> t.Any:
    seed, maps = parsed_input

    res = []
    for i in seed.items:
      for map_t in maps:
        i = cast(map_t, i)
      print()
      res.append(i)
    print(res)

    return min(res)


  def solution_part_2(self, parsed_input) -> t.Any:
    seed, maps = parsed_input

    res = []
    for i_start, i_range in zip(seed.items[::2], seed.items[1::2]):
      for i in range(i_start, i_start + i_range):
        for map_t in maps:
          i = cast(map_t, i, print_=True)
        print()
        res.append(i)
    print(res)

    return min(res)
