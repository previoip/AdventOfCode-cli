class Puzzle:

    def __init__(self, verbose):
        self.data = None
        self.cache = None
        self.verbose = verbose

    def appendData(self, data):
        self.data = [int(i) for i in data.splitlines()]

    def part1(self):
        array = ''
        temp = [0, 0]
        count = 0

        
        for i in self.data:
            temp[1] = temp[0]
            temp[0] = int(i)
            if(temp[1] < temp[0]):
                count += 1

        return count - 1

    def part2(self):
        array = self.data
        temp = [0, 0]
        count = 0
        
        for index in range(len(array)-2):
            temp[1] = temp[0]
            temp[0] = int(array[index]) + int(array[index+1]) + int(array[index+2])
            if(temp[1] < temp[0]):
                count += 1

        return count - 1
        return None

    def run(self, part):
        if part == 1:
            self.result = self.part1()
        else:
            self.result = self.part2()

        if self.verbose:
            self.dump()

    def dump(self):
        print('Dumping')
        print(', '.join([str(i) for i in self.data[:10]]) + ', ...')

    def getResult(self):
        return self.result

if __name__ == "__main__":
    print('no')