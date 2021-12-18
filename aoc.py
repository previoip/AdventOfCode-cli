import argparse, os, re, importlib, json
from inspect import getsourcefile
from importlib import import_module

from utils import fileUtil

def main():

    setYear = 2021
    cfd = os.path.abspath(getsourcefile(lambda:0) + '/..')

    tempComp = {}

    with open(cfd + '/comp.json') as filehandle:
        tempComp = json.load(filehandle)
    
    parser = argparse.ArgumentParser(prog='aoc',
                                    description='A Command Line Interface for managing Advent Of Code. python.'
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
                        help='Run puzzle on specified part. default: part 1'
                        )

    parser.add_argument('-y', 
                        metavar='YEAR',
                        type=int,
                        action='store',
                        default=setYear,
                        help='run specified puzzle script based on year published, default will be the most current year.')

    parser.add_argument('--test',
                        action='store_true',
                        help='Run on test inputs'
                        )

    parser.add_argument('--create',
                       action='store_true',
                       help='create new script instances with from a pre-made boilerplate, if year is not specified it will create instance in most current year.')

    # parser.add_argument('--open',
    #                     action='store_true',
    #                     help='open in text editor on specified day (or latest if not specified). To choose which text editor program, please configure the config.json '
    #                     )

    parser.add_argument('-v',
                       '--verbose',
                       action='store_true',
                       help='not quite ye-verbose-output, but this option enable full outputs printouts.')

    args = parser.parse_args()

    if args.d < 0 or args.y < 0:
        print('Err: arg DAY/YEAR cannot be negative.')
        return

    if not args.y:
        print('Err: arg YEAR is null.')
        return

    if args.y <= 2015 or args.y > 2035:
        print('Err: arg YEAR is probably out of expected bounds. (>2035???)')
        return 
    
    dirScripts = cfd + '/scripts/' + str(args.y)
    dirDatasets = cfd + '/datasets/' + str(args.y)

    if args.create:
        fileUtil.createNewPuzzleInstance(dirScripts, '__init__', 'py')
        fileUtil.createNewPuzzleInstance(dirScripts, 'day', 'py', args.d) # todo: args.d doenst work, fix
        fileUtil.createNewPuzzleInstance(dirDatasets, 'day', 'txt', args.d) # todo: args.d doenst work, fix
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
        pattern = r"(?:(\-\-\-test_)((?:.*?\r?\n?)*)(\-\-\-end))" if args.test else r"(?:(\-\-\-mainData\n)((?:.*?\r?\n?)*)(\-\-\-end))"
        matches = re.finditer(pattern, tempstr, re.MULTILINE)
        tempData = []
        for match in matches:
            tempData.append(match.group(2))

        if not tempData:
            print('no data string is present')
            return

        print('importing and running script...')
        """
        try:
            mod = import_module('scripts.{}.day{}'.format(convArg['y'], convArg['d']))
        except ModuleNotFoundError:
            print('Err: scripts cannot be loaded for some reason')
            return
        """
        mod = import_module('scripts.{}.day{}'.format(convArg['y'], convArg['d']))

        for ind, datum in enumerate(tempData):
            if args.test: print('Running on dataset: %d' % (ind))
            prog = mod.Puzzle(args.verbose)
            prog.appendData(datum.strip())
            prog.run(convArg['p'])
            res = prog.getResult()
            print('\nAnswer: %s' % (res if res else 'returns None, puzzle is not yet completed.'))
    
    if str(convArg['y']) not in tempComp:
        tempComp[str(convArg['y'])] = {}
    if str(convArg['d']) not in tempComp[str(convArg['y'])]:
        tempComp[str(convArg['y'])][str(convArg['d'])] = {}
    if str(convArg['p']) not in tempComp[str(convArg['y'])][str(convArg['d'])]:
        tempComp[str(convArg['y'])][str(convArg['d'])][str(convArg['p'])] = {}

    tempComp[str(convArg['y'])][str(convArg['d'])][str(convArg['p'])] = True if res else False
    
    with open(cfd + '/comp.json', 'w') as filehandle:
        filehandle.write(json.dumps(tempComp, indent=2))
    # print(vars(args))


if __name__ == '__main__':
    main()



