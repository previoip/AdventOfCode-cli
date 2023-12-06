class Puzzle:

    class LanterFish:
        def __init__(self, series, maxDays):
            self.initSeries = series
            self.maxDays = maxDays
            self.cache = []
            # self.total = len(self.initSeries)
            self.total = 0

        def iterSelf(self):
            lenght = len(self.initSeries)
            for ind, i in enumerate(self.initSeries):
                arr = [i]
                for _ in range(self.maxDays):
                    for i, a in enumerate(arr):
                        temp = arr[i] - 1
                        if temp < 0:
                            arr[i] = 6
                            arr.append(9)
                        else:
                            arr[i] = temp
                self.total += len(arr)
                print('index:{}/{} -> {}'.format(ind+1, lenght, self.total))
            return self.total

    # main funcs
    def part1(self):
        fishes = self.LanterFish(self.data, 80)
        lenght = fishes.iterSelf()
        return lenght

    def part2(self):
        return None
        '''
        fishes = self.LanterFish(self.data, 256)
        fishes.iterSelf()
        return lenght
        '''

    def appendData(self, data):
        self.data = [int(i) for i in data.split(',')]

    def dump(self):
        print('dddddddddddddddupmp')
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