import typing as t
from io import IOBase
from src.aoc.base_class import AOCBaseClass, AOCRunAsEnum
from src.shared.containers import StringMatrixV2 as StringMatrix
from array import array
from math import copysign


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
    self.frame_char_null = ' '
    self.frame_char_searched = '.'
    self.frame_arr_searched = array('u', self.frame_char_searched*4)

  def process_test_answer(self, b: bytes) -> t.Any:
    return int(b.decode(self.default_encoding))

  def parser(self, buf_io: IOBase) -> t.Any:
    return buf_io.read().decode(self.default_encoding)

  def solution_part_1(self, parsed_input) -> t.Any:
    count = 0
    view = array('u', ' '*4)
    frame_view = array('u', ' '*4)
    string_matrix = StringMatrix(parsed_input)
    frame_matrix = StringMatrix('').from_empty(string_matrix.width, string_matrix.height, self.frame_char_null)
    print(string_matrix)

    for n, cel in string_matrix.iter_cell():
      x, y = string_matrix.index_to_coo(n)
      for i in range(8):
        indices = string_matrix.fetch_line(x,y,view,i)
        if view.tounicode() == 'XMAS':
          frame_matrix.fetch_line(x, y, frame_view, i)
          for j in indices:
            frame_matrix.set_char_from_index(j, self.frame_char_searched)
          count += 1
    print(frame_matrix)
    return count

  def solution_part_2(self, parsed_input) -> t.Any:
    from itertools import chain
    count = 0
    view_1 = array('u', ' '*3)
    view_2 = array('u', ' '*3)

    string_matrix = StringMatrix(parsed_input)
    frame_matrix = StringMatrix('').from_empty(string_matrix.width, string_matrix.height, self.frame_char_null)
    print(string_matrix)
    mas_set = 'MAS'

    for n, cel in string_matrix.iter_cell():
      x, y = string_matrix.index_to_coo(n)
      for i, j, oi, oj, in ((1,3,-1,-1), (1,7,-1,-1), (5,3,-1,-1), (5,7,-1,-1)):
        indices_1 = string_matrix.fetch_line(x,y,view_1,i,oi)
        indices_2 = string_matrix.fetch_line(x,y,view_2,j,oj)
        if view_1.tounicode() == mas_set and view_2.tounicode() == mas_set:
          for k in chain(indices_1, indices_2):
            frame_matrix.set_char_from_index(k, self.frame_char_searched)
          count += 1
    print(frame_matrix)
    return count
