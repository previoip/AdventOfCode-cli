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
            return ''.join(self.bits)

        def proc(self):
            self.cache = {'vers': [], 'tIDs': [], 'lIDs': [], 'ress': []}
            getPacketNum = 3

            while len(self.bits) > 0:
                tempBits = ''
                packetDict = {'ver': 0, 'tID': 0, 'lID': 0, 'res': None}
                # packet Version
                for _ in range(3):
                    try: tempBits += self.bits.pop(0)
                    except IndexError: pass
                    try: packetDict['ver'] = int('0b' + tempBits, 2)
                    except ValueError: pass
                tempBits = ''

                # packet operator ID
                for _ in range(3):
                    try: tempBits += self.bits.pop(0)
                    except IndexError: pass
                try: packetDict['tID'] = int('0b' + tempBits, 2)
                except ValueError: pass
                tempBits = ''

                # if packet id 4, use literal value
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
                
                # otherwise use operator
                else:
                    literalPackets = []
                    tempBits = ''
                    try: tempBits += self.bits.pop(0)
                    except IndexError: pass
                    try: packetDict['lID'] = tempBits
                    except ValueError: pass

                    tempBits = ''
                    lenSubPacket = 0
                    # first operator, 2 subpackets, 11 bits first sub
                    if packetDict['lID'] == '0':
                        getPacketNum = 15
                        for _ in range(getPacketNum):
                            try: tempBits += self.bits.pop(0)
                            except IndexError: pass
                        try: lenSubPacket = int('0b' + tempBits, 2)
                        except ValueError: pass
                        tempBits = ''

                        for _ in range(11):
                            try: tempBits += self.bits.pop(0)
                            except IndexError: pass
                        try: literalPackets.append(tempBits)
                        except ValueError: pass
                        tempBits = ''

                        for _ in range(lenSubPacket - 11):
                            try: tempBits += self.bits.pop(0)
                            except IndexError: pass
                        try: literalPackets.append(tempBits)
                        except ValueError: pass
                        packetDict['res'] = literalPackets

                    # second operator, n subpackets on lenght
                    elif packetDict['lID'] == '1':
                        getPacketNum = 11

                        for _ in range(getPacketNum):
                            try: tempBits += self.bits.pop(0)
                            except IndexError: pass
                        try: lenSubPacket = int('0b' + tempBits, 2)
                        except ValueError: pass
                        for _ in range(lenSubPacket):
                            tempBits = ''
                            for _ in range(11):
                                try: tempBits += self.bits.pop(0)
                                except IndexError: pass
                            try: literalPackets.append(tempBits)
                            except ValueError: pass
                        packetDict['res'] = literalPackets
                    else:
                        pass

                self.cache['vers'].append(packetDict['ver'])
                self.cache['tIDs'].append(packetDict['tID'])
                self.cache['lIDs'].append(packetDict['lID'])
                self.cache['ress'].append(packetDict['res'])



    def part1(self):
        packet = self.Packet(self.data)
        self.dump(packet.initIter())
        packet.proc()
        self.dump(packet.cache)
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