class Puzzle:
    class Packet:
        def __init__(self, packetStr):
            self.packet = [i for i in packetStr]
            self.metadata = {'versions': [], 'typeIDs': [], 'lengthIDs': [], 'res': []}

        def get(self):
            try:
                return str(bin(int(self.packet.pop(0), 16))[2:].zfill(4))
            except IndexError:
                return '0000'

        def getLen(self):
            return len(self.packet)
        
        def append_meta(self, metadata):
            self.metadata['versions'].append(metadata['v'])
            self.metadata['typeIDs'].append(metadata['t'])
            self.metadata['lengthIDs'].append(metadata['l'])
            self.metadata['res'].append(metadata['r'])
        
        def get_versionsSum(self):
            return sum(self.metadata['versions'])

    class Decoder:
        def __init__(self):
            self.res = ''
            self.cache = None
        
        def getVersion(self, bits):
            return (bits[3:], int(bits[:3], 2))

        def getTypeID(self, bits):
            return (bits[3:], int(bits[:3], 2))

        def getLiteral(self, bits):
            return (bits[5:], ''.join([bits[i+1] for i in range(4)]), int(bits[0], 2))

        def getLengthID(self, bits):
            return (bits[1:], int(bits[:1], 2))

        def getSublength(self, bits, lenght):
            return (bits[lenght:], int(bits[:lenght], 2))
        
        def getSubLenLiteral(self, bits, lenght):
            # return (bits[lenght:], int(bits[:lenght], 2))
            return (bits[lenght:], bits[:lenght])



        def flush(self):
            return ('', None)

    # main funcs
    def part1(self):
        packet = self.Packet(self.data)
        decoder = self.Decoder()
        
        pstr = ''
        #     while len(pstr)<=3:
        while packet.getLen():
        # for i in range(3):
            meta = {'v': None, 't': None, 'l':None, 'r':None}
            try:
                if packet.packet[0] == '0':
                    while packet.packet[0] == '0':
                        packet.packet.pop(0)
            except IndexError:
                pass

            else:
                while len(pstr)<=3:
                    pstr += packet.get()
                (pstr, meta['v']) = decoder.getVersion(pstr)

                while len(pstr)<=3:
                    pstr += packet.get()
                (pstr, meta['t']) = decoder.getVersion(pstr)

                if meta['t'] == 4:
                    temp = []
                    nt = ''
                    while True:
                        while len(pstr)<5:
                            pstr += packet.get()
                        pstr, n, s= decoder.getLiteral(pstr)
                        nt += n
                        if s == 0:
                            break
                    meta['r'] = nt

                else:
                    pstr += packet.get()
                    (pstr, meta['l']) = decoder.getLengthID(pstr)

                    if meta['l'] == 0:
                        while len(pstr)<15:
                            pstr += packet.get()
                        (pstr, lenght) = decoder.getSublength(pstr, 15)

                        temp = []
                        while len(pstr)<lenght:
                            pstr += packet.get()
                        (pstr, sub) = decoder.getSubLenLiteral(pstr, 11)
                        temp.append(sub)
                        (pstr, sub) = decoder.getSubLenLiteral(pstr, lenght-11)
                        temp.append(sub)

                        meta['r'] = temp

                    elif meta['l'] >= 1:
                        while len(pstr)<11:
                            pstr += packet.get()
                        (pstr, lenght) = decoder.getSublength(pstr, 11)
                        
                        temp = []
                        for _ in range(lenght):
                            while len(pstr)<11:
                                pstr += packet.get()
                            (pstr, sub) = decoder.getSubLenLiteral(pstr, 11)
                            temp.append(sub)

                        meta['r'] = temp
                
                if self.verbose: print(pstr)
                (pstr, _) = decoder.flush()
                packet.append_meta(meta)

        if self.verbose:
            print(packet.metadata)
            print(packet.packet)
            print(packet.get_versionsSum())

        return None

    def part2(self):
        return None

    def appendData(self, data):
        self.data = data.splitlines()[0]

    def dump(self):
        print('Dumping data')
        print(self.data)
        # print(self.result)
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