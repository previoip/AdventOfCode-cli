class Puzzle:

    class DriacDice:

        class Player:
            def __init__(self, name):
                self.name = name
                self.pos = 0
                self.score = 0
            
            def move(self, incr):
                self.pos += incr
                self.pos = self.pos if self.pos<=10 else self.pos%10
            def addScore(self, score):
                self.score += score

        def __init__(self):
            self.board = [i for i in range(1,11)]
            self.player = {'1': self.Player('1'), '2': self.Player('2')}
            self.currIndex = 0
            self.rollCount = 0

        def getScores(self):
            return (self.player['1'].score, self.player['2'].score)

        def rollDice(self, jump=3):
            diceSum = 0
            curr = self.currIndex
            for i in range(jump):
                diceSum += self.board[(curr + i)%len(self.board)]
            self.currIndex += jump
            self.rollCount += 1
            return diceSum


    # main funcs
    def part1(self):
        game = self.DriacDice()
        (game.player['1'].pos, game.player['2'].pos) = (self.data['p1'], self.data['p2'])

        while True:
            inc = game.rollDice()
            game.player['1'].move(inc)
            score = game.player['1'].pos
            game.player['1'].addScore(score)
            if 1000 <= max(game.getScores()):
                break

            inc = game.rollDice()
            game.player['2'].move(inc)
            score = game.player['2'].pos
            game.player['2'].addScore(score)
            if 1000 <= max(game.getScores()):
                break

        finalScore = game.getScores()
        finalDiceIndex = game.currIndex
        return min(finalScore) * finalDiceIndex

    def part2(self):
        return None

    def appendData(self, data):
        temp = data.splitlines()
        self.data = {
            'p1': int(temp[0][28:]),
            'p2': int(temp[1][28:])
            }

    def dump(self):
        print('Dumping...')
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