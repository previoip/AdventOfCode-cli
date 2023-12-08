import re

class AOCInputParser:

  regexp_tags = re.compile(
    rb'^\>\>(ans).*?\:\ *?\n(.*?)\n?^\>\>(inp).*?\:\ *?\n(.*?)\n?^\<\<end\!',
    re.MULTILINE | re.DOTALL
  )

  @classmethod
  def get_matches(cls, b):
    for match in cls.regexp_tags.finditer(b):
      _, ans, _, inp = match.groups()
      yield ans, inp

  @classmethod
  def get_matches_from_iostream(cls, fo):
    yield from cls.get_matches(fo.read())
