class Puzzle:

    class _target:
        def __init__(self, target):
            self.probe = [0,0]
            self.targetArea = target
            self.targetTile = []
            self.maxHeight = 0
            self.possVelX = []
            '''
            The probe's x position increases by its x velocity.
            Due to drag, the probe's x velocity changes by 1 toward the value 0; that is, it decreases by 1 if it is greater than 0, increases by 1 if it is less than 0, or does not change if it is already 0.
            
            x = x0 + vt + (t * (-1 if v> 0 else (1 if v<0 else 0)))

            The probe's y position increases by its y velocity.
            Due to gravity, the probe's y velocity decreases by 1.
            
            y = y0 +vt - 0.5*t**2

            '''

        def evalMinVelocity_x(self):
            for idt, t in enumerate(self.targetTile[0]):
                countIter = 0
                tempx = t[0]
                v = 0
                while tempx > 0:
                    tempx = tempx - 1 - v
                    v += 1
                    countIter += 1
                # print('v: %d, t: %d' % (v, tempx))
                if tempx == 0:
                    self.possVelX.append((t[0], v, countIter))
            print(self.possVelX)
            return 0

        def evalVelocity_y(self):
            if not self.possVelX:
                return
            possXids = [i[0] for i in self.possVelX]
    
            possY = []
            for dy in self.targetTile:
                for dx in dy:
                    if dx[0] in possXids:
                        if dx[1] not in possY:
                            possY.append(dx[1])
            print(possY)
            initVel = 1
            initY = 0
        

        def iterateArea(self):
            for dy in range(self.targetArea['y0'], self.targetArea['y1']):
                temp = []
                for dx in range(self.targetArea['x0'], self.targetArea['x1']):
                    temp.append([dx, dy])
                self.targetTile.append(temp)
    
    # main funcs
    def part1(self):
        # target = self._target(self.data)
        # target.iterateArea()
        # print(target.targetTile)
        # target.evalMinVelocity_x()
        # target.evalVelocity_y()
        return None

    def part2(self):
        return None

    def appendData(self, data):
        temp = data[13:].split(', ')
        temp = [[int(j) for j in i[2:].split('..')] for i in temp]
        print(temp)
        (x0, x1) = (min(temp[0]), max(temp[0]))
        (y0, y1) = (min(temp[1]), max(temp[1]))
        self.data = {'x0': x0, 'y0': y0, 'x1': x1, 'y1': y1}

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