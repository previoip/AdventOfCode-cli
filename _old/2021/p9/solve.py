import os

def getData(path):
    array = []
    with open(path, 'r') as filehandle:
        array = filehandle.read().splitlines()
        filehandle.close()
    return array

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

def puzzle9_part1():
    testString = [
        '2199943210',
        '3987894921',
        '9856789892',
        '8767896789',
        '9899965678'
        ]

    testString2 = [
        '989',
        '858',
        '969'
    ]
    data = getData(os.getcwd() + '/p9/data.txt')
    tile = depthMap(data)
    tile.evalRisk()
    tile.evalScore()
    tile.evalBasin()
    print(tile.evalBasinScore())
    tile.dump()
    

if __name__ == "__main__":
    puzzle9_part1()