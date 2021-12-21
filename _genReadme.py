
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
            cols = int(len(compDict[year])/10)+1
            table += ' '.join(["| Day  | Stars |" for _ in range(cols)])
            table += "\n"
            table += '-'.join(["| :-:  | :---: |" for _ in range(cols)])
            table += "\n"
            for i in range(1, 11):
                # table += "| %s  | %s%s |\n" % (day, ' *' if compDict[year][str(day)]['1'] else '  ', '* ' if compDict[year][str(day)]['2'] else '  ')
                row = []
                for j in range(cols):
                    index = i + (10*j)

                    if index > 25:
                        row.append( "|      |       |" )
                    else:
                        temp = '|  %s%s  |  ' % (index, '' if index>=10 else ' ')
                        try:
                            part1 = compDict[year][str(index)]['1']
                            temp += '%s' % ('*' if part1 else ' ')
                        except KeyError:
                            temp += ' '

                        try:
                            part2 = compDict[year][str(index)]['2']
                            temp += '%s' % ('*' if part2 else ' ')
                        except KeyError:
                            temp += ' '
                        temp += '   |'

                        row.append(temp)
                    # try:
                    #     (part1, part2) = (compDict[year][str(index)]['1'], compDict[year][str(index)]['2'])
                    #     row.append( "| %s  | %s%s |" % (index, ' *' if part1 else '  ', '* ' if part2 else '  '))
                    # except KeyError:
                    #     row.append( "|     |     |" )
                    #     pass
                table += ' '.join(row)
                table += "\n"
            table += "\n"

    fileHandle('README.md', 'w', readme_template + table)

if __name__ == "__main__":
    main()