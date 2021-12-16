import os
# puzzle8_part1 func

digits = {

    '1': ['cf', 2],
    '7': ['acf', 3],
    '4': ['bcdf', 4],
    '8': ['abcdefg', 7],

    '0': ['abcefg', 6], 
    '6': ['abdefg', 6],
    '9': ['abcdfg', 6],

    '2': ['acdeg', 5],
    '3': ['acdfg', 5],
    '5': ['abdfg', 5],}

def removeSubstr(setString, subsetString):
    returnString = setString
    for letter in subsetString:
        returnString = returnString.replace(letter, '')
    return returnString

def getData(path):
    array = []
    with open(path, 'r') as filehandle:
        array = filehandle.read().splitlines()
        filehandle.close()
    return array

def puzzle8_part1():
    data = getData(os.getcwd() + '/p8/data.txt')
    count = 0
    for line in data:
        [ _ , output] = line.split(' | ')
        for i in output.split(' '):
            if len(i) == 2 or len(i) == 3 or len(i) == 4 or len(i) == 7:
                count += 1
    print(count)

def puzzle8_part2():
    data = ['beacf afbd bcead cgefa ecdbga efb gbfdeac ecgfbd acbdfe fb | bf efb bgecdfa egcfa']
    # data = getData(os.getcwd() + '/p8/data.txt')
    
    outputSum = 0
    
    """
    knownDigits = {
        '1': ['cf', 2],
        '7': ['acf', 3],
        '4': ['bcdf', 4],
        '8': ['abcdefg', 7],
    }
    """
    
    for line in data:
        [unique, output] = line.split(' | ')
        splitUnique = unique.split(' ')
        confirmedDigits = {}
        for uniqueItem in splitUnique:
            if len(uniqueItem) == digits['1'][1]:
                confirmedDigits['1'] = uniqueItem
            elif len(uniqueItem) == digits['7'][1]:
                confirmedDigits['7'] = uniqueItem
            elif len(uniqueItem) == digits['4'][1]:
                confirmedDigits['4'] = uniqueItem
            elif len(uniqueItem) == digits['8'][1]:
                confirmedDigits['8'] = uniqueItem

        print(confirmedDigits)

        temp_segmentCharMap = {}
        # segment a
        temp_segmentCharMap[removeSubstr(confirmedDigits['7'], confirmedDigits['1'])] = 'a'
        
        # segment f
        letter_f = unique[0]
        temp_word = ''
        for i in unique:
            letter_f = removeSubstr(i, temp_word)
            temp_word = i
        temp_segmentCharMap[letter_f] = 'f'

        #segment c
        temp_segmentCharMap[confirmedDigits['1'].replace(letter_f, '')] = 'c'
        
        # segment d
        letter_eg = removeSubstr(confirmedDigits['8'], confirmedDigits['1'] + confirmedDigits['4'] + confirmedDigits['7'])
        onesWithSixLetters = [i for i in splitUnique if len(i) == 6]
        temp_word = onesWithSixLetters[len(onesWithSixLetters) - 1]
        letter_d = ''
        for i in onesWithSixLetters:
            letter_d = removeSubstr(i, temp_word + letter_eg)
            temp_word = i 
        temp_segmentCharMap[letter_d] = 'd'

        # segment b
        onesWithFiveLetters = [i for i in splitUnique if len(i) == 6]
        temp_word = onesWithFiveLetters[len(onesWithFiveLetters) - 1]
        letter_b = ''
        for i in onesWithFiveLetters:
            letter_b = removeSubstr(i, temp_word + letter_eg)
            temp_word = i
        print(letter_b)
        print({k: v for k, v in sorted(temp_segmentCharMap.items(), key=lambda item: item[1])})


        # splitOutput = output.split(' ')


if __name__ == "__main__":
    puzzle8_part2()