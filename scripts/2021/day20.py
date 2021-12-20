class Puzzle:
    class ImageEnhance:
        def __init__(self, algoStr, imgArr):
            self.algo = algoStr
            self.img = []
            self.tempimg = []
            imgArr
            (width, height) = len(imgArr), len(imgArr[0])
            padd = 2
            paddStr = 'X'
            self.img = [[paddStr for _ in range(width + padd)] for _ in range(height + padd)]
            for y in range(round(padd/2), round(height + padd/2)):
                for x in range(round(padd/2), round(height + padd/2)):
                    self.img[y][x] = imgArr[y - round(padd/2)][x - round(padd/2)]
            self.tempimg = self.img.copy()
        
        def switch(self):
            self.img = self.tempimg.copy()

        def getImage(self):
            return self.img

    # main funcs
    def part1(self):
        self.imgInst = self.ImageEnhance(self.algoStr, self.data)

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