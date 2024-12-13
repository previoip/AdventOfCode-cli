import typing as t
from array import array
from math import copysign
from collections import deque

class StringMatrix:
  empty = ' '

  def __init__(self, str_):
    spl = str_.splitlines()
    self.width = len(spl[0])
    self.height = len(spl)
    self.length = self.width * self.height
    self._buf = str_.replace('\r\n', '').replace('\n', '').replace('\r', '')
    if len(self._buf) < self.length:
      self._buf += self.empty * (self.length - len(self._buf))

  def coord_to_index(self, x, y):
    return x + (y * self.width)

  def index_to_coord(self, i):
    return i % self.width, i // self.width

  def check_oob(self, x, y):
    i = self.coord_to_index(x, y)
    return i >= self.length or i < 0

  def set_char(self, x, y, char):
    if self.check_oob(x, y):
      return
    i = self.coord_to_index(x, y)
    self._buf = self._buf[:i] + char + self._buf[i+1:]

  def query_cel(self, x, y):
    if self.check_oob(x, y):
      return self.empty
    return self._buf[self.coord_to_index(x, y)]

  def query_row(self, y):
    l = self.width * y
    return self._buf[l : l + self.width]

  def query_col(self, x):
    return self._buf[x : : self.width]

  def query_kernel(self, x, y, w, h, nl='\n'):
    r = ''
    mx = (w // 2)
    my = (h // 2)
    for dy in range(h):
      dy = dy + y - my
      for dx in range(w):
        dx = dx + x - mx
        r += self.query_cel(dx, dy)
      r += nl
    return r

  def __repr__(self):
    return self.to_str(nl='\n')

  def to_str(self, nl=''):
    r = ''
    for i in range(self.height):
      r += self.query_row(i)
      r += nl
    return r

  def iter_cells(self):
    for n, char in enumerate(self._buf):
      yield char, self.index_to_coord(n)


class StringMatrixV2:
  empty = ' '

  def __init__(self, string: str, strict=False):
    self.data = None
    self.strict = strict
    self.width = 0
    self.height = 0
    self.length = 0
    self.scale = 0
    if string:
      self.from_string(string)
    else:
      self.data = array('u', '')

  @property
  def scale_offset(self):
    return 2 ** self.scale - 1 

  def offset_scale_index(self, n):
    return self.scale_offset + (n * (self.scale_offset + 1))

  def offset_scale_coo(self, x, y):
    return self.offset_scale_index(x), self.offset_scale_index(y)

  def from_string(self, string):
    string = string.strip()
    self.data = array('u', string.replace('\n', '').replace('\r', ''))
    rows = string.splitlines()
    self.width = len(rows[0])
    self.height  = len(rows)
    self.length = self.width * self.height
    for row in rows:
      assert self.width == len(row)
    self.scale = 0
    return self

  def from_empty(self, w, h, c=' '):
    if not c:
      c = self.empty
    self.width = w
    self.height = h
    self.length = self.width * self.height
    self.data = array('u', c*self.length)
    self.scale = 0
    return self

  def index_to_coo(self, n):
    return n % self.width, n // self.width
  
  def coo_to_index(self, x, y):
    return x + self.width * y

  def check_oob_from_coo(self, x, y):
    if x < 0 or x >= self.width:
      return True
    if y < 0 or y >= self.height:
      return True
    return False

  def check_oob_from_index(self, n):
    x, y = self.index_to_coo(n)
    return self.check_oob_from_coo(x, y)

  def get_cell_from_index(self, n):
    if self.check_oob_from_index(n):
      if self.strict:
        raise IndexError()
      return self.empty
    return self.data[n]

  def get_cell_from_coo(self, x, y):
    if self.check_oob_from_coo(x, y):
      if self.strict:
        raise IndexError()
      return self.empty
    return self.data[self.coo_to_index(x, y)]

  def get_col(self, n):
    if n >= self.width:
      if self.strict:
        raise IndexError()
      return array('u', self.empty*self.height)
    return self.data[n::self.width]

  def get_row(self, n):
    if n >= self.height:
      if self.strict:
        raise IndexError()
      return array('u', self.empty*self.width)
    return self.data[self.width*n:self.width*(n+1)]

  @staticmethod
  def _octant_to_cosine_sign(octant):
    octant %= 8
    s = copysign(1, 4-octant) if octant % 4 != 0 else 0
    octant += 2
    octant %= 8
    c = copysign(1, 4-octant) if octant % 4 != 0 else 0
    return int(s), int(c)

  def fetch_line(self, x, y, arr, octant=0, offset=0):
    n = len(arr)
    ind = array('i', range(n))
    s, c = self._octant_to_cosine_sign(octant)
    for i in range(n):
      ix, iy = x+int((i+offset)*c), y+int((i+offset)*s)
      ind[i] = self.coo_to_index(ix, iy)
      arr[i] = self.get_cell_from_coo(ix, iy)
    return ind

  def get_line(self, x, y, n, octant=0, offset=0):
    buf = array('u', ' '*n)
    ind = self.fetch_line(x, y, buf, octant, offset)
    return ind, buf

  def get_occurrences(self, c):
      n = self.count_char(c)
      indices = [None for _ in range(n)]
      offset = -1
      for i in range(n):
        offset = self.data.index(c, offset+1)
        indices[i] = self.index_to_coo(offset)
      return indices

  def replace(self, c, repl):
    for x, y in self.get_occurrences(c):
      self.set_char(x, y, repl)

  def set_char(self, x, y, c):
    if self.check_oob_from_coo(x, y):
      return
    n = self.coo_to_index(x, y)
    self.set_char_from_index(n, c)

  def set_char_from_index(self, n, c):
    self.data[n] = c

  def has_char(self, c):
    return self.count_char(c) > 0

  def get_char_index(self, c):
    return self.data.index(c)

  def count_char(self, c):
    return self.data.count(c)

  def iter_cell(self):
    for n, c in enumerate(self.data):
      yield n, c

  def iter_row(self):
    for n in range(self.height):
      yield n, self.get_row(n)

  def iter_col(self):
    for n in range(self.width):
      yield n, self.get_col(n)

  def pad_once(self):
    for i in range(self.height, -1, -1):
      for j in range(self.width-1, -1, -1):
        self.data.insert(self.width * i, self.empty)
    self.height *= 2
    self.height += 1
    for i in range(self.height, -1, -1):
      for j in range(self.width, -1, -1):
        self.data.insert(self.width * i + j, self.empty)
    self.width *= 2
    self.width += 1
    self.length = self.width * self.height
    self.scale += 1
    return self

  def flood_fill_indices(self, x, y):
    frame = self.__class__('').from_empty(self.width, self.height, ' ')
    search_queue = deque()
    indices = list()
    matrix_view = array('u', ' ')
    frame_view = array('u', ' ')
    curr_char = self.get_cell_from_coo(x, y)
    search_queue.append((x, y))
    while search_queue:
      (x, y) = search_queue.pop()
      indices.append(self.coo_to_index(x, y))
      frame.set_char(x, y, '#')
      for o in (0, 2, 4, 6):
        ss, sc = self._octant_to_cosine_sign(o)
        ix, iy = int(x+sc), int(y+ss)
        self.fetch_line(x, y, matrix_view, o, 1)
        frame.fetch_line(x, y, frame_view, o, 1)
        if not ('#' in frame_view) and curr_char in matrix_view:
          frame.set_char(ix, iy, '#')
          search_queue.append((ix, iy))
    return indices

  def __repr__(self):
    r = ''
    for _, arr in self.iter_row():
      r += arr.tounicode()
      r += '\n'
    return r

class Tree:
  def __init__(self, parent=None):
    self._parent = None
    self._children = list()
    self.set_parent(parent)

  def _assert_subclass(self, o):
    o_is_sub = issubclass(o.__class__, self.__class__)
    s_is_sub = issubclass(self.__class__, o.__class__)
    if not o is None and not (o_is_sub or s_is_sub):
      raise ValueError('object {} is not subclass of {}'.format(o, self))

  def repr(self) -> str:
    return '<{} {}>'.format(
        self.__class__.__name__,
        getattr(self, 'name', hex(id(self)))
    )

  def __repr__(self) -> str:
    return self.repr()

  @property
  def parent(self) -> 'Tree':
    return self._parent

  @parent.setter
  def parent(self, node: 'Tree'):
    self.set_parent(node)

  @property
  def children(self) -> t.List['Tree']:
    return self._children.copy()

  @property
  def rank(self) -> int:
    return len(self._children)

  @property
  def depth(self) -> int:
    c = 0
    for _ in self.iterupstream():
      c += 1
    return c - 1

  @property
  def atindex(self) -> int:
    if self.isroot():
      return -1
    return self._parent._children.index(self)

  def isroot(self) -> bool:
    return self.parent is None

  def isleaf(self) -> bool:
    return self.rank == 0

  def isorphan(self) -> bool:
    return self.isroot() or self.parent.rank == 1

  def isonstart(self) -> bool:
    if self.isroot():
      return False
    return self.atindex == 0

  def isonend(self) -> bool:
    if self.isroot():
      return False
    return self.atindex == (self._parent.rank - 1)

  def iterchildren(self) -> t.Generator['Tree', None, None]:
    yield from self._children

  def iteradjacent(self) -> t.Generator['Tree', None, None]:
    if not self.isroot():
      yield from filter(self.parent.iterchildren(), lambda node: node!=self)

  def iterupstream(self) -> t.Generator['Tree', None, None]:
    p = self
    while not p is None:
      yield p
      p = p.parent

  def iterdownstream(self) -> t.Generator['Tree', None, None]:
    yield self
    for child in self.iterchildren():
      yield from child.iterdownstream()

  def set_parent(self, node: 'Tree') -> 'Tree':
    self._assert_subclass(node)
    previous_parent = self._parent
    if not self.isroot():
      self._parent.remove_child(self)
    self._parent = node
    if not node is None:
      node.append_child(self)
    return previous_parent

  def append_child(self, node: 'Tree'):
    self._assert_subclass(node)
    if node is None:
      raise ValueError('node arg cannot be None')
    if node._parent != self:
      node._parent.remove_child(node)
      node._parent = self
    if node in self._children:
      raise ValueError('{} is already {} child'.format(node, self))
    self._children.append(node)

  def remove_child(self, node: 'Tree'):
    if not node in self._children:
      raise ValueError('{} is not {} child'.format(node, self))
    if not node._parent == self:
      raise ValueError('{} parent is not {}'.format(node, self))
    node._parent = None
    self._children.remove(node)

  def index(self, node: 'Tree'):
    self._assert_subclass(node)
    if not node in self._children:
      raise IndexError('node is not {} child: {}'.format(node, self))
    return self._children.index(node)

  def get_child_by_attr(self, attr, value):
    for c in self._children:
      if not hasattr(c, attr):
        print('warning: object has no attribute')
        continue
      if getattr(attr, c) == value:
        return c

  def __getitem__(self, i):
    if isinstance(i, int):
      return self._children[i]
    elif isinstance(i, slice):
      return tuple(self[i] for i in range(i.start, i.stop, i.step if i.step else 1))
    elif isinstance(i, tuple):
      for j in i:
        return tuple(self[k] for k in j)

  def get_coordinate(self):
    return tuple(reversed(tuple(map(lambda node: node.atindex, filter(lambda node: not node.isroot(), self.iterupstream())))))

  def get_child_from_coordinate(self, c):
    cur = self
    for i in c:
      cur = cur[c]
    return cur

  def get_total_node_count(self):
    c = 0
    for node in self.iterdownstream():
      c += 1
    return c

  def iterreprtree(self, arrowlen=0, maxdepth=99, shownum=False, fill=' '):
    node = self
    total = node.get_total_node_count()
    lstr = '─'
    strnumfmttmp = '[{: >%sd}]'
    arpadfmttmp = '{:%s^%d}'
    arrowlen = max(arrowlen, 0)

    # inode: current node
    # pnode: parent node
    # nnode: next parent node
    for n, inode in enumerate(node.iterdownstream()):
      strnum = ''
      strlen = arrowlen
      if shownum and not inode.isroot():
        c = max(len(str(inode.parent.rank)), 2)
        strnumfmt = strnumfmttmp % c
        arpadfmt = arpadfmttmp % (lstr, max(arrowlen, c+2))
        strnum = strnumfmt.format(inode.atindex)
        arpad = arpadfmt.format(strnum)
        strlen = c + 2
      else:
        arpadfmt = arpadfmttmp % (lstr, max(arrowlen, 0))
        arpad = arpadfmt.format('')
      srpad = fill * strlen

      s = ''
      d = inode.depth
      if d > maxdepth:
        continue
      pnodes = tuple(inode.iterupstream())
      for pnode in reversed(pnodes):
        d -= 1
        nnode = pnodes[max(0, d)]
        if False: pass
        elif pnode == inode:
          continue
        elif d == 0 and pnode.rank > 0 and inode.isonstart() and not inode.isorphan():
          s += '╰┬' + arpad
        elif d == 0 and pnode.rank > 1 and inode.isonend():
          s += fill + '╰' + arpad
        elif d == 0 and pnode.rank > 0 and not (inode.isonstart() or inode.isonend()):
          s += fill + '├' + arpad
        elif d == 0 and inode.isonend():
          s += '╰─' + arpad
        elif nnode.rank > 0 and not nnode.isonend():
          s += fill + '│' + srpad
        else:
          s += fill * 2 + srpad
      if inode.isleaf():
        s += lstr + '●'
      elif inode.depth > maxdepth - 1:
        s += '■'
      else:
        s += '┬○'
      yield inode, s
