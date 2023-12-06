from random import randint

CHAR_ACTIVE = '@'
CHAR_SOLID  = '#'
CHAR_REST   = '%'
CHAR_EMPTY  = '.'

block_set = [list(i) for i in [
    '@@@@' +\
    '....' +\
    '....' +\
    '....',

    '.@..' +\
    '@@@.' +\
    '.@..' +\
    '....',

    '..@.' +\
    '..@.' +\
    '@@@.' +\
    '....',

    '@...' +\
    '@...' +\
    '@...' +\
    '@...',

    '@@..' +\
    '@@..' +\
    '....' +\
    '....',
]]

def listTo2dList(screen, width):
    return [line for line in [screen[i*width:(i*width+width)] for i in range(len(screen)//width)]]

def flipList(screen, width) -> str:
    t = []
    for line in reversed(listTo2dList(screen, width)):
        t += line
    return t

def printList(screen, width):
    for line in listTo2dList(flipList(screen, width), width):
        print(''.join(line))
    print()

def newline(width, new_height=1) -> str:
    return [CHAR_EMPTY]*width*new_height

def queryScreenTile(screen_buffer, width, x, y):
    height = len(screen_buffer) // width

def iterWrapAround(ls):
    # iter generator that does not raise StopIteration when list is exhausted
    l = len(ls)
    c = 0
    while True:
        yield ls[c]
        c += 1 
        c %= l


class Puzzle:

    def part1(self):
        width = 7
        initial_height = 3
        # the only way to make screen buffer mutable is to make it as a list. Also note that the buffer 
        # is 1d array and is flipped, thus bottom of the game is within index 0 of the buffer. 
        # This is done to accommodate ease of adding new line when needed
        tetris_screen_buffer = [CHAR_SOLID]*width
        tetris_screen_buffer += newline(width, initial_height)

        printList(tetris_screen_buffer, width)

        for n, block in enumerate(block_set):
            block_set[n] = flipList(block, 4)
            print(block_set[n])

        block_iter = iterWrapAround(block_set)
        print(printList(next(block_iter), 4))
        print(printList(next(block_iter), 4))
        print(printList(next(block_iter), 4))
        print(printList(next(block_iter), 4))
        print(printList(next(block_iter), 4))
        print(printList(next(block_iter), 4))

        feed_new_block = True
        c = 0
        while False:
            

            instr = self.data[c % len(self.data)]
            c += 1



        return None

    def part2(self):
        return None

    def appendData(self, data):
        # data preprocessor
        self.data = [i for i in data.splitlines() if i][0]

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