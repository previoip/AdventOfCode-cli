
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



