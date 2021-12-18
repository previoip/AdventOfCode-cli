class Puzzle:
    class Snails:
        def __init__(self, snailCollection):
            self.snailCollection = snailCollection

        def addItem(self, snailList):
            self.snailCollection = [self.snailCollection, snailList]

        def getRes(self):
            return self.snailCollection
    
    # main funcs
    def part1(self):
        snails = self.Snails([1,2])
        snails.addItem([3,4])
        return snails.getRes()

    def part2(self):
        return None

    def appendData(self, data):
        import ast
        temp = []
        for item in [data.splitlines()[0]]:
            temp.append(ast.literal_eval(item))
            
        self.data = temp
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