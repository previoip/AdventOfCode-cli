import os

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
    
    def dump(self, verbose=False):
        if verbose:
            for i in self.tile:
                print(''.join([' ' + str(j[0]) + ' ' if j[0] > 0 else ' . ' for j in i]))
        print('Lines Coincides: {}'.format(self.overlapCount))

# main func
def getData(path):
    array = []
    with open(path, 'r') as filehandle: 
        array = filehandle.read().splitlines()
        filehandle.close()
    return array

def main():
    def noremalizeString(itemString):
        [point1, point2] = itemString.split('->')
        [x1, y1] = point1.split(',')
        [x2, y2] = point2.split(',')
        return (( int(x1), int(y1) ) , ( int(x2), int(y2) ))

    array = getData(os.getcwd() + '/p5/data.txt')
    normalized = [noremalizeString(i) for i in array]

    def puzzle5_part1():
        set_p1 = [i for i in normalized if i[0][0] == i[1][0] or i[0][1] == i[1][1]]
        screen = puzzleTile(width=999, height=999)
        for point in set_p1:
            screen.appnedLines(point[0], point[1])
        screen.evalOverlap()
        screen.dump()
        # print(set_p1)
    
    def puzzle5_part2():
        set_p2 = []
        # for p in normalized:
        #     p1 = p[0]
        #     p2 = p[1]
        #     dx = p1[0]-p2[0]
        #     dy = p1[1]-p2[1]
        #     grad = abs(dx)-abs(dy)
        #     if p1[0] == p2[0] or p1[1] == p2[1] or grad == 0:
        #         set_p2.append(p)
        set_p2 = [i for i in normalized]
        

        screen = puzzleTile(width=999, height=999)
        for point in set_p2:
            screen.appnedLines(point[0], point[1])
        screen.evalOverlap()
        screen.dump()
        # print(set_p1)
    
    def debug():
        t = puzzleTile(width=10, height=10)
        t.appnedLines((0,9), (5,9))
        t.appnedLines((8,0), (0,8))
        t.appnedLines((9,4), (3,4))
        t.appnedLines((2,2), (2,1))
        t.appnedLines((7,0), (7,4))
        t.appnedLines((6,4), (2,0))
        t.appnedLines((0,9), (2,9))
        t.appnedLines((3,4), (1,4))
        t.appnedLines((0,0), (8,8))
        t.appnedLines((5,5), (8,2))
        
        t.evalOverlap()
        
        t.dump(verbose=True)

    # debug()
    # puzzle5_part1()
    puzzle5_part2()

if __name__ == "__main__":
    main()
    