class Puzzle:

    class depthMap:
        def __init__(self, data):
            self.width = len(data[0])
            self.lowPoints = []
            self.scores = []
            self.score = 0
            self.lowPointsCount = 0
            self.basinSizes = []
            self.height = len(data)
            tile = [[9 for _ in range(self.width + 2)]]
            for y in range(self.height):
                temp_row = []
                temp_row.append(9)
                for x in range(self.width):
                    temp_row.append(int(data[y][x]))
                temp_row.append(9)
                tile.append(temp_row)
            tile.append([9 for _ in range(self.width + 2)])
            self.tile = tile
            self.tileBW = [[[i, False] for i in j] for j in tile]
            # self.tile = [[int(i) for i in j] for j in data]

        def dump(self):
            print('Width: {}, Height: {}'.format(self.width, self.height))
            print('Low points: {}, Risk: {}'.format(self.lowPointsCount, self.score))
            print('Low points val, coord: {}'.format(self.lowPoints))
            print(self.scores)
            tempTile = [['░' if i[1] is False else '█' for i in j] for j in self.tileBW]
            for i in tempTile:
                print(''.join(i))

        def evalAdj(self, x, y):
            current = self.tile[y][x]
            top = self.tile[y+1][x]
            bottom = self.tile[y-1][x]
            left = self.tile[y][x-1]
            right = self.tile[y][x+1]

            if current < top and current < left and current < bottom and current < right:
                self.lowPointsCount += 1
                self.lowPoints.append((current, (x, y)))
                self.scores.append(1 + current)
                
        def evalBasin(self):
            for (value, coord) in self.lowPoints:
                if self.tileBW[coord[1]][coord[0]][1] == True:
                    pass
                else:
                    count = 0
                    queue = []
                    queue.append(coord)
                    while queue:
                        cur = queue[0]
                        queue.pop(0)
                        if self.tileBW[cur[1]][cur[0]][0] < 9 and self.tileBW[cur[1]][cur[0]][1] == False:
                            self.tileBW[cur[1]][cur[0]][1] = True
                            count += 1
                            for dp in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                                try:
                                    queue.append((cur[0] + dp[0], cur[1] + dp[1]))
                                except IndexError:
                                    pass #NUH
                    self.basinSizes.append(count)
            
        def evalRisk(self):
            for y in range(self.height):
                for x in range(self.width):
                    self.evalAdj(x+1,y+1)

        def evalScore(self):
            self.score = sum(self.scores)
            return self.score

        def evalBasinScore(self):
            basins = self.basinSizes.copy()
            print(basins)
            temp = 1
            for i in range(3):
                temp = temp * max(basins)
                basins.pop(basins.index(max(basins)))
            return temp
    # main funcs
    def part1(self):
        tile = self.depthMap(self.data)
        tile.evalRisk()
        score = tile.evalScore()
        
        return score

    def part2(self):
        tile = self.depthMap(self.data)
        tile.evalRisk()
        score = tile.evalScore()
        tile.evalBasin()
        score = tile.evalBasinScore()

        return score

    def appendData(self, data):
        self.data = data.splitlines()

    def dump(self):
        print('Dumping result')
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