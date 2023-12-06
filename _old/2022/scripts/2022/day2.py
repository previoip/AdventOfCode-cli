class Puzzle:

    # main funcs
    def part1(self):
        total = 0
        for their, mine  in self.data:
            total += self.calc_score(their, mine)
        print(total)
        return total

    def part2(self):
        total = 0

        strat_lose = {
            'A': 'Z',
            'B': 'X',
            'C': 'Y'
        }

        for their, mine  in self.data:
            if mine == 'X':
                total += self.calc_score(their, strat_lose.get(their))
            elif mine == 'Y':
                total += self.calc_score(their, self.cond_draw.get(their))
            elif mine == 'Z':            
                total += self.calc_score(their, self.cond.get(their))
        print('P2',total)
        return total

    def appendData(self, data):
        self.data = [i.split(' ') for i in data.splitlines()]

    def calc_score(self, their, mine):
        if self.cond.get(their) == mine:
            # wins
            return self.score_if_win + self.score_from_selection.get(mine)
        elif self.cond_draw.get(their) == mine:
            # draws
            return self.score_if_draw + self.score_from_selection.get(mine)
        else:
            # loses
            return self.score_from_selection.get(mine)

    def dump(self):
        print('Dumping...')
        print(self.data)
        print(self.result)
        return

    # defaults
    def __init__(self, verbose):
        self.data = None
        self.cache = None
        self.verbose = verbose
        self.cond_draw = {
            'A': 'X',
            'B': 'Y',
            'C': 'Z'
        }
        self.cond = {
            'A': 'Y', # rock    > paper
            'B': 'Z', # paper   > scissor
            'C': 'X'  # scissor > rock
        }
        self.score_from_selection = {
            'X': 1,
            'Y': 2,
            'Z': 3
        }
        self.score_if_win = 6
        self.score_if_draw = 3

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