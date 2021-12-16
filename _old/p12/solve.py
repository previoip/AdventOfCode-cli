class CaveNode:

    def __init__(self):
        self.nodePoints = []
        self.nodeIndices = []
        self.nodeIndicesLen = []

    def insertPoints(self, point):
        [a, b] = point
        nodeIndex = 0
        isALowerCase = a.islower()
        isBLowerCase = b.islower()
        if a not in self.nodePoints:
            self.nodePoints.append(a)
            nodeIndex = self.nodePoints.index(a)
        else: 
            nodeIndex = self.nodePoints.index(a)

        # if not self.nodeIndices[nodeIndex]:
            # self.nodeIndices.insert(nodeIndex, []) -> raises index error
        try:
            _ = self.nodeIndices[nodeIndex]
        except IndexError:
            self.nodeIndices.insert(nodeIndex, [])

        try:
            _ = self.nodeIndicesLen[nodeIndex]
        except IndexError:
            self.nodeIndicesLen.insert(nodeIndex, 0)

        if b not in self.nodeIndices[nodeIndex]:
            self.nodeIndices[nodeIndex].append(b)
            # self.nodeIndicesLen[nodeIndex] = len(self.nodeIndices[nodeIndex])
            self.nodeIndicesLen[nodeIndex] += 1

    def getConn(self, pointer):
        index = self.nodePoints.index(pointer)
        return self.nodeIndices[index]
    
    def getAllPossiblePath(self, startingPoint='start', stopPoint='end'):
        tempNodePoints = self.nodePoints.copy()
        tempnodeIndices = self.nodeIndices.copy()
        point = startingPoint
        tempIndicies = []
        temp = []
        paths = []
        while True:
            nextIndex = tempNodePoints.index(point)
            nexttConnectionslength = len(tempnodeIndices[nextIndex])
            nexttConnections = iter(tempnodeIndices[nextIndex])
            curr = next(nexttConnections)
            connIndex = tempnodeIndices[nextIndex].index(curr)
            tempnodeIndices[nextIndex].pop(connIndex)
            if curr == 'start':
                pass
            elif curr == 'end':
                pass
            else:
                point = curr

    def dump(self):
        print('Name {is lowercase} [length] -> connected to')
        print('----------------------------------------------------')
        for i in self.nodePoints:
            index = self.nodePoints.index(i)
            conn = self.nodeIndices[index]
            length = self.nodeIndicesLen[index]
            padd = ''.join(['\t' for _ in range(2 - int(len(i + '----' if i.islower() else i) / 4))])
            printStr = 'Node {} {} [{}] -> {}'.format(
                i + ' {lc}' if i.islower() else i, 
                padd,
                length, 
                '['+'|'.join(conn) + ']'
                )
            print(printStr)


def main():
    finalInput = ['yb-start', 'de-vd', 'rj-yb', 'rj-VP', 'OC-de', 'MU-de', 'end-DN', 'vd-end', 'WK-vd', 'rj-de', 'DN-vd', 'start-VP', 'DN-yb', 'vd-MU', 'DN-rj', 'de-VP', 'yb-OC', 'start-rj', 'oa-MU', 'yb-de', 'oa-VP', 'jv-MU', 'yb-MU', 'end-OC']
    testInput = ['dc-end', 'HN-start', 'start-kj', 'dc-start', 'dc-HN', 'LN-dc', 'HN-end', 'kj-sa', 'kj-HN', 'kj-dc']
    initInput = ['start-A', 'start-b', 'A-c', 'A-b', 'b-d', 'A-end', 'b-end']
    programInput = [a.split('-') for a in initInput]

    caveNode = CaveNode()

    for i in programInput:
        caveNode.insertPoints(i)
        caveNode.insertPoints(reversed(i))
    # print(caveNode.getConn('start'))
    # print(caveNode.getConn('end'))
    caveNode.dump()
    
if __name__ == "__main__":
    main()