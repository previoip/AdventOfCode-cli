def parse(data_str: str, callback: lambda x: x) -> list:
    assert data_str[0] == '[' and data_str[-1] == ']'
    temp = []
    leftover = ''
    data_str = data_str[1:] 
    while data_str[0] != ']':
        c = data_str[0]
        if c == '[':
            res, data_str = parse(data_str, callback)
            temp.append(res)
        elif c ==']':
            continue
        elif c != ',':
            temp.append(callback(c))
        data_str = data_str[1:]
    return temp, data_str

def evalP1(left, right):
    if len(left) == 0:
        return True
    if len(right) == 0:
        return False

    for n, left_item in enumerate(left):
        if n+1 > len(right):
            return False
        right_item = right[n]
        if isinstance(left_item, int) and isinstance(right_item, int):
            if left_item < right_item:
                return True
            elif left_item > right_item:
                return False
        elif isinstance(left_item, list) and isinstance(right_item, list):
            res = evalP1(left_item, right_item)
            if res == None:
                continue
            else:
                return res
        elif isinstance(left_item, list) and isinstance(right_item, int):
            res = evalP1(left_item, [right_item for _ in range(len(left_item))])
            if res == None:
                continue
            else:
                return res
        elif isinstance(left_item, int) and isinstance(right_item, list):
            res = evalP1([left_item for _ in range(len(right_item))], right_item)
            if res == None:
                continue
            else:
                return res
    return True    

class Puzzle:

    def part1(self):
        dup = []
        res = []
        data = self.data.copy()
        while data:
            line = data.pop(0)
            if isinstance(line, str):
                if self.verbose: print('evaluating: ', dup)
                res.append(evalP1(*dup))
                if self.verbose: print('result: ', res[-1])
                if self.verbose: 
                    if input():
                        exit()
                dup.clear()
            else:
                dup.append(line)
        if self.verbose:
            print('results: ', res)
            print('indexes: ', [n+1 for n, i in enumerate(res) if i])
            print('sums: ', sum([n+1 for n, i in enumerate(res) if i]))
        return None

    def part2(self):
        return None

    def appendData(self, data):
        # data preprocessor
        self.data = [i for i in data.splitlines()]
        if not self.data[0]:
            self.data.pop(0)
        
        for n in range(len(self.data)):
            if self.data[n]:
                self.data[n], _ = parse(self.data[n], int)


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