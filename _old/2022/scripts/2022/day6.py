class PacketDeque:
    def __init__(self, length):
        self.deque = ['+']*length

    def put(self, i):
        self.deque.append(i)
        return self.deque.pop(0)

    def __repr__(self):
        return '[' + ' '.join(self.deque) + ']'

    def checkDupes(self):
        d = list(self.deque)
        while d:
            a = d.pop()
            if '+' not in d and a in d:
                return True
        return False

class Puzzle:

    def part1(self):
        deque = PacketDeque(4)
        for n, c in enumerate(self.data):
            deque.put(c)
            if self.verbose: print(n, deque.checkDupes(), deque)
            if n > 3 and not deque.checkDupes():
                return n + 1
        return 0

    def part2(self):
        deque = PacketDeque(14)
        for n, c in enumerate(self.data):
            deque.put(c)
            if self.verbose: print(n, deque.checkDupes(), deque)
            if n > 13 and not deque.checkDupes():
                return n + 1
        return 0

    def appendData(self, data):
        # data preprocessor
        self.data = data.strip()

    # defaults
    def __init__(self, verbose):
        self.data = None
        self.cache = None
        self.verbose = verbose
        self.stripData = True

    def run(self, part):
        if part == 2:
            self.result = self.part2()
        else:
            self.result = self.part1()

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