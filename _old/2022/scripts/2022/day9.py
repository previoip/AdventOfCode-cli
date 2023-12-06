from math import isclose

class Vec2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def set(self, x, y):
        self.x = x
        self.y = y
        return self
    
    def __add__(self, o):
        x = self.x + o.x
        y = self.y + o.y
        return self.__class__(x, y)

    def __sub__(self, o):
        x = self.x - o.x
        y = self.y - o.y
        return self.__class__(x, y)

    def __mul__(self, o):
        if isinstance(o, (int, float)):
            x = self.x * o
            y = self.y * o
            return self.__class__(x, y)
        else:
            raise ValueError('No.')

    def __truediv__(self, o):
        if isinstance(o, (int, float)):
            x = self.x / o
            y = self.y / o
            return self.__class__(x, y)
        else:
            raise ValueError('No.')


    def __repr__(self):
        return f'<{self.x}, {self.y}>'

    def __abs__(self):
        self.x = abs(self.x)
        self.y = abs(self.y)
        

    def __eq__(self, o):
        return all((isclose(self.x, o.x), isclose(self.y, o.y)))

    def rev(self):
        x = int(self.x)
        self.x = self.y
        self.y = x

class RopeNode:
    def __init__(self, name, pos):
        self.name = name
        self.front = None
        self.back = None
        self.pos = pos

    def addNode(self, node: "RopeNode"):
        self.back = node
        node.front = self

    def move(self, incr: Vec2):
        self.pos += incr


motion_enum = {
    'U': Vec2(0,1),
    'D': Vec2(0,-1),
    'L': Vec2(-1,0),
    'R': Vec2(1,0)
}

class Puzzle:

    def part1(self):
        head = RopeNode('H', Vec2(0, 0))
        tail = RopeNode('T', Vec2(0, 0))
        head.addNode(tail)

        # [-2, 2][-1, 2][ 0, 2][ 1, 2][ 2, 2]
        # [-2, 1]<-1, 1>< 0, 1>< 1, 1>[ 2, 1]
        # [-2, 0]<-1, 0>< 0, 0>< 1, 0>[ 2, 0]
        # [-2,-1]<-1,-1>< 0,-1>< 1,-1>[ 2,-1]
        # [-2,-2][-1,-2][ 0,-2][ 1,-2][ 2,-2]

        for mot, n_times in self.data:
            for n in range(n_times):
                head.move(mot)
                diff = tail.pos - head.pos

                if self.verbose: print('Before: head pos: ', head.pos, '\ttail pos: ', tail.pos, '\tdiff: ', diff)
                # tail.pos = tail.pos - diff
                if (abs(diff.x) > 1 and abs(diff.y) <= 1) or (abs(diff.x) <= 1 and abs(diff.y) > 1):
                    tail.pos = tail.pos - diff
                elif abs(diff.x) > 1 and abs(diff.y) > 1:
                    tail.pos = tail.pos - (diff/2)

                diff = tail.pos - head.pos
                if self.verbose: print('After: head pos: ', head.pos, '\ttail pos: ', tail.pos, '\tdiff: ', diff); print()
        return None

    def part2(self):
        return None

    def appendData(self, data):
        # data preprocessor
        self.data = [i.split(' ') for i in data.splitlines() if i]
        self.data = [(motion_enum[i[0]], int(i[1])) for i in self.data]


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