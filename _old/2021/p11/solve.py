class octopi:

    def __init__(self):
        self.totalFlash = 0
        self.step = 0

    def appendData(self, isTest = True):
        realData = [
            '4658137637',
            '3277874355',
            '4525611183',
            '3128125888',
            '8734832838',
            '4175463257',
            '8321423552',
            '4832145253',
            '8286834851',
            '4885323138'

        ]
        localtestData = [
            '5483143223',
            '2745854711',
            '5264556173',
            '6141336146',
            '6357385478',
            '4167524645',
            '2176841721',
            '6882881134',
            '4846848554',
            '5283751526'
        ]
        if not isTest: self.data = [[int(i) for i in j] for j in realData]
        else: self.data = [[int(i) for i in j] for j in localtestData]

    def iterData(self):
        self.step += 1
        for dy, y in enumerate(self.data):
            for dx, x in enumerate(y):
                self.data[dy][dx] += 1
                if self.data[dy][dx] >= 9:
                    # self.totalFlash += 1
                    pass

        while True:
            whole = []
            knownLoc = []
            for dy, y in enumerate(self.data):
                for dx, x in enumerate(y):
                    if x >= 10:
                        for (px, py) in [(0, -1), (0, 1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, -1), (-1, 1)]:
                            try:
                                ix = dx + px
                                iy = dy + py
                                if ix < 0 or iy < 0: raise IndexError()
                                if self.data[iy][ix] != 0:
                                    self.data[iy][ix] += 1
                                if self.data[iy][ix] > 9:
                                    # self.data[iy][ix] = 0
                                    # self.totalFlash += 1
                                    pass
                            except IndexError:
                                pass
                        knownLoc.append((dx, dy))
                        # self.data[dy][dx] = 0
            for (dx, dy) in knownLoc:
                self.totalFlash += 1
                self.data[dy][dx] = 0

            for i in self.data:
                for j in i:
                    whole.append(True if j <= 9 else False)

            if all(whole): break

    def evalAll(self):
        temp = []
        for i in self.data:
            for j in i:
                temp.append(True if j == 0 else False)
        return all(temp)

    def dump(self):
        for j in self.data:
            print(''.join(['██' if i == 0 else '░░' for i in j]) + '\t' + ''.join([str(i) for i in j]))
        print('\n')


def main():
    octo = octopi()
    octo.appendData(False)
    # num = 100
    # for _ in range(num):
    #     octo.iterData()
    # octo.dump()
    # print(octo.totalFlash)
    # print(octo.evalAll())

    while True:
        octo.iterData()
        octo.dump()
        print(octo.evalAll(), octo.totalFlash)
        if octo.evalAll():
            break
    octo.dump()
    print('total step {}'.format(octo.step))


if __name__ == '__main__':
    main()