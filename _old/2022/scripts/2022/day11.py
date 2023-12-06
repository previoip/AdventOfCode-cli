from collections import OrderedDict
from math import sqrt

class Monkey:
    def __init__(self, name, starting_items: list):
        self.name = name
        self.items = list(starting_items)
        self.worry_level = 0
        self.monkey_if_true = None
        self.monkey_if_false = None
        self.inspect_counter = 0
        self.inspect_argv = 1
        self.worry_denominator = 3
        self.modulo_divisors = 0 # <== i cheated quite a bit by looking at reddit
        self.inspecOperation = lambda x: x
        self.test_denominator = lambda x: bool(x)

        self.verbose = False

    def addItem(self, item):
        self.items.append(item)

    def inspect(self):
        while self.items:
            item = self.items.pop(0)
            self.inspect_counter += 1
            if self.verbose: print(f'\n{self.name} is inspecting item {item}', end=' ')

            worry_level = 0
            if self.inspect_argv == 'old':
                worry_level = self.inspecOperation(item, item)
            else:
                worry_level = self.inspecOperation(item, self.inspect_argv)
            

            if self.verbose: print(f'and your worry level has gone up to {worry_level}.')
            if self.worry_denominator > 1:
                worry_level = worry_level // self.worry_denominator
            worry_level_remainder = worry_level
            if self.verbose: print(f'{self.name} put down item and you relieved as your blood tension went down to {worry_level}.')
            worry_level_remainder = worry_level_remainder % self.modulo_divisors


            fucker = None
            if worry_level % self.test_denominator == 0:
                self.monkey_if_true.addItem(worry_level_remainder)
                fucker = self.monkey_if_true.name
            else:
                self.monkey_if_false.addItem(worry_level_remainder)
                fucker = self.monkey_if_false.name
            if self.verbose: print(f'Then {self.name} throw said item to {fucker}.')

    def __repr__(self):
        return f'{self.name}\titems: {", ".join(map(str, self.items))}\tthrowing their shit => if true to {self.monkey_if_true.name} \tif false to {self.monkey_if_false.name}'

    def __eq__(self, o):
        if isinstance(o, self.__class__):
            return self.name == o.name
        else:
            return self.name == o

class Puzzle:

    def part1(self):
        monkeys_list = []
        for monkey_name, attrs in self.data.items():
            monki = Monkey(monkey_name, attrs.get('Starting items'))
            monki.inspect_argv = attrs.get('Operation')[0]
            monki.inspecOperation = attrs.get('Operation')[1]
            monki.test_denominator = attrs.get('Test')
            monki.verbose = self.verbose
            monki.worry_denominator = 3
            monki.modulo_divisors = self.MOD
            monkeys_list.append(monki)

        # re-set for throw-item-ifs attr, by monkeys_list[index]
        for mong in monkeys_list:
            monkey_data = self.data[mong.name]
            mong.monkey_if_true = monkeys_list[monkey_data['If true']]
            mong.monkey_if_false = monkeys_list[monkey_data['If false']]

        if self.verbose: 
            for mong in monkeys_list: 
                print(mong)

        
        for n in range(20):
            for monkey in monkeys_list:
                monkey.inspect()
            if (n == 0 or (n + 1) % 5 == 0) and self.verbose:
                print(f'Round {n+1}:')
                for monkey in monkeys_list:
                    print(monkey.name, monkey.items)

        counter = [i.inspect_counter for i in monkeys_list]
        res = counter.pop(counter.index(max(counter))) #sheeeshh
        res *= counter.pop(counter.index(max(counter))) 
        return res

    def part2(self):

        monkeys_list = []
        for monkey_name, attrs in self.data.items():
            monki = Monkey(monkey_name, attrs.get('Starting items'))
            monki.inspect_argv = attrs.get('Operation')[0]
            monki.inspecOperation = attrs.get('Operation')[1]
            monki.test_denominator = attrs.get('Test')
            monki.worry_denominator = 1
            monki.modulo_divisors = self.MOD
            monki.verbose = self.verbose
            monkeys_list.append(monki)

        # re-set for throw-item-ifs attr, by monkeys_list[index]
        for mong in monkeys_list:
            monkey_data = self.data[mong.name]
            mong.monkey_if_true = monkeys_list[monkey_data['If true']]
            mong.monkey_if_false = monkeys_list[monkey_data['If false']]

        
        for n in range(10000):
            for monkey in monkeys_list:
                frac = len(monkey.items)/36
                le = int(16*frac)
                rg = 16-le
                print(monkey.name, '#'*le + '.'*rg, end='\t')
            print()

            for monkey in monkeys_list:
                monkey.inspect()
            print(n, end=' ')
        counter = [i.inspect_counter for i in monkeys_list]
        res = counter.pop(counter.index(max(counter))) #sheeeshh
        res *= counter.pop(counter.index(max(counter))) 
        return res
        # return [i.inspect_counter for i in monkeys_list]


    def appendData(self, data):

        self.MOD = []
        # data preprocessor
        data = [i for i in data.splitlines() if i]
        temp = []
        while data:
            line = data.pop(0)
            if line[:6] == 'Monkey':
                line = line.replace(':', '')
                temp.append(list())
            temp[-1].append(line)
        data = OrderedDict(map(lambda x: (x[0], [ [k.strip() for k in j.split(':')] for j in x[1:]]), temp))
        temp = data.copy()

        # parse attrs
        for k in temp.keys():
            data[k] = {}
            for n, (attr_k, attr_v) in enumerate(temp[k]):

                if attr_k == 'Starting items':
                    attr_v = list(map(int, attr_v.split(', ')))

                elif attr_k == 'Operation':
                    l_value, operand, r_value,  = attr_v[6:].split(' ')
                    assert l_value == 'old' # if not then fuck all
                    if operand == '+':
                        operand = lambda x, y: x + y
                    elif operand == '-':
                        operand = lambda x, y: x - y
                    elif operand == '*':
                        operand = lambda x, y: x * y
                    elif operand == '/': # just in case
                        operand = lambda x, y: x / y
                    if not r_value == 'old':
                        r_value = int(r_value)
                    attr_v = (r_value, operand)

                elif attr_k == 'Test':
                    attr_v = attr_v.split(' ')[-1]
                    attr_v = int(attr_v)
                    if attr_v not in self.MOD:
                        self.MOD.append(attr_v)
                elif attr_k.startswith('If'):
                    assert attr_v[:8] == 'throw to' # if not then for fucks sake
                    attr_v = attr_v[9:].split(' ')[-1]
                    attr_v = int(attr_v)

                data[k][attr_k] = attr_v
        
        mod = self.MOD[0]
        for i in self.MOD[1:]:
            mod *= i
        self.MOD = mod
        self.data = data

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
        print('Input monkeys: ')
        for d in self.data.keys():
            print(d, end='\t')
            for k, v in self.data[d].items():
                print(k, ':', v, end='\t')
            print()
        print(self.result)
        return

    def getResult(self):
        return self.result

if __name__ == "__main__":
    pass