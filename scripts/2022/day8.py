class Tree:

    def __init__(self, height):
        self.height = height
        self.is_visible = False
        self.adjacent_trees = [[[],[],[]], [[],[],[]], [[],[],[]]]
        self.scenic_score = 0

    def addAdjacentTree(self, adjacent_tree, heading=(1, 0)):
        self.adjacent_trees[heading[0] + 1][heading[1] + 1].append(adjacent_tree)


    def __repr__(self):
        if self.is_visible:
            return f' {self.height} '
        else:
            return f'<{self.height}>'

    def evalVisibility(self):
        self.is_visible = any([all(map(lambda x: x.height < self.height, i)) if i else False for j in self.adjacent_trees for i in j])
        return [all(map(lambda x: x.height < self.height, i)) if i else False for j in self.adjacent_trees for i in j]

    def evalScenicScore(self):
        self.scenic_score = 1
        scores = []
        for row in self.adjacent_trees:
            for heading in row:
                if not heading:
                    continue
                scores.append(0)
                if not heading:
                    continue
                for item in heading:
                    if item.height == -1:
                        break
                    if item.height < self.height:
                        scores[-1] += 1
                    else:
                        scores[-1] += 1
                        break

        for n in scores:
            self.scenic_score *= n
        return self.scenic_score

class Puzzle:

    def part1(self):
        outer_bound_tree = Tree(-1)
        col_height = len(self.data)
        row_width  = len(self.data)

        kernel = [(-1,0), (0,1), (1,0), (0,-1)]
        #          left    top   right  bottom
        if self.verbose: 
            for row in self.data: 
                print(row)
            print()

        for n_col in range(col_height):
            for n_row in range(row_width):
                for vx, vy in kernel:
                    dx, dy = n_row, n_col
                    while True:
                        dx, dy = dx+vx, dy+vy
                        if dy > col_height-1 or dy < 0 or dx > row_width-1 or dx < 0:
                            self.data[n_col][n_row].addAdjacentTree(outer_bound_tree, (vy, vx))
                            break
                        else:
                            self.data[n_col][n_row].addAdjacentTree(self.data[dy][dx], (vy, vx))

        for n_col in range(col_height):
            for n_row in range(row_width):
                self.data[n_col][n_row].evalVisibility()


        if self.verbose: 
            for row in self.data: 
                print(row)

        return sum([1 if i.is_visible else 0 for j in self.data for i in j])

    def part2(self):
        outer_bound_tree = Tree(-1)
        col_height = len(self.data)
        row_width  = len(self.data)

        kernel = [(-1,0), (0,1), (1,0), (0,-1)]

        for n_col in range(col_height):
            for n_row in range(row_width):
                for vx, vy in kernel:
                    dx, dy = n_row, n_col
                    while True:
                        dx, dy = dx+vx, dy+vy
                        if dy > col_height-1 or dy < 0 or dx > row_width-1 or dx < 0:
                            self.data[n_col][n_row].addAdjacentTree(outer_bound_tree, (vy, vx))
                            break
                        else:
                            self.data[n_col][n_row].addAdjacentTree(self.data[dy][dx], (vy, vx))

        for n_col in range(col_height):
            for n_row in range(row_width):
                self.data[n_col][n_row].evalScenicScore()

        return max([i.scenic_score for j in self.data for i in j])

    def appendData(self, data):
        # data preprocessor
        self.data = data.splitlines()
        self.data = [list(i) for i in data.splitlines() if i]
        for n in range(len(self.data)):
            for m in range(len(self.data[n])):
                self.data[n][m] = Tree(int(self.data[n][m]))

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

                # for dy, dx in map(lambda x: (x[0] + n_col, x[1] + n_row), kernel):
