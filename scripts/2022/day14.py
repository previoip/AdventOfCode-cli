from math import sqrt


def castInt(ls: list):
    for n, i in enumerate(ls):
        if isinstance(i, list):
            castInt(i)
        else:
            ls[n] = int(i)

def flattenList(ls: list) -> list:
    t = []
    for i in ls:
        if isinstance(i, list):
            t += flattenList(i)
        else:
            t.append(i)
    return t

def padstr(string, l):
    if not isinstance(string, str):
        string = str(string)
    if len(string) > l:
        return string
    return string + ' '*(l - len(string))

class Tile:
    def __init__(self):
        self.tile_type = 'air'
        self.settled = False
        self.update_pass = False

    def setType(self, tile_type_enum):
        self.tile_type = tile_type_enum
        if tile_type_enum == 'sand':
            self.settled = False
        elif tile_type_enum == 'rock':
            self.settled = True
        elif tile_type_enum == 'out_of_bound':
            self.settled = True
        return self

    def update(self):
        pass

    def __repr__(self):
        if self.tile_type == 'rock':
            return '#'
        elif self.tile_type == 'sand' and not self.settled: 
            return 'o'
        elif self.tile_type == 'sand' and self.settled: 
            return 'O'
        elif self.tile_type == 'out_of_bound':
            return '%'
        else:
            return '.'

class Simulator:
    def __init__(self, width, height):
        self.padding = 2
        self.gravity = (0, 1)
        self.cursor = [0,0]
        self._width = width
        self._height = height
        self.tile_width = width + (self.padding*2)
        self.tile_height = height + (self.padding*2)
        self.tile_buffer = [[Tile() for i in range(self.tile_width)] for _ in range(self.tile_height)]
        self.update_priority_stack = []
        self.tile_oob = Tile().setType('out_of_bound')
        self.scan_kernel = [
            (-1,0),
            (-1,1),
            (0, 1),
            (1, 1),
            (1, 0),
        ]
        self.eof = False
        self.out_ouf_bound_eof = False

    def reset(self):
        self.eof = False

    def getTileAtPos(self, x, y):
        x = x + self.padding
        y = y + self.padding
        if x < 0 or x > self.tile_width-1 or y < 0  or y > self.tile_height-1:
            return self.tile_oob
        return self.tile_buffer[y][x]

    def drawPoint(self, x, y, tile_type_enum):
        self.getTileAtPos(x, y).setType(tile_type_enum)
        if tile_type_enum == 'sand':
            self.update_priority_stack.append([x, y])

    def drawSquare(self, start_x, end_x, start_y, end_y, tile_type_enum):
        if start_x > end_x:
            end_x, start_x = start_x, end_x
        if start_y > end_y:
            end_y, start_y = start_y, end_y
        for ny in range(start_y, end_y+1):
            for nx in range(start_x, end_x+1):
                self.drawPoint(nx, ny, tile_type_enum)
    
    def update(self, all_tiles=True):
        if self.eof:
            return

        if all_tiles:
            for x in range(self._width + (self.padding*2)):
                x -= self.padding
                for y in range(self._height + (self.padding*2)):
                    y -= self.padding
                    tile = self.getTileAtPos(x, y)
                    if not tile.update_pass:
                        self.updateTile(x, y)
        else:
            curr_stack = self.update_priority_stack.copy() 
            self.update_priority_stack.clear()
            for x, y in curr_stack:
                tile = self.getTileAtPos(x, y)
                if not tile.update_pass:
                    self.updateTile(x, y)
            pass
        self.updateDefer()

    def updateTile(self, x, y):
        tile = self.getTileAtPos(x, y)

        # tile update rules
        if tile and tile.tile_type == 'sand' and not tile.settled:
            kernel = []
            for dx, dy in self.scan_kernel:
                kernel.append(self.getTileAtPos(x+dx, y+dy))

            # kernel index
            #
            #   0 x 4
            #   1 2 3
 
            if any(map(lambda x: x.tile_type == 'out_of_bound', kernel)):
                self.out_ouf_bound_eof = True

            # order matters fuck fuck fuck fuck fuck fuck 
            if (kernel[1].settled and kernel[2].settled and kernel[3].settled):
                # (kernel[1].settled and kernel[2].settled and kernel[4].settled) or \
                # (kernel[0].settled and kernel[2].settled and kernel[3].settled):
                tile.settled = True

            elif not kernel[2].settled:
                self.drawPoint(x, y, 'air')
                self.drawPoint(x+self.gravity[0], y+self.gravity[1], 'sand')
                self.getTileAtPos(x+self.gravity[0], y+self.gravity[1]).update_pass = True

            elif kernel[2].settled and kernel[3].settled:
                self.drawPoint(x, y, 'air')
                self.drawPoint(x+self.gravity[0]-1, y+self.gravity[1], 'sand')
                self.getTileAtPos(x+self.gravity[0]-1, y+self.gravity[1]).update_pass = True

            elif kernel[2].settled and kernel[1].settled:
                self.drawPoint(x, y, 'air')
                self.drawPoint(x+self.gravity[0]+1, y+self.gravity[1], 'sand')
                self.getTileAtPos(x+self.gravity[0]-1, y+self.gravity[1]).update_pass = True

            elif kernel[2].settled and not kernel[1].settled and not kernel[3].settled:
                self.drawPoint(x, y, 'air')
                self.drawPoint(x+self.gravity[0]-1, y+self.gravity[1], 'sand')
                self.getTileAtPos(x+self.gravity[0]-1, y+self.gravity[1]).update_pass = True

            # if [x, y] in self.update_priority_stack:
            #     self.update_priority_stack.pop(self.update_priority_stack.index([x, y]))


    def updateDefer(self):
        a = []
        for x in range(self._width + (self.padding*2)):
            x -= self.padding
            for y in range(self._height + (self.padding*2)):
                y -= self.padding
                tile = self.getTileAtPos(x, y)
                tile.update_pass = False
                if tile.tile_type == 'sand':
                    a.append(tile.settled)
        self.eof = all(a)

    def countSand(self):
        return sum([1 if i.tile_type == 'sand' else 0 for i in flattenList(self.tile_buffer)])

    def __repr__(self):
        t = ''
        numstr_len = len(str(len(self.tile_buffer[0])))
        if numstr_len > 1:
            # t += ' ' * (3+1)
            temp = list(range(len(self.tile_buffer[0])))
            temp = list(map(lambda x: padstr(x-self.padding, numstr_len+1), temp))
            temp = list(map(lambda x: list(x), temp))
            temp = flattenList(temp)
            for ns in range(numstr_len+1):
                t += ' ' * (numstr_len+2)
                t += ''.join(temp[ns::numstr_len+1])
                t += '\n'

        for ni, i in enumerate(self.tile_buffer):
            t += padstr(ni-self.padding, 3) + ' '
            for nj, j in enumerate(i):
                if [nj, ni] == list(map(lambda x: x + self.padding, self.cursor)):
                    t += 'S'
                else:
                    t += str(j)
            t += '\n'
        return t


