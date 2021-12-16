import argparse, os, re, importlib
from inspect import getsourcefile
from importlib import import_module

from utils import fileUtil

def main():

    setYear = 2021
    cfd = os.path.abspath(getsourcefile(lambda:0) + '/..')

    parser = argparse.ArgumentParser(prog='aoc',
                                    description='A Command Line Interface for AOC Scripts bootstrapper-ish'
                                    )

    parser.add_argument('-d',
                        metavar='DAY',
                        type=int,
                        default=0,
                        help='Run puzzle on specified day (int), if not specified, this will run latest entry.'
                        )

    parser.add_argument('-p',
                        type=int,
                        action='store',
                        default=1,
                        choices=[1,2],
                        help='Run puzzle on specified part'
                        )

    parser.add_argument('-t', '--test',
                        action='store_true',
                        help='Run on test inputs'
                        )

    parser.add_argument('-y', 
                        metavar='YEAR',
                        type=int,
                        action='store',
                        default=setYear,
                        help='run specified puzzle script based on year published, default will be the most current year.')

    parser.add_argument('-c', '--create',
                       action='store_true',
                       help='create new script instances with this program boilerplate, if year is not specified it will create instance in latest event')

    parser.add_argument('-v',
                       '--verbose',
                       action='store_true',
                       help='not quite the verbose you might expect, but it\'ll show full outputs of the script.')

    args = parser.parse_args()

    if args.d < 0:
        print('Err: arg DAY cannot be negative.')
        return

    if not args.y:
        print('Err: arg YEAR is null.')
        return

    if args.y <= 2015 or args.y > 2035:
        print('Err: arg YEAR is probably out of expected bounds.')
        return 
    
    dirScripts = cfd + '/scripts/' + str(args.y)
    dirDatasets = cfd + '/datasets/' + str(args.y)

    if args.create:
        fileUtil.createNewPuzzleInstance(dirScripts, '__init__', 'py')
        fileUtil.createNewPuzzleInstance(dirScripts, 'day', 'py')
        fileUtil.createNewPuzzleInstance(dirDatasets, 'day', 'txt')
        return

    else:
        listScripts = sorted([i for i in os.listdir(dirScripts) if i != '__pycache__'])
        listDatasets = sorted(os.listdir(dirDatasets))

        if len(listDatasets) <= 0 and len(listScripts) <= 1:
            print('no script/dataset present')
            return

        # print(listDatasets, listScripts)
        # print(len(listDatasets), len(listScripts))

        convArg = {'y': args.y, 'd': args.d if args.d > 0 else len(listScripts)-1, 'p': args.p, 't': args.test}
        

        if len(listDatasets) < convArg['d'] or len(listScripts) <= convArg['d']:
            print('no script/dataset found in corresponding folder')
            return

        currPath = {'script': listScripts.pop(convArg['d']), 'data': listDatasets.pop(convArg['d']-1)}


        print('\n----- Advent Of Code %s, Day %d part %d %s-----\n' % (convArg['y'], convArg['d'], convArg['p'], 'using test variable. ' if convArg['t'] else ''))
        # print(convArg)
        # print(currPath)
        
        ## main func
        print('fetching local data...')
        tempstr = ''
        with open(cfd + '/datasets/' + str(args.y) + '/day' + str(convArg['d']) + '.txt', 'r') as filehandle:
            tempstr = filehandle.read()
            filehandle.close()
        pattern = r"(?:(\-\-\-test\:\n)((?:.*?\r?\n?)*)(\-\-\-data:))" if args.test else r"(?:(\-\-\-data\:\n)((?:.*?\r?\n?)*)(\-\-\-end))"
        matches = re.finditer(pattern, tempstr, re.MULTILINE)
        tempstr = ''
        for match in matches:
            tempstr += match.group(2)

        if not tempstr:
            print('no data is present in txt')
            return

        print('importing and running script...')
        try:
            mod = import_module('scripts.{}.day{}'.format(convArg['y'], convArg['d']))
        except ModuleNotFoundError:
            print('Err: scripts cannot be loaded for some reason')
            return

        prog = mod.Puzzle(args.verbose)
        prog.appendData(tempstr)
        prog.run(convArg['p'])
        print('Answer: %s' % (prog.getResult()))


    # print(vars(args))


if __name__ == '__main__':
    main()



