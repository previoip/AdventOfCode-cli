
class Register:
    def __init__(self, name):
        self.name = name
        self._v = 0

    @property
    def v(self):
        return self._v

    @v.setter
    def v(self, value):
        self._v = value

class CounterEventListener:
    def __init__(self, ptr, listen_at_cycles=[20]):
        self.counter = 1
        self.ptr = ptr
        self.listen_at_cycles = listen_at_cycles

        self.pixel_buffer = [[None for _ in range(40)] for j in range(5)]
        
        self.global_counter = 1
        self.cache_stack = []
        self.goofy_ahh = False


class Puzzle:

    def part1(self):
        data = list(self.data)
        stack = []
        reg = Register('X')
        reg.v = 1
        listen_at_c = [20, 40]
        
        class ListenAtDumbCycles(CounterEventListener):
            def __init__(self, ptr, listen_at_cycles):
                super().__init__(ptr, listen_at_cycles)
        
            def incr(self):
                self.counter += 1
                self.global_counter += 1
                if self.counter % self.listen_at_cycles[0] == 0:
                    if len(self.listen_at_cycles) > 1:
                        self.counter = 0
                        self.listen_at_cycles.pop(0)
                    self.cache_stack.append(self.ptr.v * self.global_counter)
                    if self.goofy_ahh: print(sum(self.cache_stack), self.ptr.v, self.global_counter, self.ptr.v * self.global_counter, sep='\t')
                    if self.goofy_ahh: print('Stack: ', self.cache_stack)

            def res(self):
                return sum(self.cache_stack)

        counter = ListenAtDumbCycles(reg, listen_at_c)
        counter.goofy_ahh = self.verbose
        

        print('data length: ', len(data))
        while data:
            stdin = data.pop(0)

            instr = stdin[:4]
            argv = stdin[5:]

            if instr == 'noop':
                counter.incr()
            elif instr == 'addx':
                stack.append(int(argv))
                counter.incr()
                reg.v += stack.pop(0)
                counter.incr()
        return counter.res()

    def part2(self):

        data = list(self.data)
        stack = []
        reg = Register('X')
        reg.v = 1
        listen_at_c = [40]

        class ListenPixelBuffer(CounterEventListener):
            def __init__(self, ptr, listen_at_cycles):
                super().__init__(ptr, listen_at_cycles)
                self.row_len = 6
                self.cache_stack = [[False for _ in range(listen_at_cycles[0])] for j in range(self.row_len)] # pixel buffer
                self.cache_stack[0][0] = True
                self.buffer_row_index = 0
                self.global_counter = 0

            def incr(self):

                sprite_index = self.ptr.v
                pixel_value = True

                if self.global_counter > (self.listen_at_cycles[0]*self.row_len)-1: return
                buffer_col_index = self.global_counter % self.listen_at_cycles[0]

                cuh = []
                for d in [-1, 0, 1]:
                    sprite_index_offset = sprite_index + d
                    if sprite_index < 0 or sprite_index > self.listen_at_cycles[0]:
                        continue
                    print(sprite_index_offset, end=' ')
                    cuh.append(sprite_index_offset == buffer_col_index)
                if self.goofy_ahh: print(cuh, self.ptr.v) 
                pixel_value = any(cuh)
                
                if self.global_counter and buffer_col_index == 0:
                    self.buffer_row_index += 1
                self.cache_stack[self.buffer_row_index][buffer_col_index] = pixel_value

                
                self.global_counter += 1

                if self.goofy_ahh: print('\n'+'\n'.join([''.join(['#' if j else '.' for j in i]) for i in self.cache_stack]))



            def res(self):
                return '\n'+'\n'.join([''.join(['#' if j else ' ' for j in i]) for i in self.cache_stack])


        counter = ListenPixelBuffer(reg, listen_at_c)
        counter.goofy_ahh = self.verbose

        print('data length: ', len(data))
        while data:
            stdin = data.pop(0)

            instr = stdin[:4]
            argv = stdin[5:]

            if instr == 'noop':
                counter.incr()
            elif instr == 'addx':
                counter.incr()
                stack.append(int(argv))
                counter.incr()
                reg.v += stack.pop(0)
        return counter.res()
    def appendData(self, data):
        # data preprocessor
        self.data = [i for i in data.splitlines() if i]

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