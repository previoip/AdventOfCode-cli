import os

def getData(path):
    array = []
    with open(path, 'r') as filehandle:
        array = filehandle.read().splitlines()
        filehandle.close()
    return array

def puzzle2_part1():
    array = getData(os.getcwd() + "\p2\data.txt")
    vertical = 0
    horizontal = 0

    for i, item in enumerate(array):
        [command, step] = item.split(' ')
        
        if(command == 'up'):
            vertical = vertical + int(step)
        elif(command == 'down'):
            vertical = vertical - int(step)
        elif(command == 'forward'):
            horizontal = horizontal + int(step)
        
    print(vertical * horizontal)


def puzzle2_part2():
    array = getData(os.getcwd() + "\p2\data.txt")
    vertical = 0
    horizontal = 0
    aim = 0

    for i, item in enumerate(array):
        [command, step] = item.split(' ')
        
        if(command == 'up'):
            aim = aim - int(step)
        elif(command == 'down'):
            aim = aim + int(step)
        elif(command == 'forward'):
            horizontal = horizontal + int(step)
            vertical = vertical + (aim * int(step))
        
    print(vertical * horizontal)

    

if __name__ == "__main__":
    puzzle2_part2()