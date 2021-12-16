import os

def getData(path):
    array = []
    with open(path, 'r') as filehandle:
        array = filehandle.read().splitlines()
        filehandle.close()
    return array

def puzzle1_part1():
    array = ''
    temp = [0, 0]
    count = 0

    array = getData(os.getcwd() + '/p1/data.txt')
    
    for i in array:
        temp[1] = temp[0]
        temp[0] = int(i)
        if(temp[1] < temp[0]):
            count += 1

    return count - 1

def puzzle1_part2():
    array = getData(os.getcwd() + '/p1/data.txt')
    temp = [0, 0]
    count = 0
    
    for index in range(len(array)-2):
        temp[1] = temp[0]
        temp[0] = int(array[index]) + int(array[index+1]) + int(array[index+2])
        if(temp[1] < temp[0]):
            count += 1

    return count - 1

if __name__ == "__main__":
    count = puzzle1_part2()
    print(count)