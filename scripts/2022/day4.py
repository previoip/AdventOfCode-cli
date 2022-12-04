def parseID(i):
    return [[int(k) for k in j.split('-')] for j in i.split(',')]

def rangeToBinary(r):
    t = ['0']*max(r)
    for i in range(r[0]-1, r[1]):
        t[i] = '1'
    return int(''.join(reversed(t)), 2)

class Puzzle:

    def part1(self):
        score = 0
        for i in self.data:
            group1, group2 = parseID(i)
            groupsAsBin = [rangeToBinary(group1), rangeToBinary(group2)]
            if rangeToBinary(group1) & rangeToBinary(group2) in groupsAsBin:
                score += 1
        return score

    def part2(self):
        score = 0
        for i in self.data:
            group1, group2 = parseID(i)
            if rangeToBinary(group1) & rangeToBinary(group2):
                score += 1
        return score

    def appendData(self, data):
        # data preprocessor
        self.data = data.splitlines()
        print(self.data)

    # defaults
    def __init__(self, verbose):
        self.data = None
        self.cache = None
        self.verbose = verbose

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