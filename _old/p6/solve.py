import os, time

class LanterFish:
    def __init__(self, series, maxDays):
        self.initSeries = series
        self.maxDays = maxDays
        self.cache = []
        # self.total = len(self.initSeries)
        self.total = 0

    def iterSelf(self):
        lenght = len(self.initSeries)
        for ind, i in enumerate(self.initSeries):
            arr = [i]
            for _ in range(self.maxDays):
                for i, a in enumerate(arr):
                    temp = arr[i] - 1
                    if temp < 0:
                        arr[i] = 6
                        arr.append(9)
                    else:
                        arr[i] = temp
            self.total += len(arr)
            print('index:{}/{} -> {}'.format(ind+1, lenght, self.total))

    def iterSelfv2(self):
        lenght = len(self.initSeries)
        for ind, i in enumerate(self.initSeries):
            arr = [i]
            for _ in range(self.maxDays):
                for i, a in enumerate(arr):
                    temp = arr[i] - 1
                    if temp < 0:
                        arr[i] = 6
                        arr.append(9)
                        self.total += 1
                    else:
                        arr[i] = temp
            self.total += 1
            print('index:{}/{} -> {}'.format(ind+1, lenght, self.total))

    def iterSelfv3(self):
        lenght = len(self.initSeries)
        for ind, i in enumerate(self.initSeries):
            arr = [i]
            for _ in range(self.maxDays):
                for i, a in enumerate(arr):
                    temp = arr[i] - 1
                    if temp < 0:
                        arr[i] = 6
                        arr.append(9)
                        self.total += 1
                    else:
                        arr[i] = temp
            self.total += 1
            print('index:{}/{} -> {}'.format(ind+1, lenght, self.total))

    def dump(self):
        print('total: {}'.format(self.total))




# main func
def getData(path):
    array = []
    with open(path, 'r') as filehandle:
        array = filehandle.read().split(',')
        filehandle.close()
    return array


def example():
    # data = getData(os.getcwd() + '/p6/data.txt')
    # data = [int(i) for i in data]
    days = 128
    data = [3,4,3,1,2]
    arrLen = len(data)

    fishes = LanterFish(data, days)
    print('--------------')
    startTime = time.time()
    fishes.iterSelf()
    print('------- Ver 1, days: {}, initAmmount:{}, runtime: {} secs'.format(days, arrLen, time.time() - startTime))
    
    fishes = LanterFish(data, days)
    startTime = 0
    startTime = time.time()
    fishes.iterSelfv2()
    print('------- Ver 2, days: {}, initAmmount:{}, runtime: {} secs'.format(days, arrLen, time.time() - startTime))

    fishes = LanterFish(data, days)
    startTime = 0
    startTime = time.time()
    fishes.iterSelfv3()
    print('------- Ver 3, days: {}, initAmmount:{}, runtime: {} secs'.format(days, arrLen, time.time() - startTime))


    fishes.dump()


def main():
    data = getData(os.getcwd() + '/p6/data.txt')
    data = [int(i) for i in data]
    days = 128
    fishes = LanterFish(data, days)
    fishes.iterSelf()
    fishes.dump()
    


if __name__ == "__main__":
    example()