class Puzzle:
    # main funcs
    class Chiton:
        def __init__(self, tile):
            self.tile = tile
            self.curr = [0,0]
            self.adj = {'n':0, 'e':0,'s':0, 'w':0, 'nn':0, 'ee':0,'ss':0, 'ww':0}
            self.adjCoord = [(0,-1), (1,0), (0,1), (-1,0), (0,-2), (2,0), (0,2), (-2,0)]
            self.adjDict = [i for i in self.adj.keys()]
            self.score = 0

            self.deterPath = {
                's'     : [(0,1)], 
                'ss'    : [(0,1), (0,2)], 
                'se'    : [(0,1), (1,1)], 
                'sse'   : [(0,1), (0,2), (1,2)], 
                'e'     : [(1,0)], 
                'ee'    : [(1,0), (2,0)], 
                'es'    : [(1,0), (1,1)],
                'ees'   : [(1,0), (2,0), (2,1)], 
                }
            self.deter = {}
            for i in self.deterPath.keys():
                self.deter[i] = None

        def eval_deter(self):
            for i in self.deter.keys():
                paths = self.deterPath[i]
                temp = 0
                for p in paths:
                    dx = self.curr[0] + p[0]
                    dy = self.curr[1] + p[1]
                    try:
                        temp += self.tile[dy][dx][0]
                    except IndexError:
                        temp = 100
                self.deter[i] = temp
            # print(self.curr)
            # print(self.deter)

        def examine_adj(self):
            for i, p in enumerate(self.adjCoord):
                crdnl = self.adjDict[i]
                dx = self.curr[0] + p[0]
                dy = self.curr[1] + p[1]
                try:
                    adj = self.tile[dy][dx][0]
                    stat = self.tile[dy][dx][1]
                    self.adj[crdnl] = {'value': adj, 'past': stat}
                except IndexError:
                    self.adj[crdnl] = {'value': 0, 'past': True}


        def get_possibleMinimalValueTakenOnPath(self):
            # lmfao

            # limit
            (width, height) = (len(self.tile[0]), len(self.tile))
            if self.curr[0] > width-2:
                return (0,1)
            if self.curr[1] > height-2:
                return (1,0)

            # print('adjacent-> s:%s ss:%s e:%s ee:%s'%(self.adj['s']['value'], self.adj['ss']['value'], self.adj['e']['value'], self.adj['ee']['value']))

            # main algo
            downSum = self.adj['s']['value'] + self.adj['ss']['value']
            rightSum = self.adj['e']['value'] + self.adj['ee']['value']
            # print('sums -> south: %d, east: %d'%(downSum, rightSum))

            downSum = sum((self.deter['s'], self.deter['ss'], self.deter['se'], self.deter['sse']))
            rightSum = sum((self.deter['e'], self.deter['ee'], self.deter['es'], self.deter['ees']))

            # print('toRight:%d toDown:%d'%(rightSum, downSum))
            if downSum > rightSum:
                return (1,0)
            elif rightSum > downSum:
                return (0, 1)
            else:
                return (1, 0)
            # print(keys, values)

        def set_move(self, pos):
            try:
                (self.curr[0], self.curr[1]) = (self.curr[0] + pos[0], self.curr[1] + pos[1])
                self.score  += self.tile[self.curr[1]][self.curr[0]][0]
                self.set_pathway()
            except IndexError:
                return

        def is_it_done_yet(self):
            (width, height) = (len(self.tile[0]), len(self.tile))
            if self.curr[0] >= width-1 and self.curr[1] >= height-1:
                return False
            return True

        def set_pathway(self):
            self.tile[self.curr[1]][self.curr[0]][1] = True

        def get_tile(self):
            return self.tile

    def part1(self):
        chiton = self.Chiton(self.data)
        chiton.set_move((0,0))
        chiton.examine_adj()
        chiton.eval_deter()

        while chiton.is_it_done_yet():
            nxt = chiton.get_possibleMinimalValueTakenOnPath()
            chiton.set_move(nxt)
            # chiton.examine_adj()
            chiton.eval_deter()

        print('score: %d' % (chiton.score))
        (width, height) = (len(self.data[0]), len(self.data))

        self.data = chiton.get_tile()
        return chiton.score - chiton.tile[height-1][width-1][0]

    def part2(self):
        return None

    def appendData(self, data):
        self.data = [[[int(i), False] for i in j] for j in data.splitlines()]

    def dump(self):
        print('Dumping result')
        for i in self.data:
            print(''.join([('%s%s%s' % ( '[' if j[1] else ' ',j[0], ']' if j[1] else ' ')) for j in i]))
        # print(self.result)
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