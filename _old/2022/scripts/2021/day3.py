class Puzzle:
    class Diagnostics:
        def __init__(self):
            self.binaryContainer = []
            self.binaryCount = []
            self.cache = []

        def insertBinaryString(self, binString):
            self.binaryContainer.append(binString)

        def evalBinCount(self, onIndex):
            temp = {'0': 0, '1': 0}
            for i in self.cache:
                if i[onIndex] == '1':
                    temp['1'] += 1
                else:
                    temp['0'] += 1
            return temp
        
        def begin(self):
            self.cache = self.binaryContainer.copy()

        def removeBasedOnValOnIndex(self, value, indexOffset):
            if len(self.cache) == 1: return False
            tempIndices = []
            for i in self.cache:
                if value == i[indexOffset]:
                    itemp = self.cache[self.cache.index(i)]
                    if itemp not in tempIndices:
                        tempIndices.append(itemp)
            for item in tempIndices:
                try:
                    self.cache.remove(item)
                except ValueError:
                    pass
            return True

    # main funcs
    def part1(self):
        return None

    def part2(self):
        return None

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