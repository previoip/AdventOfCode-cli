import os

class Poly:
    def __init__(self, sequence):
        self.sequence = sequence
        self.itemDict = {}

    
    def dump(self, verbose=False):
        if verbose: print(self.sequence)
        print(self.itemDict)
        (maxVal, minVal) = (max(self.itemDict.values()), min(self.itemDict.values()))
        
        print('Max value: {}, Min value: {}, div: {}'.format(maxVal, minVal, maxVal-minVal))


    def iterInstruction(self, inst):
        print(len(self.sequence))
        ret = self.sequence[0]
        for i in range(len(self.sequence)-1):
            chars = self.sequence[i] + self.sequence[i+1]
            temp = ''
            for e in inst:
                if chars == e[0]:
                    temp = e[1] + chars[1]
            if not temp:
                ret += chars
            else:
                ret += temp
        self.sequence = ret
    
    def evalElement(self):
        self.itemDict = {}
        for char in self.sequence:
            if char not in self.itemDict:
                self.itemDict[char] = 1
            else:
                self.itemDict[char] += 1
        return


def getData(path):
    array = []
    with open(path, 'r') as filehandle:
        array = filehandle.read().splitlines()
        filehandle.close()
    temp = False
    data = []
    test = []
    for i in array:
        if i == 'input:':
            temp = True
        if temp:
            if i:
                test.append(i)
        else:
            if i:
                data.append(i)
    return (test[1:], data[1:])

def main():
    data = getData(os.getcwd() + '/p14/data.txt')
    data = data[0]

    sequence = data.pop(0)
    instr = []

    for i in data:
        (pattern, repl) = i.split(' -> ')
        instr.append((pattern, repl))
    
    polymer = Poly(sequence)
    for _ in range(40):
        polymer.iterInstruction(instr)
    polymer.evalElement()
    polymer.dump()

if __name__ == '__main__':
    main()