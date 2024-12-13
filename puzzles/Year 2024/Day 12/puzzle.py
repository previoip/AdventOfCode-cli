import typing as t
from io import IOBase
from src.aoc.base_class import AOCBaseClass, AOCRunAsEnum
from src.shared.containers import StringMatrixV2 as StringMatrix
from array import array
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
    self.field = StringMatrix('')
    self.frame = StringMatrix('')
    self.edges = StringMatrix('')
    self.field_view = array('u', ' '*1)
    self.frame_view = array('u', ' '*1)
    self.char_searched = '#'
    self.char_ignored = '.'
    self.char_edge_v = '|'
    self.char_edge_h = '-'
    self.edge_to_oct = {
      self.char_edge_h: ((0, (1, 7)), (4, (3, 5))),
      self.char_edge_v: ((2, (1, 3)), (6, (5, 7)))
      # self.char_edge_h: ((0, (2, 6)), (4, (2, 6))),
      # self.char_edge_v: ((2, (0, 4)), (6, (0, 4)))
    }
    self.search_queue = deque()

  def process_test_answer(self, b: bytes) -> t.Any:
    return int(b)

  def parser(self, buf_io: IOBase) -> t.Any:
    self.field.from_string(buf_io.read().decode(self.default_encoding))
    self.frame.from_empty(self.field.width, self.field.height, ' ')
    self.edges.from_empty(self.field.width, self.field.height, ' ')
    self.edges.pad_once()

  def solution_part_1(self, parsed_input) -> t.Any:
    print(self.field)
    searched_count = list()
    edges_count = list()

    for i, c in self.field.iter_cell():
      x, y = self.field.index_to_coo(i)
      if self.frame.get_cell_from_index(i) == self.char_searched or \
         self.frame.get_cell_from_index(i) == self.char_ignored:
        continue
      curr_char = self.field.get_cell_from_coo(x, y)

      for ii in self.field.flood_fill_indices(x, y):
        ix, iy = self.field.index_to_coo(ii)
        self.frame.set_char(ix, iy, self.char_searched)
        self.edges.set_char(
          self.edges.offset_scale_index(ix),
          self.edges.offset_scale_index(iy),
          curr_char
        )

        for oc, ed in((0, self.char_edge_v), (4, self.char_edge_v), (2, self.char_edge_h), (6, self.char_edge_h)):
          ss, sc = self.field._octant_to_cosine_sign(oc)
          jx, jy = int(ix+sc), int(iy+ss)
          if self.field.get_cell_from_coo(jx, jy) != curr_char:
            self.edges.set_char(
              self.edges.offset_scale_index(ix) + sc,
              self.edges.offset_scale_index(iy) + ss,
              ed
            )

      print(self.frame)
      print(self.edges)
      searched_count.append(self.frame.count_char(self.char_searched))
      edges_count.append(self.edges.count_char(self.char_edge_v) + self.edges.count_char(self.char_edge_h))
      self.frame.replace(self.char_searched, self.char_ignored)
      self.edges.replace(self.char_edge_v, ' ')
      self.edges.replace(self.char_edge_h, ' ')
    return sum(map(lambda x: x[0]*x[1], zip(searched_count, edges_count)))


  def solution_part_2(self, parsed_input) -> t.Any:
    import time
    searched_count = list()
    edges_count = list()

    for i, c in self.field.iter_cell():
      x, y = self.field.index_to_coo(i)
      if self.frame.get_cell_from_index(i) == self.char_searched or \
         self.frame.get_cell_from_index(i) == self.char_ignored:
        continue
      curr_char = self.field.get_cell_from_coo(x, y)

      for ii in self.field.flood_fill_indices(x, y):
        ix, iy = self.field.index_to_coo(ii)
        self.frame.set_char(ix, iy, self.char_searched)
        self.edges.set_char(
          self.edges.offset_scale_index(ix),
          self.edges.offset_scale_index(iy),
          curr_char
        )

        for oc, ed in ((0, self.char_edge_v), (4, self.char_edge_v), (2, self.char_edge_h), (6, self.char_edge_h)):
          ss, sc = self.field._octant_to_cosine_sign(oc)
          jx, jy = int(ix+sc), int(iy+ss)
          if self.field.get_cell_from_coo(jx, jy) != curr_char:
            self.edges.set_char(
              self.edges.offset_scale_index(ix) + sc,
              self.edges.offset_scale_index(iy) + ss,
              ed
            )

      edge_count = 0
      for ii, ce in self.edges.iter_cell():
        if not ce in (self.char_edge_h, self.char_edge_v) or \
          ce == self.char_searched or ce == self.edges.empty:
          continue
        edge_count += 1
        # print('>>', edge_count)
        x, y = self.edges.index_to_coo(ii)
        char_curr = self.edges.get_cell_from_coo(x, y)
        char_tangent = self.char_edge_h if char_curr == self.char_edge_v else self.char_edge_v
        self.edges.set_char(x, y, self.char_searched)
        for oc, (hea_oc_l, hea_oc_r) in self.edge_to_oct.get(ce):
          ss, sc = self.field._octant_to_cosine_sign(oc)
          ss_l, sc_l = self.field._octant_to_cosine_sign(hea_oc_l)
          ss_r, sc_r = self.field._octant_to_cosine_sign(hea_oc_r)
          ox = sc * (self.edges.scale + 1)
          oy = ss * (self.edges.scale + 1)
          ix, iy = x, y
          ix += ox
          iy += oy

          char_view_l = self.edges.get_cell_from_coo(x+sc_l, y+ss_l)
          char_view_r = self.edges.get_cell_from_coo(x+sc_r, y+ss_r)
          # print('>>>&', char_view_l, '::',  char_view_r, '::', char_tangent)
          if char_view_l in (char_tangent, self.char_searched) or \
            char_view_r in (char_tangent, self.char_searched): break

          while True:
            char_q = self.edges.get_cell_from_coo(ix, iy)
            if char_q == self.char_searched: break
            if char_q == self.edges.empty: break
            self.edges.set_char(ix, iy, self.char_searched)
            char_view_l = self.edges.get_cell_from_coo(ix+sc_l, iy+ss_l)
            char_view_r = self.edges.get_cell_from_coo(ix+sc_r, iy+ss_r)
            # print('>>>>', char_view_l, '::',  char_view_r, '::', char_tangent)
            if char_view_l in (char_tangent, self.char_searched) or \
              char_view_r in (char_tangent, self.char_searched): break
            ix += ox
            iy += oy
        # print(self.edges)
      # print(edge_count)

      # print(self.edges)
      # print(self.frame, flush=True)
      num_sect = self.frame.count_char(self.char_searched)
      print(edge_count, num_sect)
      # time.sleep(.08)
      searched_count.append(num_sect)
      edges_count.append(edge_count)
      self.frame.replace(self.char_searched, self.char_ignored)
      self.edges.replace(self.char_edge_v, ' ')
      self.edges.replace(self.char_edge_h, ' ')
      self.edges.replace(self.char_searched, ' ')
    return sum(map(lambda x: x[0]*x[1], zip(searched_count, edges_count)))
