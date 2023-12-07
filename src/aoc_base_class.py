import unittest
import typing as t
import os.path
import functools
from io import IOBase, BytesIO
from os import PathLike
from re import compile as re_compile

_re_test_tag_fetch = re_compile(rb'\[(Test|Ans).*\]\B\n')

class AOCRunAsEnum:
  eval = 'eval'
  test = 'test'

class AOCBaseClass:
  def __init__(self, base_dir='.'):
    self._base_dir = base_dir
    self.eval_path_part_1 = 'input_p1.txt'
    self.eval_path_part_2 = 'input_p2.txt'
    self.test_path_part_1 = 'test_p1.txt'
    self.test_path_part_2 = 'test_p2.txt'
    self.default_encoding = 'utf8'

  def loader(self, part=1, run_as:AOCRunAsEnum=AOCRunAsEnum.test, *args, **kwargs) -> IOBase:
    path = getattr(self, '{}_path_part_{}'.format(run_as, part), None)
    if path is None:
      raise Exception('path does not resolve to valid PathLike string: {}'.format(path))
    return self.file_loader(os.path.join(self._base_dir, path))

  def file_loader(self, path: PathLike) -> IOBase:
    with open(path, 'rb') as fo:
      return BytesIO(fo.read())

  def tests_unloader(self, buf: IOBase) -> t.Generator[t.Iterator[t.Tuple[str, IOBase]], None, None]:
    bytes_all = buf.read()
    tag_matches_it = _re_test_tag_fetch.finditer(bytes_all)
    tag_matches = list(tag_matches_it)
    count = len(tag_matches)

    for n, match in enumerate(tag_matches):
      start_cursor, end_cursor = match.span()
      tag = bytes_all[start_cursor:end_cursor].decode(self.default_encoding).strip()
      if n + 1 == count:
        bytes_content = bytes_all[end_cursor:]
      else:
        next_match = tag_matches[n+1]
        next_cursor = next_match.span()[0]
        bytes_content = bytes_all[end_cursor:next_cursor]
      yield (tag, BytesIO(bytes_content))

  def parser(self, buf_io: IOBase) -> t.Any:
    raise NotImplementedError('data parser is not yet implemented')

  def parser_part_1(self, buf_io: IOBase) -> t.Any:
    return self.parser(buf_io)

  def parser_part_2(self, buf_io: IOBase) -> t.Any:
    return self.parser(buf_io)

  def solution_part_1(self, parsed_input) -> t.Any:
    raise NotImplementedError('puzzle part 1 is not yet implemented')

  def solution_part_2(self, parsed_input) -> t.Any:
    raise NotImplementedError('puzzle part 2 is not yet implemented')

  def _run(self, run_as:AOCRunAsEnum=AOCRunAsEnum.test, part=1) -> t.Generator[t.Tuple[str, str, t.Callable, t.Callable], None, None]:
    if not (run_as != AOCRunAsEnum.eval or run_as != AOCRunAsEnum.test):
      raise ValueError('run_as arg is invalid: {}'.format(run_as))
    callable_sol = getattr(self, 'solution_part_{}'.format(part), None)
    if callable_sol is None:
      raise Exception('invalid part arg: {}'.format(part))
    
    callable_parser = getattr(self, 'parser_part_{}'.format(part), None)
    if callable_parser is None:
      raise Exception('invalid part arg: {}'.format(part))

    buf = self.loader(part=part, run_as=run_as)


    if run_as == AOCRunAsEnum.eval:
      yield 'eval', None, callable_sol, callable_parser(buf)

    elif run_as == AOCRunAsEnum.test:
      test_it = list(self.tests_unloader(buf))
      ans = None
      for test_name, trunc_buf in test_it:
        if test_name == '[Ans]':
          ans = trunc_buf
          continue
        yield test_name, ans, callable_sol, callable_parser(trunc_buf)
        ans = None