class Puzzle:

    def part1(self):
        sim = Simulator(self.tile_width, self.tile_height)
        for line in self.data:
            for n in range(len(line)-1):
                px, py = line[n]
                ix, iy = line[n+1]
                px, ix = px - self.tile_width_extrema[0], ix - self.tile_width_extrema[0]
                sim.drawSquare(px, ix, py, iy, 'rock')
        
        sim.cursor = [500-self.tile_width_extrema[0], 0]
        if self.verbose:
            print('Simulator: ')
            print(sim)

        c = 0
        while not sim.out_ouf_bound_eof:
            if c % 4:
                sim.drawPoint(sim.cursor[0], sim.cursor[1], 'sand')
            while not sim.eof:
                sim.update(all_tiles=False)
            sim.reset()
            c += 1
            if self.verbose: print(sim) 

        if self.verbose:
            print('After update: ')
            print(sim)
            print('Sand count: ', sim.countSand())
        print(sim)
        return sim.countSand() - 1

    def part2(self):
        # ive wasted so much time on this
        return None

    def appendData(self, data):
        # data preprocessor
        self.data = [[j.strip().split(',') for j in i.split('->')] for i in data.splitlines() if i]
        castInt(self.data)
        x_coords = flattenList(self.data)[::2]
        y_coords = flattenList(self.data)[1::2]
        x_extrema = min(x_coords), max(x_coords)
        self.tile_width_extrema = x_extrema
        self.tile_width = x_extrema[1] - x_extrema[0] + 1
        self.tile_height = max(y_coords) + 1

    # defaults
    def __init__(self, verbose):
        self.data = None
        self.cache = None
        self.verbose = verbose
        self.stripData = True

    def run(self, part):
        if part == 2:
            self.result = self.part2()
        else:
            self.result = self.part1()

        if self.verbose:
            self.dump()

    def dump(self):
        print('Dumping...')
        print(self.data)
        print(self.result)
        return

    def getResult(self):
        return self.result

if __name__ == "__main__":
    pass