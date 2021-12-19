import os, json, re
from inspect import getsourcefile
from importlib import import_module

def directEval(year, day, part):
    tempComp = {}
    cfd = os.path.abspath(getsourcefile(lambda:0) + '/..')

    with open(cfd + '/comp.json') as filehandle:
        tempComp = json.load(filehandle)

    tempstr = ''
    with open(cfd + '/datasets/' + str(year) + '/day' + str(day) + '.txt', 'r') as filehandle:
        tempstr = filehandle.read()
        filehandle.close()
    pattern = r"(?:(\-\-\-mainData\n)((?:.*?\r?\n?)*)(\-\-\-end))"
    matches = re.finditer(pattern, tempstr, re.MULTILINE)
    tempData = []
    for match in matches:
        tempData.append(match.group(2))

    if not tempData:
        return

    mod = import_module('scripts.{}.day{}'.format(year, day))

    for ind, datum in enumerate(tempData):
        prog = mod.Puzzle(False)
        prog.appendData(datum.strip())
        prog.run(part)
        res = prog.getResult()

    if str(year) not in tempComp:
        tempComp["_name"] = "year"
        tempComp[str(year)] = {}
    if str(day) not in tempComp[str(year)]:
        tempComp[str(year)]["_name"] = "day"
        tempComp[str(year)][str(day)] = {}

    tempComp[str(year)][str(day)]["_name"] = "part"
    tempComp[str(year)][str(day)][str(part)] = True if res else False
    
    with open(cfd + '/comp.json', 'w') as filehandle:
        filehandle.write(json.dumps(tempComp, indent=2))

def main():
    cfd = os.path.abspath(getsourcefile(lambda:0) + '/..')


    with open(cfd + '/comp.json') as filehandle:
        tempComp = json.load(filehandle)
    

    dirDef = cfd + '/scripts/'
    listYear = os.listdir(dirDef)

    for year in listYear:
        dirScripts = cfd + '/scripts/' + str(year)
        exclude = ['__pycache__', '__init__.py']
        listScripts = sorted([i for i in os.listdir(dirScripts) if i not in exclude])
        # python_exec = 'py'
        for day, scr in enumerate(listScripts):
            # temp = '%s aoc.py -y %s -d %s -p %s' % (python_exec, year, day+1, 1)
            directEval(year, day+1, 1)
            directEval(year, day+1, 2)
    
if __name__ == '__main__':
    main()