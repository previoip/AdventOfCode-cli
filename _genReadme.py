
def fileHandle(path, mode, stdin=None):
    temp_ = ''

    if mode == 'r':
        with open(path, 'r') as filehandle:
            temp_ = filehandle.read()
            filehandle.close()

    elif mode == 'w':
        if not stdin:
            return
        with open(path, 'w') as filehandle:
            filehandle.write(stdin)

    return temp_

def main():
    import json
    
    readme_template = fileHandle('temp_README.md', 'r')
    
    compDict = fileHandle('comp.json', 'r')
    table = '\n\n### Stats'
    compDict = json.loads(compDict)
    for year in compDict:
        if year != "_name":
            table += "\n\n#### %s \n\n" % (str(year))
            table += "| Days  | Stars |\n"
            table += "| ----  | ----- |\n"
            for day in compDict[year]:
                if day != "_name":
                    table += "| %s  | %s%s |\n" % (day, ' *' if compDict[year][day]['1'] else '  ', '* ' if compDict[year][day]['2'] else '  ')

    fileHandle('README.md', 'w', readme_template + table)

if __name__ == "__main__":
    main()