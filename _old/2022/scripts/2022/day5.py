class CrateStack:

    def __init__(self, nth, stack):
        self.nth = int(nth)
        self.stack = self.normStack(stack)

    def normStack(self, stack):
        ret_stack = []

        for n, i in enumerate(stack):
            if i == 'NAN':
                continue
            else:
                ret_stack.append(i[1:2])
        return ret_stack

    def put(self, val):
        self.stack.append(val)
    
    def pop(self):
        return self.stack.pop()

    def __repr__(self):
        return f'stack ({self.nth}) > ' + ' '.join(self.stack)

def parseInstruction(instr):
    instr = instr.split(' ')
    n, src, dst = map(int, [instr[1], instr[3], instr[5]])
    # return n, src, dst
    return n, src, dst


def moveToByInstruction(stacks, instr, reverse=True):
    n, src, dst = parseInstruction(instr)
    t = []
    for _ in range(n):
        t.append(stacks[src-1].pop())
    if not reverse:
        t = list(reversed(t))
    for _ in range(n):
        stacks[dst-1].put(t.pop())

class Puzzle:

    def part1(self):
        stacks = [CrateStack(i[0], i[1:]) for i in self.data]

        for instr in self.instructions:
            moveToByInstruction(stacks, instr, False)
            if self.verbose: 
                print()
                print(instr)
                for i in stacks:
                    print(i)
                input()

        return ''.join([i.pop() for i in stacks])

    def part2(self):
        stacks = [CrateStack(i[0], i[1:]) for i in self.data]

        for instr in self.instructions:
            moveToByInstruction(stacks, instr, True)
            if self.verbose: 
                print()
                print(instr)
                for i in stacks:
                    print(i)
                input()

        return ''.join([i.pop() for i in stacks])


    def appendData(self, data):
        # data preprocessor
        self.data = data.splitlines()
        self.instructions = []

        if not self.data[0]:
            self.data.pop(0) # i spent nearly 2 hrs just because of this f*cker 

        for n, d in enumerate(self.data):
            if not d.strip():
                self.instructions = self.data[n:]
                self.data = self.data[:n]
                self.instructions.pop(0)
                break

        col_height = len(self.data)

        stacks = []
        for d in self.data:
            while d:
                a = d[:3]
                a = a.strip()
                if not a:
                    a = 'NAN'
                stacks.append(a)
                d = d[4:]

        row_width = len(stacks) // col_height

        self.data = [list() for _ in range(row_width)]
        for n in range(row_width):
            self.data[n] = list(reversed(stacks[n::row_width]))

        if self.verbose:
            for d in self.data:
                print(d)


    # defaults
    def __init__(self, verbose):
        self.data = None
        self.cache = None
        self.verbose = verbose
        self.stripData = False

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