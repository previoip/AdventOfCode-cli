class Puzzle:

    class BingoBoard:
        def __init__(self, boardStringList, sequenceList):
            # print(boardStringList)
            self.sequence = sequenceList
            self.sequenceIterationCount = 0
            self.board = self.generateBoard(boardStringList)
            self.score = 0
            
        def generateBoard(self, stringList):
            temp = []
            temp_board = []
            for row in stringList:
                temp_row = row.split(' ')
                for num in temp_row:
                    if num:
                        temp.append([int(num), False])
                temp_board.append(temp)
                temp = []
            return temp_board        

        def iterateSequence(self):
            # seq = self.sequence
            index = 0
            while True:
                num = int(self.sequence[index])
                self.lastSequence = num
                index += 1
                for rowId, row in enumerate(self.board):
                    for itemId, item in enumerate(row):
                        if item[0] == num:
                            self.board[rowId][itemId][1] = True
                            if self.checkBingo():
                                self.sequenceIterationCount = index
                                return
                if(index >= len(self.sequence)):
                    break
                
        def evalScore(self):
            numlist = []
            for row in self.board:
                for item in row:
                    if item[1] == False:
                        numlist.append(item[0])
            self.score = sum(numlist) * self.lastSequence
        

        def checkBingo(self):
            for row in self.board:
                checkRow = all([i[1] for i in row])
                if checkRow:
                    self.evalScore()
                    return True
            for colId in range(len(self.board[0])):
                column = []
                for item in self.board:
                    column.append(item[colId][1])
                if all(column):
                    self.evalScore()
                    return True
            return False

        def getScore(self):
            return self.score

        def getCount(self):
            return self.sequenceIterationCount
        
        def dump(self):
            print('Bingo Sequence: {}'.format('-'.join(self.sequence)))
            print('Board:')
            for row in self.board:
                # print(' '.join([ (str(i[0]) + ' ' + ('O' if i[1] else 'X') + ' ') for i in row]))
                print(' '.join([ '|{}| {}\t'.format('X' if i[1] else ' ', i[0]) for i in row]))
            print('Score: {}'.format(self.score))
        
    # main funcs
    def part1(self):
        data = self.data
        sequence = data[0].split(',')
        data.pop(0)
        data.pop(0) # no

        # seperate board list from newline terminator 
        temp = []
        boardList = []
        for item in data:
            if item:
                temp.append(item) 
            else:
                boardList.append(temp)
                temp = []

        temp_score = []
        temp_iterCount = []
        for i in boardList:
            # print(' | ' .join(i))
            bingus = self.BingoBoard(i, sequence)
            bingus.iterateSequence()
            temp_score.append(bingus.getScore())
            temp_iterCount.append(bingus.getCount())
        
        # just for kicks
        biggestBingo = self.BingoBoard(boardList[temp_score.index(max(temp_score))], sequence)
        latestBingo = self.BingoBoard(boardList[temp_iterCount.index(max(temp_iterCount))], sequence)
        
        biggestBingo.iterateSequence()
        print('Biggest Score')
        biggestBingo.dump()
        latestBingo.iterateSequence()
        print('Latest win')
        latestBingo.dump()
        return 'up'

    def part2(self):
        return 'Answer is also on part 1'

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