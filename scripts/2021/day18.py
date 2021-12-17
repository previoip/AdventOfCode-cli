class Puzzle:

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