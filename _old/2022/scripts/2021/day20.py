class Puzzle:
    class ImageEnhance:

        def __init__(self, algoStr, imgArr):
            self.algo = algoStr
            self.img = [[i for i in j] for j in imgArr]
            # self.tempimg = []
            # (height, width) = len(imgArr), len(imgArr[0])
            # self.tempimg = self.img.copy()

        def extendImgPadding(self, direction):
            if direction not in [(1,0),(-1,0),(0,1),(0,-1)]:
                return
            paddStr = '.'
            (baseHeight, baseWidth) = self.getDimension()
            (dx, dy) = direction
            (newHeight, newWidth) = (baseHeight + abs(dy), baseWidth + abs(dx))
            if dy:
                self.img.insert(0 if dy==1 else newHeight-1, [paddStr for _ in range(newWidth)])
            elif dx:
                for y in range(baseHeight):
                    self.img[y].insert(0 if dx==-1 else newWidth-1, paddStr)
            return

        def getDimension(self):
            return (len(self.img), len(self.img[0]))

        def getCellBits(self, coord):
            tempBitStr = ''
            (x, y) = coord
            # for d in [(1,1),(0,1),(-1,1), (1,0),(0,0),(-1,0), (1,-1),(0,-1),(-1,-1)]:
            for d in [(-1,-1),(0,-1),(1,-1), (-1,0),(0,0),(1,0), (-1,1),(0,1),(1,1)]:
                (dx, dy) = (x + d[0], y + d[1])
                try:
                    tempBitStr += '1' if self.img[dy][dx] == '#' else '0'
                except IndexError:
                    tempBitStr += '0'
            return tempBitStr

        # def switch(self, setTemp = False):

        #     if setTemp:
        #         self.tempimg = self.img.copy()
        #     else:
        #         self.img = self.tempimg.copy()
        def evalLightCount(self):
            count = 0
            for row in self.img:
                for col in row:
                    if col == '#':
                        count += 1
            return count

        def getImage(self):
            return self.img

    # main funcs
    def part1(self):
        self.imgInst = self.ImageEnhance(self.algoStr, self.data)

        for p in [(1,0),(-1,0),(0,1),(0,-1)]: #init padding darkspot per side
            self.imgInst.extendImgPadding(p)
        
        # if self.verbose: print('Bits on (3,3): ' + self.imgInst.getCellBits((3,3)))
        # if self.verbose: print('bin to dec: ' + str(int(self.imgInst.getCellBits((3,3)), 2)))
        # if self.verbose: print('char from algo: ' + str(self.algoStr[int(self.imgInst.getCellBits((3,3)), 2)]))
        for _ in range(2):
            (baseHeight, baseWidth) = self.imgInst.getDimension()
            temp = []
            for y in range(baseHeight):
                temp.append([])
                for x in range(baseWidth):
                    # curr = self.imgInst.img[y][x]
                    index = int(self.imgInst.getCellBits((x,y)), 2)
                    repl = self.algoStr[index]
                    temp[y].append(repl)
                    # print('coord: (%d, %d) char: %d:%s %s' % (x, y, index, repl, self.imgInst.getCellBits((x,y))))
                    # self.imgInst.tempimg[y][x] = repl

                # print(''.join(temp[y]) + '     ' + ''.join(self.imgInst.img[y]))
            self.imgInst.img = temp

            for p in [(1,0),(-1,0),(0,1),(0,-1)]: #init padding darkspot per side
                self.imgInst.extendImgPadding(p)

        return self.imgInst.evalLightCount()

    def part2(self):
        return None

    def appendData(self, data):
        temp = data
        temp = data.splitlines()
        self.algoStr = temp.pop(0)
        temp.pop(0)
        self.data = temp
        return
        # self.data = [[k for k in i] for i in temp]

    def dump(self):
        print('Dumping...')
        print('algo:')
        print(self.algoStr)
        print('img:')
        for i in self.imgInst.getImage():
            print(' '.join([str(j) for j in i]))
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