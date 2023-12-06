class Puzzle:
    class puzzleTile():
        def __init__(self, width=999, height=999):
            self.tile = [[[0] for _ in range(width)] for _ in range(height)]
            self.overlapCount = 0

        def appnedLines(self, point1, point2):
            (x1, y1) = point1
            (x2, y2) = point2
            tdx = x1 - x2
            tdy = y1 - y2
            dx = abs(tdx)
            dy = abs(tdy)
            if tdx != 0 and tdy != 0:
                grad = tdy/tdx
                if grad > 0:
                    x0 = min([x1, x2])
                    y0 = min([y1, y2])
                    while dx+1 and dy+1:
                        self.tile[y0 + dy][x0 + dx][0] += 1
                        dx -= 1
                        dy -= 1
                if grad < 0:
                    x0 = min([x1, x2])
                    y0 = max([y1, y2])
                    while dx+1 and dy+1:
                        self.tile[y0 - dy][x0 + dx][0] += 1
                        dx -= 1
                        dy -= 1
            else:
                x0 = min([x1, x2])
                y0 = min([y1, y2])
                for ix in range(dx+1):
                    for iy in range(dy+1):
                        self.tile[y0 + iy][x0 + ix][0] += 1
                


            # print('({}x{}y)({}x{}y)\ndx={} dy={}\n x0={} y0={}'.format(x1, y1, x2, y2, dx, dy, x0, y0))
        
        def evalOverlap(self):
            for i in self.tile:
                for j in i:
                    if j[0] > 1:
                        self.overlapCount += 1
        
        def getRes(self):
            return self.overlapCount
        
        def dump(self, verbose=False):
            if verbose:
                for i in self.tile:
                    print(''.join([' ' + str(j[0]) + ' ' if j[0] > 0 else ' . ' for j in i]))
            print('Lines Coincides: {}'.format(self.overlapCount))

    # main funcs
    def part1(self):
        set_p1 = [i for i in self.data if i[0][0] == i[1][0] or i[0][1] == i[1][1]]
        maxX = 0
        maxY = 0
        for i in set_p1:
            if i[0][0] > maxX:
                maxX = i[0][0]
            elif i[1][0] > maxX:
                maxX = i[1][0]
            if i[0][1] > maxY:
                maxY = i[0][1]
            if i[1][1] > maxY:
                maxY = i[1][1]

        self.screen = screen = self.puzzleTile(width=maxX+1, height=maxY+1)
        for point in set_p1:
            self.screen.appnedLines(point[0], point[1])
        self.screen.evalOverlap()
        return self.screen.getRes()

    def part2(self):
        set_p1 = [i for i in self.data]
        maxX = 0
        maxY = 0
        for i in set_p1:
            if i[0][0] > maxX:
                maxX = i[0][0]
            elif i[1][0] > maxX:
                maxX = i[1][0]
            if i[0][1] > maxY:
                maxY = i[0][1]
            if i[1][1] > maxY:
                maxY = i[1][1]

        self.screen = screen = self.puzzleTile(width=maxX+1, height=maxY+1)
        for point in set_p1:
            self.screen.appnedLines(point[0], point[1])
        self.screen.evalOverlap()
        return self.screen.getRes()

    def appendData(self, data):
        def noremalizeString(itemString):
            [point1, point2] = itemString.split('->')
            [x1, y1] = point1.split(',')
            [x2, y2] = point2.split(',')
            return (( int(x1), int(y1) ) , ( int(x2), int(y2) ))

        self.data = [noremalizeString(i) for i in data.splitlines()]

    def dump(self):
        print('Dumping result')
        self.screen.dump(verbose=True)
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