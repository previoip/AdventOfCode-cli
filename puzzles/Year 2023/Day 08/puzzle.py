import typing as t
from io import IOBase
from src.aoc.base_class import AOCBaseClass, AOCRunAsEnum
from collections import namedtuple, OrderedDict

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
    nt = namedtuple('Dir', field_names=['pos', 'L', 'R'])
    inp = buf_io.read().decode(self.default_encoding).splitlines()
    instr = inp.pop(0)

    inp = filter(lambda x: x, inp)
    inp = map(lambda x: x.split(' = '), inp)
    inp = map(lambda x: (x[0], x[1][1:-1]), inp)
    inp = map(lambda x: (x[0], x[1].replace(' ', '').split(',')), inp)
    inp = map(lambda x: (x[0], nt(x[0], *x[1])), inp)
    inp = OrderedDict(inp)
    return instr, inp


  def solution_part_1(self, parsed_input) -> t.Any:
    instr, nodes = parsed_input
    instr_len = len(instr)
    start_pos = 'AAA'
    target_pos = 'ZZZ'

    print(nodes)
    print('compiling...')
    pos = start_pos
    jump_nodes = OrderedDict()
    nt_jmp = namedtuple('JumpNode', field_names=['pos', 'next_pos', 'n'])
    for pos in nodes.keys():
      last_pos = pos
      n = instr_len
      for n_i, i in enumerate(instr):
        next_node = nodes.get(pos)
        pos = getattr(next_node, i)
        if pos == target_pos:
          n = n_i + 1
      jump_nodes[last_pos] = nt_jmp(last_pos, pos, n)

    pos = start_pos
    for _ in range(1_000_000):
      curr_node = jump_nodes.get(pos)
      if curr_node.pos == start_pos and curr_node.next_pos == target_pos:
        break
      next_node = jump_nodes.get(curr_node.next_pos)
      jump_nodes[pos] = nt_jmp(pos, next_node.next_pos, curr_node.n + next_node.n)
      del jump_nodes[next_node.pos]


    print(jump_nodes)

    # c = 0
    # pos = next(iter(nodes.keys()))
    # for _ in range(100_000_000_000):
    #   i = instr[c % instr_len]
    #   pred = nodes.get(pos)
    #   pos = getattr(pred, i)
    #   c += 1
    #   if pos == tgt_pos:
    #     break
    # return c

    return jump_nodes.get(start_pos).n

  def solution_part_2(self, parsed_input) -> t.Any:
    #  yield
    return