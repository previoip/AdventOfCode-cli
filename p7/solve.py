import os
# main func
def getData(path):
    array = []
    with open(path, 'r') as filehandle:
        array = filehandle.read().split(',')
        filehandle.close()
    return array

def main():
    part = '2'
    data = getData(os.getcwd() + '/p7/data.txt')
    data = [int(i) for i in data]
    maxPos = max(data)
    minPos = min(data)
    fuelCosts = 0
    fuelCost = 0
    lowest = 1e19
    for est in range(minPos, maxPos):
        for currentPos in data:
            currentCost = 0
            for i in range(abs(est - currentPos)):
                currentCost += (1 if part == '1' else i+1) 
            fuelCosts += currentCost
            currentCost = 0
        if(fuelCost < lowest):
            lowest = fuelCost
        fuelCosts = 0
    print(lowest)


if __name__ == "__main__":
    main()