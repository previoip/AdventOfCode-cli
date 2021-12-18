class Puzzle:

    # main funcs
    def part1(self):
        maxPos = max(self.data)
        minPos = min(self.data)
        print(minPos, maxPos)
        fuelCosts = 0
        fuelCost = 0
        lowest = 1e19
        for est in range(minPos, maxPos):
            for currentPos in self.data:
                currentCost = 0
                for i in range(abs(est - currentPos)):
                    currentCost += 1
                print(currentCost)
                fuelCosts += currentCost
            if(fuelCost < lowest):
                lowest = fuelCost
            fuelCosts = 0
        return lowest

    def part2(self):
        return None

    def appendData(self, data):
        self.data = [int(i) for i in data.split(',')]

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