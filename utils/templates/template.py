class Puzzle:

    def part1(self):
        return None

    def part2(self):
        return None

    def appendData(self, data):
        # data preprocessor
        self.data = data.splitlines()

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

    def dump(self):
        print('Dumping...')
        print(self.data)
        print(self.result)
        return

    def getResult(self):
        return self.result

if __name__ == "__main__":
    pass