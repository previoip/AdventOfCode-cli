import os

class Diagnostics:
    def __init__(self):
        self.binaryContainer = []
        self.binaryCount = []
        self.cache = []

    def insertBinaryString(self, binString):
        self.binaryContainer.append(binString)

    def evalBinCount(self, onIndex):
        temp = {'0': 0, '1': 0}
        for i in self.cache:
            if i[onIndex] == '1':
                temp['1'] += 1
            else:
                temp['0'] += 1
        return temp
    
    def begin(self):
        self.cache = self.binaryContainer.copy()

    def removeBasedOnValOnIndex(self, value, indexOffset):
        if len(self.cache) == 1: return False
        tempIndices = []
        for i in self.cache:
            if value == i[indexOffset]:
                itemp = self.cache[self.cache.index(i)]
                if itemp not in tempIndices:
                    tempIndices.append(itemp)
        for item in tempIndices:
            try:
                self.cache.remove(item)
            except ValueError:
                pass
        return True

def getData(path):
    array = []
    with open(path, 'r') as filehandle:
        array = filehandle.read().splitlines()
        filehandle.close()
    return array

def binToInt(str):
    temp = 0
    for i, n in enumerate(str):
        temp = temp + (int(n)*(2**i))
        # print(n, i)
    return temp

def main():
    diag = Diagnostics()
    data = getData(os.getcwd() + '/p3/data.txt')
    binLength = len(data[0])
    for i in data:
        diag.insertBinaryString(i)
    
    #puzzle part 1; eval the most common on every bit index-es
    diag.begin()
    index = 0
    gammaByteString = ''
    for index in range(binLength):
        binCount = diag.evalBinCount(index)
        if(binCount['1'] > binCount['0']):
            gammaByteString += '1'
        else:
            gammaByteString += '0'

    epsilonByteString = ''
    for index in range(binLength):
        binCount = diag.evalBinCount(index)
        if(binCount['1'] < binCount['0']):
            epsilonByteString += '1'
        else:
            epsilonByteString += '0'

    print(binToInt(reversed(gammaByteString)) * binToInt(reversed(epsilonByteString)))

    #puzzle part 2; eval the most common on every bit index-es
    #oxyScrubber Rating
    index = 0
    shouldWeNotStopYet = True
    while shouldWeNotStopYet:
        binCount = diag.evalBinCount(index)
        if(binCount['1'] >= binCount['0']):
            shouldWeNotStopYet = diag.removeBasedOnValOnIndex('0', index)
        else:
            shouldWeNotStopYet = diag.removeBasedOnValOnIndex('1', index)
        index += 1
        if index >= binLength: index = 0
    oxyRating = binToInt(reversed(diag.cache[0]))

    #co2Scrubber Rating
    diag.begin()
    index = 0
    shouldWeNotStopYet = True
    while shouldWeNotStopYet:
        binCount = diag.evalBinCount(index)
        if(binCount['0'] > binCount['1']):
            shouldWeNotStopYet = diag.removeBasedOnValOnIndex('0', index)
        else:
            shouldWeNotStopYet = diag.removeBasedOnValOnIndex('1', index)
        index += 1
        if index >= binLength: index = 0
    co2Rating = binToInt(reversed(diag.cache[0]))

    print(oxyRating * co2Rating)
if __name__ == "__main__":
    main()