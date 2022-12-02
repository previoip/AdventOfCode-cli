class Puzzle:

    # main funcs
    def part1(self):
        t = [0]
        for i in self.data:
            if not i:
                t.append(0)
            else:
                t[-1] += i
        t.pop(-1)
        return max(t)

    def part2(self):
        t = [0]
        for i in self.data:
            if not i:
                t.append(0)
            else:
                t[-1] += i
        t.pop(-1)

        s = []

        for _ in range(3):
            idx = t.index(max(t))
            s.append(t.pop(idx))

        return sum(s)

    def appendData(self, data):
        self.data = data.splitlines()
        self.data = [int(i) if i else None for i in self.data]

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