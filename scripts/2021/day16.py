class Puzzle:

    def __init__(self, verbose):
        self.data = None
        self.cache = None
        self.verbose = verbose

    def appendData(self, data):
        self.data = data.splitlines()[0]

    class Packet:
        def __init__(self, hexString):
            self.string = hexString
            self.bits = ''

        def initIter(self):
            temp = ''
            for i in self.string:
                temp += str(bin(int(i, 16))[2:].zfill(4))
            self.bits = [i for i in temp]

        def proc(self):
            self.cache = {'vers': [], 'tIDs': [], 'lIDs': [], 'ress': []}
            getPacketNum = 3
            while len(self.bits) > 0:
                tempBits = ''
                
                packetDict = {}

                # packet Version
                for _ in range(3):
                    try: tempBits += self.bits.pop(0)
                    except IndexError: pass
                packetDict['ver'] = int('0b' + tempBits, 2)
                tempBits = ''
                
                # packet operator ID
                for _ in range(3):
                    try: tempBits += self.bits.pop(0)
                    except IndexError: pass
                packetDict['tID'] = int('0b' + tempBits, 2)
                tempBits = ''
                # if packet id 4 use literal value
                if packetDict['tID'] == 4:
                    literalPackets = []
                    while True:
                        try: tempBits += self.bits.pop(0)
                        except IndexError: pass
                        if tempBits == '1':
                            tempBits = ''
                            for _ in range(4):
                                try: tempBits += self.bits.pop(0)
                                except IndexError: pass
                            literalPackets.append(tempBits)
                            tempBits = ''
                        else:
                            for _ in range(4):
                                try: tempBits += self.bits.pop(0)
                                except IndexError: pass
                            literalPackets.append(tempBits[1:])
                            tempBits = ''
                            break
                    packetDict['res'] = literalPackets
                else:
                
                    # packet length ID
                    try: tempBits += self.bits.pop(0)
                    except IndexError: pass
                    packetDict['lID'] = int('0b' + tempBits, 2)
                    tempBits = ''

                    if packetDict['lID'] == '0':
                        getPacketNum = 15
                    elif packetDict['lID'] == '1':
                        getPacketNum = 11

                    for _ in range(getPacketNum):
                        try: tempBits += self.bits.pop(0)
                        except IndexError: pass
                    packetDict['subLen'] = tempBits
                    tempBits = ''
                    
                    for _ in range(int('0b'+ packetDict['subLen'], 2)):
                        try: tempBits += self.bits.pop(0)
                        except IndexError: pass
                    packetDict['res'] = tempBits
                    
                    tempBits = ''
                    
                self.cache['vers'].append(packetDict['ver'])
                self.cache['tIDs'].append(packetDict['tID'])
                self.cache['lIDs'].append(packetDict['lID'])
                self.cache['ress'].append(packetDict['res'])
                break
            print(self.cache)


    def part1(self):
        packet = self.Packet(self.data)
        self.dump(packet.initIter())
        packet.proc()
        return
        

    def part2(self):
        return None

    def run(self, part):
        if part == 1:
            self.result = self.part1()
        else:
            self.result = self.part2()


    def dump(self, stuff):
        if self.verbose:
            print(stuff)
        return

    def getResult(self):
        return self.result

if __name__ == "__main__":
    print('no')