class Puzzle:

    def floor(num):
        if num == int(num): return num
        else: return int(num)

    def ceil(num):
        if num == int(num): return num
        else: return int(num)+1


    class Syntax:
        def __init__(self, chunkString):
            self.data = [i for i in chunkString]
            self.incompleteData = []
            self.errorScore = 0
            self.autoCompleteScore = 0
            self.chunks = [i for i in chunkString]
            self.chars = {'st': ['(','[','{','<'], 'en':[')',']','}','>']}
            self.illegalCharScore = {
                self.chars['en'][0]: 3,
                self.chars['en'][1]: 57,
                self.chars['en'][2]: 1197,
                self.chars['en'][3]: 25137
            }
            self.legalCharScore = {
                self.chars['en'][0]: 1,
                self.chars['en'][1]: 2,
                self.chars['en'][2]: 3,
                self.chars['en'][3]: 4
            }

            self.enclosingDict = {
                '{':'}',
                '[':']',
                '<':'>',
                '(':')',
            }

        def checkIfEnclosed(self, firstEl, secondEl):
            return bool(firstEl == secondEl)

        def beginIterChunk(self):
            for di, i in enumerate(self.data):
                while True:
                    temp = ''
                    for dItem, item in enumerate(i):
                        isEncloseStr = False
                        isCorrectStr = False
                        if item in self.chars['st']:
                            temp = item
                            print(temp)
                    break
        
        def removeEnclosed(self):
            enclosedChar = [i+self.enclosingDict[i] for i in self.chars['st']]
            for dItem, item in enumerate(self.data):
                temp = item
                before = temp
                after = ''
                exitLoop = False
                while not exitLoop:
                    after = before
                    for deter in enclosedChar:
                        after = after.replace(deter, '')
                    if(before == after): exitLoop = True
                    before = after
                self.data[dItem] = after
            return self.data

        def evalSyntaxError(self):
            for line in self.data:
                cur = 0
                for index, item in enumerate(line):
                    if item in self.chars['st'] and line[(index + 1) % len(line)] in self.chars['en']:
                        # print(item, line[(index + 1) % len(line)])
                        cur += self.illegalCharScore[line[(index + 1) % len(line)]]
                self.errorScore += cur
                if cur == 0:
                    self.incompleteData.append(line)

        def evalIncompleteData(self):
            scores= []
            for i in self.incompleteData:
                score = 0
                for char in reversed(i):
                    score = score * 5
                    score += self.legalCharScore[self.enclosingDict[char]]
                    # followups += self.enclosingDict[char]
                scores.append(score)
            # scores.append(288957)
            scores = sorted(scores)
            # print(scores)
            scoresLenght = len(scores)
            if not scoresLenght % 2:
                # upper = ceil(scoresLenght/2) - 1
                # lower = floor(scoresLenght/2) - 1
                # mid = scores[upper] + scores[lower] / 2
                # print(mid)
                print('even number lmao')
                return None
            else:
                return scores[round(scoresLenght/2)]

        def dump(self):
            # print(self.data)
            return self.errorScore

    # main funcs
    def part1(self):
        syn = self.Syntax(self.data)
        print(syn.removeEnclosed())
        syn.evalSyntaxError()
        return syn.dump()

    def part2(self):
        syn = self.Syntax(self.data)
        syn.removeEnclosed()
        syn.evalSyntaxError()
        return syn.evalIncompleteData()

    def appendData(self, data):
        self.data = data.splitlines()

    def dump(self):
        print('Dumping result')
        print(self.data)
        print(self.result)
        return

    # defaults
    def __init__(self, verbose):
        self.data = None
        self.cache = None
        self.verbose = verbose

    def run(self, part):
        if part == 1:
            self.result = self.part1()
        else:
            self.result = self.part2()

        if self.verbose:
            self.dump()

    def getResult(self):
        return self.result

if __name__ == "__main__":
    print("this shouldn't be ran as standalone script")
    pass