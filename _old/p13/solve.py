import os

class TransparentPaper:
    def __init__(self, dx, dy):
        self.width = dx
        self.height = dy
        self.tile = [[0 for _ in range(dx)] for _ in range(dy)]

    def addDot(self, x, y):
        self.tile[y][x] += 1
    
    def fold(self, axis, l):
        half = 0
        temp = []
        if axis == 'x':
            newWidth = self.width - l - 1
            temp = [[0 for _ in range(newWidth)] for _ in range(self.height)]
            for iy, y in enumerate(temp):
                for ix, x in enumerate(y):
                    temp[iy][ix] = self.tile[iy][ix] + self.tile[iy][self.width - ix - 1]
            self.tile = temp
            self.width = newWidth
        elif axis == 'y':
            newHeight = self.height - l - 1
            temp = [[0 for _ in range(self.width)] for _ in range(newHeight)]
            for iy, y in enumerate(temp):
                for ix, x in enumerate(y):
                    temp[iy][ix] = self.tile[iy][ix] + self.tile[self.height - iy - 1][ix]
            self.tile = temp
            self.height = newHeight
        else:
            return

    def evalDotCount(self):
        temp = 0
        for y in self.tile:
            for x in y:
                if x>0:
                    temp += 1
        return temp

    def dump(self):
        for i in self.tile:
            print(''.join(['▓▓' if a > 0 else '. ' for a in i]))
        print('w:{} h:{} dots:{}'.format(self.width, self.height, self.evalDotCount()))

def getData(path):
    array = []
    string =  ''
    with open(path, 'r') as filehandle:
        string = filehandle.read()
        filehandle.close()
    [dots, inst] = string.split('-')
    
    dots = dots.splitlines()
    inst = inst.splitlines()

    maxx = 0
    maxy = 0
    temp = []
    for d in dots:
        (x, y) = d.split(',')
        if int(x) >= maxx:
            maxx = int(x)
        if int(y) >= maxy:
            maxy = int(y)
        temp.append((int(x), int(y)))

    inst = [(i[11:].split('=')[0], int(i[11:].split('=')[1])) for i in inst if i != '']
    return (inst, temp, maxx, maxy)


def main():
    data = getData(os.getcwd() + '/p13/data.txt')
    instruct = data[0]

    paper = TransparentPaper(data[2]+1, data[3]+1)
    for i in data[1]:
        paper.addDot(i[0], i[1])
    
    print(instruct)
    # paper.dump()
    # paper.fold(instruct[0][0], instruct[0][1])
    for (ax, dp) in instruct:
        paper.fold(ax, dp)
    paper.dump()

if __name__ == '__main__':
    main()