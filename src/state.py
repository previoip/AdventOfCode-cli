from io import BytesIO

class _AOCStateFrag:
  @classmethod
  def unload(cls, fo):
    return fo.read(cls.length_bytes)

class AOCMeta(_AOCStateFrag):
  length_bytes = 4 + 8 + 8 + 2 + 2 + 4
  def __init__(self):
    self.signature: bytes
    self.total_length: int
    self.crc: bytes
    self.version: int 
    self.latest_year: int 
    self.num_entries: int 

class AOCYearEntry(_AOCStateFrag):
  length_bytes = 2 + 3 + 3
  def __init__(self):
    self.year: int
    self.offset: int
    self.length: int

class AOCEntry(_AOCStateFrag):
  length_bytes = 1
  def __init__(self):
    self.day: int
    self.state: int


class AOCStateManager:
  endian = 'little'
  signature = b'\x42\x00\x69\x69'

  def __init__(self, filepath):
    self.filepath = filepath
    self.buf = BytesIO()

  def load(self):
    with open(self.filepath, 'rb') as fo:
      b = fo.read()
      ret = self.buf.write(b)
    self.buf.seek(0)
    return ret

  def save(self):
    self.buf.seek(len(self.signature))
    with open(self.filepath, 'wb') as fo:
      fo.writelines([self.buf.read(), b'\x00'])

