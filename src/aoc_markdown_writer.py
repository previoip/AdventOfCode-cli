class AOCMarkdownWriter:
  markdown_path: str = ''
  
  def __init__(self):
    self.temp = []
    self.tag_index = -1
    self.tag = '# Stats'

  def scan(self):
    if not self.tag in self.temp:
      self.tag_index = len(self.temp)
      return
    return self.temp.index(self.tag)

  def read(cls):
    with open(cls.markdown_path, 'r') as fo:
      self.temp.extend(fo.read().splitlines())
    