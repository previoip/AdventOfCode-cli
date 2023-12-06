import os

class LanterFish:
    def __init__(self, series, maxDays):
        self.initSeries = series
        self.maxDays = maxDays
        self.cache = []
        # self.total = len(self.initSeries)
        self.total = 0

    def iterSelf(self):
        for i in self.initSeries:
            self.total += 1
            daysLeft = self.maxDays - i - 1
            arr = [6, 8]
            while daysLeft:
                daysLeft -= 1
                for i, v in enumerate(arr):
                    print(arr)
                    temp = arr[i] - 1
                    arr[i] = temp
                    if temp < 0:
                        self.total += 1
                        arr[i] = 6
                        arr.append(8)

    def dump(self):
        print(self.total)




# main func
def getData(path):
    array = []
    with open(path, 'r') as filehandle:
        array = filehandle.read().split(',')
        filehandle.close()
    return array


def example():
    days = 18
    data = [3,4,3,1,2]
    fishes = LanterFish(data, days)
    fishes.iterSelf()
    fishes.dump()


def main():
    # data = getData(os.getcwd() + '/p6/data.txt')
    # data = [int(i) for i in data]
    pass


if __name__ == "__main__":
    example()