import os

# main func
def getData(path):
    array = []
    with open(path, 'r') as filehandle:
        array = filehandle.read().split(',')
        filehandle.close()
    return array



def example_main():
    # data = getData(os.getcwd() + '/p6/data.txt')
    # data = [int(i) for i in data]
    days = 30
    data = [1,2,6,4,3,4,2,0,4]
    
    index = 0
    while True:
        index += 1
        breedCount = data[index] / days
        
        # for i, n in enumerate(data):
        #     data[i] -= 1
        #     if data[i] < 0:
        #         data[i] = 6
        #         data.append(9)
        if(index >= days):
            break
    print(len(data))



def main():
    # data = getData(os.getcwd() + '/p6/data.txt')
    # data = [int(i) for i in data]
    days = 30
    current_data = [1,2,6,4,3,4,2,0,4]
    next_iteration = []
    
    index = 0
    while True:
        index += 1
        breedCount = data[index] / days
        
        
        if(index >= days):
            break
    print(len(data))


if __name__ == "__main__":
    main()