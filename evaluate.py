from collections import defaultdict
import cycle
import re

figures = [r'[^2]2{3}[^2]',
           r'[^1]1{3}[^1]',
           r'02{4}0',
           r'12{4}0',
           r'02{4}1',
           r'[^1]1{4}[^1]',
           r'[^2]2{5}[^2]',
           r'[^1]1{5}[^1]',
           r'[^1]1{2}[^1]',
           r'[^2]2{2}[^2]',
           r'[^1]1{2}01[^1]',
           r'[^1]101{2}[^1]',
           r'[^1]1{3}01[^1]',
           r'[^1]1{2}01{2}[^1]',
           r'[^1]101{3}[^1]',
           r'[^1]101[^1]']

table_score = 0
names = {
    21: 170,
    61: 0,
    41: 30,
    28: 240,
    68: 0,
    48: 40,
    35: 1350,
    75: 0,
    55: 350,
    14: 20,
    54: 0,
    34: 20,
    60: -1000,
    74: 0,
    67: -60,
    80: -1800,
    94: 0,
    87: -80,
    100: -1900,
    114: 0,
    107: -1900,
    40: -45,
    47: -45}


class Figure:
    def __init__(self, type, mo):
        self.figure = type
        self.start = mo.start
        self.end = mo.end


def get_hash(st):
    a = 0
    for e in st:
        n = int(e)
        if n == 2:
            a += n*10
        else:
            a += n*7
    return a


def compare(game_map):
    for e in game_map.values():
        for h in figures:
            r = re.finditer(h, e)
            for elem in r:
                num = get_hash(elem.group())
                global table_score
                table_score += names[num]


def get_slices(memory):
    d1 = memory.__len__()
    d2 = len(memory[0])
    my_vert = defaultdict(lambda: "", {})
    my_hor = defaultdict(lambda: "", {})
    for e in range(0, d1):
        a = "".join(map(str, memory[e]))
        my_hor[e] = a
        for n in range(0, d2):
            my_vert[n] += str(memory[e][n])
    od = cycle.one_diag(memory)
    ad = cycle.another_diag(memory)
    return my_vert, my_hor, od, ad


def main(memory):
    global table_score
    table_score = 0
    for e in get_slices(memory):
        compare(e)
    return table_score
