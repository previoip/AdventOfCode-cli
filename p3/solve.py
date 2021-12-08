import os

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

def puzzle3_part1():
    array = []
    tempBit_one = [0 for _ in range(12)]
    tempBit_zero = [0 for _ in range(12)]
    gammaRate = 0
    epsilonRate = 0
    totalPower = 0
    array = getData(os.getcwd() + "\p3\data.txt")

    for byteString in array:
        for i, bit in enumerate(byteString):
            if bit == '0' :
                tempBit_zero[i] += 1
            else:
                tempBit_one[i] += 1

    byteValue = ''

    for i, val in enumerate(tempBit_one):
        if(val > tempBit_zero[i]):
            byteValue += '1'
        else:
            byteValue += '0'

    # gammaRate = binToInt(reversed(i[:-7])) #most sig 5 bits
    # epsilonRate = binToInt(i[5:]) #least sig 7 bits

    gammaByteValue = byteValue[::-1]
    epsilonByteValue = ''.join(['0' if i == '1' else '1' for i in byteValue])[::-1]
    print('part 1 :')
    print('byte string: {}; gamma byte string: {} epsilon byte string:{}'.format(byteValue, gammaByteValue, epsilonByteValue))
    
    gammaRate = binToInt(gammaByteValue)
    epsilonRate = binToInt(epsilonByteValue)
    
    print('gamma rate: {}, epsilon rate: {}, total power consumption: {}\n'.format(gammaRate, epsilonRate, gammaRate * epsilonRate))

    # print('abcdefghijkl'[:-7])
    # print('abcdefghijkl'[5:])

def puzzle3_part2():


    bitLookup_oxy = ''
    bitLookup_cox = ''

    def oxygenRatingAlgo():
        oxyByteString = ''
        # oxygen scrubber rating
        index = 0
        score = [0,0]
        temp_oxy = getData(os.getcwd() + "\p3\data.txt")
        
        while True:
            for bitValue in temp_oxy:
                if(bitValue[index] == '1'):
                    score[1] += 1
                else:
                    score[0] += 1
            
            # print(score)

            if(score[1] >= score[0]):
                bitLookup_oxy = '1'
            else:
                bitLookup_oxy = '0'

            score = [0,0]
            for byteString in temp_oxy:
                if(byteString[index] != bitLookup_oxy):
                    # print(byteString)
                    temp_oxy.remove(byteString)
                else:
                    oxyByteString = byteString

            index += 1
            index = index % len(temp_oxy[0])

            if(len(temp_oxy) <= 1):
                break
        return oxyByteString


    def carbonDioxideRatingAlgo():
        coxByteString = ''
        # oxygen scrubber rating
        temp_cox = getData(os.getcwd() + "\p3\data.txt")
        index = 0
        score = [0,0]
        
        while True:
            for bitValue in temp_cox:
                if(bitValue[index] == '1'):
                    score[1] += 1
                else:
                    score[0] += 1
            
            # print(score)

            if(score[1] >= score[0]):
                bitLookup_cox = '0'
            else:
                bitLookup_cox = '1'

            score = [0,0]
            for byteString in temp_cox:
                if(byteString[index] != bitLookup_cox):
                    temp_cox.remove(byteString)
                else:
                    coxByteString = byteString

            index += 1
            index = index % 12

            if(len(temp_cox) <= 1):
                break
        return coxByteString


    values = ( binToInt(oxygenRatingAlgo()[::-1]), binToInt(carbonDioxideRatingAlgo()[::-1]) )
    print('Oxygen Rating (bin): {}'.format(oxygenRatingAlgo()))
    print('CO2 Rating (bin): {}'.format(carbonDioxideRatingAlgo()))
    print(values[0] * values[1])
    # print('Life support rating: {}'.format( binToInt(coxByteString[::-1]) * binToInt(oxyByteString[::-1]) ))

if __name__ == "__main__":
    puzzle3_part2()