class Puzzle:
    def removeSubstr(setString, subsetString):
        returnString = setString
        for letter in subsetString:
            returnString = returnString.replace(letter, '')
        return returnString
    
    # main funcs
    def part1(self):
        count = 0
        for line in self.data:
            [ _ , output] = line.split(' | ')
            for i in output.split(' '):
                if len(i) == 2 or len(i) == 3 or len(i) == 4 or len(i) == 7:
                    count += 1
        return count

    def part2(self):
        return None
        outputSum = 0
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
        '5': ['abdfg', 5],
        
        }
        """
        knownDigits = {
            '1': ['cf', 2],
            '7': ['acf', 3],
            '4': ['bcdf', 4],
            '8': ['abcdefg', 7],
        }
        """
    
        for line in self.data:
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
            temp_segmentCharMap[self.removeSubstr(confirmedDigits['7'], confirmedDigits['1'])] = 'a'
            
            # segment f
            letter_f = unique[0]
            temp_word = ''
            for i in unique:
                letter_f = self.removeSubstr(i, temp_word)
                temp_word = i
            temp_segmentCharMap[letter_f] = 'f'

            #segment c
            temp_segmentCharMap[confirmedDigits['1'].replace(letter_f, '')] = 'c'
            
            # segment d
            letter_eg = self.removeSubstr(confirmedDigits['8'], confirmedDigits['1'] + confirmedDigits['4'] + confirmedDigits['7'])
            onesWithSixLetters = [i for i in splitUnique if len(i) == 6]
            temp_word = onesWithSixLetters[len(onesWithSixLetters) - 1]
            letter_d = ''
            for i in onesWithSixLetters:
                letter_d = self.removeSubstr(i, temp_word + letter_eg)
                temp_word = i 
            temp_segmentCharMap[letter_d] = 'd'

            # segment b
            onesWithFiveLetters = [i for i in splitUnique if len(i) == 6]
            temp_word = onesWithFiveLetters[len(onesWithFiveLetters) - 1]
            letter_b = ''
            for i in onesWithFiveLetters:
                letter_b = self.removeSubstr(i, temp_word + letter_eg)
                temp_word = i
            print(letter_b)
            print({k: v for k, v in sorted(temp_segmentCharMap.items(), key=lambda item: item[1])})

    def appendData(self, data):
        temp = data.splitlines()
        self.data = temp

    def dump(self):
        print('Dumping result')
        print(self.data)
        print(self.result)
        return

    # defaults
    def __init__(self, verbose):
        self.data = None
        self.cache = None
        self.verbose = verbose

    def run(self, part):
        if part == 1:
            self.result = self.part1()
        else:
            self.result = self.part2()

        if self.verbose:
            self.dump()

    def getResult(self):
        return self.result

if __name__ == "__main__":
    print("this shouldn't be ran as standalone script")
    pass