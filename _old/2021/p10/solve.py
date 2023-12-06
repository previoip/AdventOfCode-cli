import os

def getData(path):
    array = []
    with open(path, 'r') as filehandle:
        array = filehandle.read().splitlines()
        filehandle.close()
    return array
def floor(flo):
    if flo == int(flo): return flo
    else: return int(flo)

def ceil(flo):
    if flo == int(flo): return flo
    else: return int(flo)+1

class Syntax:
    def __init__(self, chunkString):
        self.data = []
        self.incompleteData = []
        self.errorScore = 0
        self.autoCompleteScore = 0
        self.chunks = [i for i in chunkString]
        self.testChunk = [
            '[({(<(())[]>[[{[]{<()<>>',
            '[(()[<>])]({[<{<<[]>>(',
            '{([(<{}[<>[]}>{[]{[(<()>',
            '(((({<>}<{<{<>}{[]{[]{}',
            '[[<[([]))<([[{}[[()]]]',
            '[{[{({}]{}}([{[{{{}}([]',
            '{<[[]]>}<{[{[{[]{()[[[]',
            '[<(<(<(<{}))><([]([]()',
            '<{([([[(<>()){}]>(<<{{',
            '<{([{{}}[<[[[<>{}]]]>[]]'
        ]
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

    def isTest(self, test = True):
        if test: self.data = self.testChunk 
        else: self.data = self.chunks
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

    def evalSyntaxError(self):
        for line in self.data:
            cur = 0
            for index, item in enumerate(line):
                if item in self.chars['st'] and line[(index + 1) % len(line)] in self.chars['en']:
                    # print(item, line[(index + 1) % len(line)])
                    cur += self.illegalCharScore[line[(index + 1) % len(line)]]
            self.errorScore = cur
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
        print(scores)
        scoresLenght = len(scores)
        if not scoresLenght % 2:
            # upper = ceil(scoresLenght/2) - 1
            # lower = floor(scoresLenght/2) - 1
            # mid = scores[upper] + scores[lower] / 2
            # print(mid)
            print('even number lmao')
        else:
            print(scores[round(scoresLenght/2)])

    def dump(self):
        print(self.data)
        print(self.errorScore)


def main():
    syn = Syntax(getData(os.getcwd() + '/p10/data.txt'))
    syn.isTest(False)
    syn.removeEnclosed()
    syn.evalSyntaxError()
    syn.dump()
    syn.evalIncompleteData()

if __name__ == "__main__":
    main()