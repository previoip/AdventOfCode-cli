import os, requests

def puzzle1():
    file = "data.txt"
    array = ''
    temp = [0, 0]
    count = 0

    if not os.path.exists(file):
        with open(os.getcwd() + "\p1\data.txt", 'r') as filehandle:
            array = filehandle.read().splitlines()
            filehandle.close()

    for i in array:
        temp[1] = temp[0]
        temp[0] = int(i)
        if(temp[1] > temp[0]):
            count += 1

    print(count)

if __name__ == "__main__":
    puzzle1()