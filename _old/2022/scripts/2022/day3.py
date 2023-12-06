lowerRange = [ord('a'), ord('z')+1]
upperRange = [ord('A'), ord('Z')+1]
charRange = [chr(j) for lower, upper in (lowerRange, upperRange) for j in range(lower, upper)]

def getCharScore(char):
    if char in charRange:
        return charRange.index(char) + 1
    return 0

def getDupes(str1, str2):
    d = ''
    for i in str1:
        if i in str2 and i not in d:
            d += i
    return d


class Puzzle:

    # main funcs
    def part1(self):
        score = 0
        for i in self.data:
            assert len(i)%2 == 0
            l = len(i) // 2
            compartment1, compartment2 = i[:-l], i[l:]
            dupe = getDupes(compartment1, compartment2)[0]
            score += getCharScore(dupe)
        return score

    def part2(self):
        score = 0
        data_chunks = [self.data[i:i+3] for i in range(0, len(self.data), 3)]
        for chunk in data_chunks:
            chunk_dupe = getDupes(chunk[1], chunk[0])
            chunk_dupe = getDupes(chunk_dupe, chunk[2])
            score += getCharScore(chunk_dupe)
        return score


    def appendData(self, data):
        self.data = data.splitlines()

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