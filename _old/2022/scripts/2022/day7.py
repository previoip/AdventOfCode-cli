class DirectoryNode:
    def __init__(self, name, isfile=False, size=0):
        self.name = name
        self.isfile = isfile
        self.size = size
        self.child = list()
        self.parent = None


    def appendChild(self, directory: "DirectoryNode"):
        if not self.isfile:
            directory.parent = self
            self.child.append(directory)
        else:
            raise RuntimeError(f'Not a directory: {self.name}')

    def abspath(self):
        r = []
        d = self
        while d.parent:
            r.append(d.name)
            d = d.parent
        return '/'+'/'.join(reversed(r)) + '\tsizeof: ' + str(self.size)

    def __repr__(self):
        return self.abspath()

    def __eq__(self, o):
        if isinstance(o, self.__class__):
            return o.name == self.name
        elif isinstance(o, str):
            return o == self.name
        else:
            return False

def traverseDir(dirNode, func=lambda x:x):
    # recursively traverse directory, map func call on each node
    for ch in dirNode.child:
        if not ch.isfile:
            traverseDir(ch, func)
        func(ch)

def mapFolderSize(node):
    node.parent.size += node.size

def mapResetFolderEvaluation(node):
    if not node.isfile:
        node.size = 0


class ScoreContainer:
    def __init__(self):
        self.sizes = []
    
    def addFolderScoreWithCond(self, node):
        if not node.isfile and node.size < 100000:
            self.sizes.append(node.size)

    def straightUpAddFolderScore(self, node):
        if not node.isfile:
            self.sizes.append(node.size)

    def getSum(self):
        return sum(self.sizes)



class Puzzle:

    def part1(self):
        traverseDir(self.directory_nodes, mapFolderSize)
        if self.verbose: 
            traverseDir(self.directory_nodes, print)
            print(self.directory_nodes)

        scoreContainer = ScoreContainer()
        traverseDir(self.directory_nodes, scoreContainer.addFolderScoreWithCond)

        # should i use _autoEval this has to be called before part2 evaluation
        traverseDir(self.directory_nodes, mapResetFolderEvaluation)
        return scoreContainer.getSum()


    def part2(self):
        traverseDir(self.directory_nodes, mapFolderSize)
        must_unused_space = 30000000
        leftover = (must_unused_space + self.directory_nodes.size - 70000000)
        if self.verbose: 
            print('leftover: ', leftover)

        scoreContainer = ScoreContainer()
        traverseDir(self.directory_nodes, scoreContainer.straightUpAddFolderScore)

        sorted_folder_sizes = list(sorted(scoreContainer.sizes))
        
        diff = 10e10
        for n in range(len(sorted_folder_sizes)):
            if n+1 >= len(sorted_folder_sizes):
                return None
            diff_curr = sorted_folder_sizes[n] - leftover
            diff_upper = sorted_folder_sizes[n+1] - leftover

            if self.verbose: print(sorted_folder_sizes[n+1], diff_curr, diff_upper)

            if abs(diff_curr) < diff_upper:
                # somewhere at some point the diff break even
                return sorted_folder_sizes[n+1]

        return None


    def appendData(self, data):
        # data preprocessor
        self.data = data.splitlines()

        data = [i for i in self.data if i]
        parent_dir = DirectoryNode('/')
        cwd = parent_dir
        data.pop(0)
        while data:
            cl = data.pop(0)

            # command-line call
            if cl.startswith('$'):
                cl = cl[2:]

                # change dir command
                if cl.startswith('cd'):
                    cl = cl[3:]
                    if cl.startswith('..'):
                        cwd = cwd.parent
                    else:
                        cwd = cwd.child[cwd.child.index(cl)]

                # list dir command
                elif cl.startswith('ls'):
                    # doesnt matter honestly owo
                    # d = d[3:]
                    pass

            else:
                cl = cl.split(' ')
                assert len(cl) == 2
                child = DirectoryNode(cl[1])

                if cl[0] == 'dir':
                    # is directory
                    cwd.appendChild(child)
                else:
                    # is file
                    child.size = int(cl[0])
                    child.isfile = True
                    cwd.appendChild(child)

        self.directory_nodes = parent_dir

    # defaults
    def __init__(self, verbose):
        self.data = None
        self.cache = None
        self.verbose = verbose
        self.stripData = True

    def run(self, part):
        if part == 2:
            self.result = self.part2()
        else:
            self.result = self.part1()

        if self.verbose:
            self.dump()

    def dump(self):
        print('Dumping...')
        print(self.data)
        print(self.result)
        return

    def getResult(self):
        return self.result

if __name__ == "__main__":
    pass