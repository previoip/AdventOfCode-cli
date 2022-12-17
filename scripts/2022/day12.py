from math import sqrt

kernel = [(0,1), (1,1), (1,0), (1,-1), (0,-1), (-1,-1), (-1,0), (-1,1)]

def padstr(string, padlen):
    if len(string) > padlen:
        return string
    return string + ' ' * (padlen-len(string))

class GraphNode:
    def __init__(self, pos, initial_height, node_type):
        self.pos = pos
        self.height = initial_height
        self.length = 10e10
        self.is_visited = False
        self.trace = None
        self.node_type = node_type
        self.adjacent_nodes = [[None,None,None],[None,self,None],[None,None,None]]

        if node_type == 'boundary':
            self.is_visited = True

    def setAdjacentNodes(self, x, y, node):
        assert not (x == 0 and y == 0), 'mate just referenced himself'
        x, y = x+1, y+1
        self.adjacent_nodes[y][x] = node

    def getAdjacentNodes(self, x, y):
        assert not (x == 0 and y == 0), 'mate just referenced himself'
        x, y = x+1, y+1
        return self.adjacent_nodes[y][x]

    def manhattanDist(self, o):
        if not isinstance(o, self.__class__):
            raise ValueError('Cannot calculate distance')
        return abs(o.pos[0] - self.pos[0]) + abs(o.pos[1] - self.pos[1])

    def euclidDist(self, o):
        if not isinstance(o, self.__class__):
            raise ValueError('Cannot calculate distance')
        return sqrt((o.pos[0] - self.pos[0])**2 + (o.pos[1] - self.pos[1])**2)


    def __repr__(self):
        if self.node_type == 'start':
            return '[' + padstr(str(self.height), 2) + ']'
        elif self.node_type == 'end':
            return '{' + padstr(str(self.height), 2) + '}'
        elif self.is_visited:
            return '|' + padstr(str(self.height), 2) + '|'
        return '<' + padstr(str(self.height), 2) + '>'


class Puzzle:

    def part1(self):
        for i in self.data:
            for j in i:
                j.is_visited = False


        tangent_kernel = kernel[::2]
        confident_score = [0]*len(tangent_kernel)
        curr_node = self.start_node
        curr_node = self.data[2][2]

        if self.verbose:
            for adj in curr_node.adjacent_nodes:
                print(adj)

        while curr_node.node_type != 'end':
            break    

        return None

    def part2(self):
        for i in self.data:
            for j in i:
                j.is_visited = False

        return None

    def appendData(self, data):
        # data preprocessor
        self.data = [list(i) for i in data.splitlines() if i]
        self.start_node = None
        self.end_node = None
        for i in range(len(self.data)):
            for j in range(len(self.data[i])):
                if self.data[i][j] == 'S':
                    self.data[i][j] = GraphNode((i, j), 1, 'start') 
                    self.start_node = self.data[i][j]
                elif self.data[i][j] == 'E':
                    self.data[i][j] = GraphNode((i, j), 26, 'end') 
                    self.end_node = self.data[i][j]
                else:
                    self.data[i][j] = GraphNode((i, j), ord(self.data[i][j])-96, 'path') 

        for n in range(len(self.data)):
            for m in range(len(self.data[n])):
                for dx, dy in kernel:
                    dm, dn = m+dx, n+dy
                    if dn >= len(self.data) or dn < 0 or dm >= len(self.data[n]) or dm < 0:
                        self.data[n][m].setAdjacentNodes(dx, dy, GraphNode((dn, dm), 27, 'boundary'))
                    else:
                        self.data[n][m].setAdjacentNodes(dx, dy, self.data[dn][dm])


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
        for i in self.data:
            for j in i:
                print(j, end=' ')
            print()
        print(self.result)
        return

    def getResult(self):
        return self.result

if __name__ == "__main__":
    pass