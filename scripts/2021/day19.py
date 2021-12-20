import re

class Puzzle:
    # Point Cloud Scans
    class NewScanner:
        def __init__(self):
            self.beacons = []
            self.center_of_mass = None

        def addBeacons(self, coord):
            (x,y,z) = (0,0,0)
            if len(coord) == 2:
                (x,y) = coord
            else:
                (x,y,z) = coord
            self.beacons.append([x,y,z])
        
        def eval_scanner_to_beacons_center_of_mass(self):
            lx = [i[0] for i in self.beacons]
            ly = [i[1] for i in self.beacons]
            lz = [i[2] for i in self.beacons]

            x = sum(lx)/len(lx)
            y = sum(ly)/len(ly)
            z = sum(lz)/len(lz)

            self.center_of_mass = (x,y,z)
    # main funcs
        def transform_translate(self, coord = (0,0,0)):
            for i, item in enumerate(self.beacons):
                self.beacons[i][0] = self.beacons[i][0] + coord[0]
                self.beacons[i][1] = self.beacons[i][1] + coord[1]
                self.beacons[i][2] = self.beacons[i][2] + coord[2]

        def transform_rotate(self, ammountCW, axis = 'z'):
            (x0, y0, z0) = self.center_of_mass
            for i, item in enumerate(self.beacons):
                (xt, yt, zt) = (self.beacons[i][0] - x0, self.beacons[i][1] - y0, self.beacons[i][2] - z0)
                if axis == 'z':
                    xr = xt + x0
                    yr = yt + y0
                    zr = zt + z0

                    self.beacons[i][0] = xr
                    self.beacons[i][1] = yr
                    self.beacons[i][2] = zr
                    pass

    def part1(self):
        # appends beacons and evaluate its nodes center of mass
        self.scannerCollections = []
        for i in self.data.items():
            scanner = self.NewScanner()
            for beaconCoord in i[1]:
                scanner.addBeacons(beaconCoord)
            scanner.eval_scanner_to_beacons_center_of_mass()
            self.scannerCollections.append(scanner)
        # translate transformmation to global 0,0,0 
        for i, sc in enumerate(self.scannerCollections):
            com = sc.center_of_mass
            (dx, dy, dz) = [0-i for i in com]
            print((dx, dy, dz))
            self.scannerCollections[i].transform_translate((dx, dy, dz))
            self.scannerCollections[i].eval_scanner_to_beacons_center_of_mass()
        
        for i, sc in enumerate(self.scannerCollections):
            print(sc.beacons)
            print(sc.center_of_mass)
        return None

    def part2(self):
        return None

    def appendData(self, data):
        pattern = r"(.+\r?\n)+(?=(\r?\n)?)"
        matches = re.finditer(pattern, data+'\n', re.MULTILINE)
        
        temp = {}
        for num, match in enumerate(matches):
            # temp[str(num)] = match.group().splitlines()
            temp['scanner_'+str(num)] = [tuple(int(j) for j in i.split(',')) for i in match.group().splitlines()[1:]]
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