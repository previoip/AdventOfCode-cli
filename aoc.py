import typing as t
import os
import sys
import shutil
import argparse
import importlib.util
import traceback
from importlib import reload as importlib_reload
from datetime import datetime
from re import compile as re_compile
from src.state import AOCStateManager


class AOCConfig:
  class options:
    print_motd = True
    clear_console_each_run = False

  class paths:
    base_folder = './puzzles'
    template_prog_filepath = './src/template_prog'
    template_ds_filepath = './src/template_ds'
    state_filename = './save'
    puzzle_filename = 'puzzle.py'
    test_part1_filename = 'test_p1.txt'
    test_part2_filename = 'test_p2.txt'
    input_part1_filename = 'input_p1.txt'
    input_part2_filename = 'input_p2.txt'
    readme_filename = './readme.md'


class AOCCommandOpt:
  clear   = 'clear'
  help    = 'help'
  test    = 'test'
  stats   = 'stats'
  eval    = 'eval'
  new     = 'new'
  delete  = 'delete'
  update  = 'update'
  exit    = 'exit'

def print_motd(year=0, motdln1='', motdln2=''):
  l = 43
  print()
  print('v', l//3*'=+=', 'v',sep='')
  print('|', 'Advent of Code{}'.format(f' {year}' if year else '').center(l), '|',sep='')
  print('|', '{}'.format(datetime.now()).center(l), '|',sep='')
  if motdln1:
    print('|', '- {} -'.format(motdln1).center(l), '|',sep='')
  if motdln2:
    print('|', '- {} -'.format(motdln2).center(l), '|',sep='')
  print('^', l//3*'=+=', '^',sep='')
  print()

def invoke_confirm(*message) -> bool:
  print()
  if message:
    print(*message)
  ret = input('do you wish to continue [Y/n] ') == 'Y'
  if not ret:
    print('cancelled')
  print()
  return ret

def invoke_argv(substr=''):
  return input('AoC {}$: '.format(substr)).lower().split()

class ErrorCatchingArgumentParser(argparse.ArgumentParser):
  """
  derivation from argparse.ArgumentParser, catches error 
  instead of resolving to sigterm on error.
  """
  def exit(self, status=0, message=None):
    if status:
      raise Exception(f'{message}')

  def error(self, message):
    self.exit(status=2, message='error: %s\n' % message)


class ProgUtil:
  @staticmethod
  def ensure_dir(path) -> bool:
    return os.path.exists(path) and os.path.isdir(path)

  @staticmethod
  def ensure_file(path) -> bool:
    return os.path.exists(path) and os.path.isfile(path)

  @classmethod
  def lazy_import(cls, name, filepath):
    assert cls.ensure_file(filepath)
    spec = importlib.util.spec_from_file_location(name, filepath)
    loader = importlib.util.LazyLoader(spec.loader)
    spec.loader = loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    loader.exec_module(module)
    return module

  @staticmethod
  def force_hot_reload(module_name):
    if module_name in sys.modules:
      importlib_reload(sys.modules.get(module_name))

  @staticmethod
  def clear_console():
    os.system('cls' if os.name=='nt' else 'clear')

  @classmethod
  def update_readme(cls, readme_filepath, content):
    temp = [
      '# Advent of Code cli',
      '',
      'shell-like advent of code puzzle manager written in python with minimal dependency.',
      '',
      '## Stats'
    ]

    if cls.ensure_file(readme_filepath):
      with open(readme_filepath, 'r') as fo:
        temp = fo.read().splitlines()

    tag_index = -1
    if not '## Stats' in temp:
      temp.append(['', '## Stats'])

    tag_index = temp.index('## Stats')
    temp = temp[:tag_index + 1] + ['```', content.strip(), '```']

    with open(readme_filepath, 'w') as fo:
      fo.writelines(list(map(lambda x: x + '\n', temp)))


class AOCArgNamespace:
  def __init__(self):
    self.year: int = 2015
    self.day: int = 1
    self.part: int = 1
    self.flag: str = ''
    self.command: str = AOCCommandOpt.test

  def assert_args(self):
    if not self.year >= 2015:
      raise Exception('year argument is invalid')
    if not (self.day > 0 and args.day <= 31):
      raise Exception('day argument is invalid')

  def to_dirpath(self, base_dir):
    fd = os.path.join(base_dir, 'Year {}'.format(self.year), 'Day {:02}'.format(self.day))
    fd = os.path.realpath(fd)
    return fd

  def __repr__(self):
    return 'year {} day {} part {}'.format(self.year, self.day, self.part)


def parser_build():
  parser = ErrorCatchingArgumentParser(
    prog='aoc.py',
    description='aoc puzzle manager.'
  )
  parser.add_argument('command', choices=[
    AOCCommandOpt.clear,
    AOCCommandOpt.exit,
    AOCCommandOpt.help,
    AOCCommandOpt.stats,
    AOCCommandOpt.new,
    AOCCommandOpt.delete,
    AOCCommandOpt.test,
    AOCCommandOpt.eval,
    AOCCommandOpt.update,
  ])
  parser.add_argument('year', type=int)
  parser.add_argument('day', type=int)
  parser.add_argument('-p', '--part', type=int, dest='part', choices=[1, 2], default=1)
  parser.add_argument('-f', '--flag', type=str, dest='flag', choices=['pass', 'fail', 'null'], default='fail')
  return parser


def program_inits(*args, **kwargs):

  if not ProgUtil.ensure_dir(AOCConfig.paths.base_folder):
    print('creating new folder:', AOCConfig.paths.base_folder)
    os.makedirs(AOCConfig.paths.base_folder)

  state_manager = kwargs.get('state_manager')
  if not state_manager is None:
    if not ProgUtil.ensure_file(AOCConfig.paths.state_filename):
      print('creating new save state:', AOCConfig.paths.state_filename)
      state_manager.save()
    state_manager.load()

  motd = ''
  year = 0
  if state_manager._meta.latest_year:
    year = state_manager._meta.latest_year

  print_motd(year, motd)

def program_defers(*args, **kwargs):
  state_manager = kwargs.get('state_manager')
  if not state_manager is None:
    print('saving latest state')
    state_manager.save()


  print('updating readme')
  ProgUtil.update_readme(AOCConfig.paths.readme_filename, state_manager.stats_repr())

  print('program exits gracefully')


if __name__ == '__main__':
  state_manager = AOCStateManager(AOCConfig.paths.state_filename)

  program_inits(state_manager=state_manager)

  args = AOCArgNamespace()
  parser = parser_build()
  counter = 0

  while True:
    try:
      argv = invoke_argv()

      if not argv:
        continue

      if len(argv) >= 4 and argv[3] != '-p':
        argv = argv[:3] + ['-p'] + argv[3:]

      if len(argv) >= 6 and argv[5] != '-f':
        argv = argv[:5] + ['-f'] + argv[5:]

      if argv[0] == AOCCommandOpt.exit:
        break

      elif argv[0] == AOCCommandOpt.help:
        parser.print_usage()
        continue

      elif argv[0] == AOCCommandOpt.clear:
        ProgUtil.clear_console()
        continue

      elif argv[0] == AOCCommandOpt.stats:
        print(state_manager.stats_repr())
        continue

      if AOCConfig.options.clear_console_each_run:
        ProgUtil.clear_console()

      parser.parse_args(argv, namespace=args)
      args.assert_args()

      if args.command == AOCCommandOpt.update:
        state_manager.update(args.year, args.day, args.part, args.flag)
        print()
        print()
        print(state_manager.stats_repr(args.year))

      if args.command == AOCCommandOpt.new:
        if not invoke_confirm('creating new puzzle:', 'Year {}'.format(args.year), 'Day {}'.format(args.day)):
          continue
        fd = args.to_dirpath(AOCConfig.paths.base_folder)
        if ProgUtil.ensure_dir(fd):
          raise FileExistsError('puzzle already exists:', fd)
        os.makedirs(fd)

        with open(AOCConfig.paths.template_prog_filepath, 'r') as fo:
          with open(os.path.join(fd, AOCConfig.paths.puzzle_filename), 'w', encoding='utf8', newline='\n') as fo2:
            fo2.write(fo.read())
          test_ds_content = fo.read()
        with open(AOCConfig.paths.template_ds_filepath, 'r') as fo:
          test_ds_content = fo.read()
        with open(os.path.join(fd, AOCConfig.paths.input_part1_filename), 'w', encoding='utf8', newline='\n'):
          pass
        with open(os.path.join(fd, AOCConfig.paths.input_part2_filename), 'w', encoding='utf8', newline='\n'):
          pass
        with open(os.path.join(fd, AOCConfig.paths.test_part1_filename), 'w', encoding='utf8', newline='\n') as fo:
          fo.write(test_ds_content)
        with open(os.path.join(fd, AOCConfig.paths.test_part2_filename), 'w', encoding='utf8', newline='\n') as fo:
          fo.write(test_ds_content)

      elif args.command == AOCCommandOpt.test or args.command == AOCCommandOpt.eval:
        fd = args.to_dirpath(AOCConfig.paths.base_folder)
        fp = os.path.join(fd, AOCConfig.paths.puzzle_filename)
        if not ProgUtil.ensure_file(fp):
          raise FileNotFoundError('file not found:', fp)

        ProgUtil.force_hot_reload('src.aoc_base_class')
        ProgUtil.force_hot_reload('src.aoc_input_parser')
        ProgUtil.force_hot_reload('src.state')

        puzzle_module = ProgUtil.lazy_import('aoc', fp)
        puzzle_instance = puzzle_module.AOC(base_dir=fd)

        print()
        for puzzle_name, puzzle_ans, puzzle_solution, puzzle_parser in puzzle_instance._run(run_as=args.command, part=args.part):
          print('evaluating', puzzle_name, args )

          eval_ans = puzzle_solution(puzzle_parser) 

          if args.command == AOCCommandOpt.test:
            puzzle_ans = puzzle_instance.process_test_answer(puzzle_ans)
            if eval_ans == puzzle_ans:
              print('-> test passed')
            else:
              print('-> try again, expected result:')
              print(puzzle_ans)

          print('-> result: {}'.format(eval_ans))
          print()

        del puzzle_instance
        del puzzle_module

      elif args.command == AOCCommandOpt.delete:
        if not invoke_confirm('deleting puzzle:', 'Year {}'.format(args.year), 'Day {}'.format(args.day)):
          continue
        fd = args.to_dirpath(AOCConfig.paths.base_folder)
        if not ProgUtil.ensure_dir(fd):
          raise FileNotFoundError('puzzle does not exist:', fd)
        shutil.rmtree(fd)

    except Exception as e:
      print('', traceback.format_exc(), '', sep='\n')
      continue
      
    counter += 1

  program_defers(state_manager=state_manager)