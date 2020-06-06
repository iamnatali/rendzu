from collections import defaultdict
import re


def print_memory(mem):
    d1 = mem.__len__()
    d2 = mem[0].__len__()
    for e in range(0, d1):
        for p in range(0, d2):
            print(str(mem[e][p])+" ", end='')
        print()


def main(memory, line):
    d = memory.__len__()
    my_vert = defaultdict(lambda: "", {})
    my_hor = defaultdict(lambda: "", {})
    for e in range(0, d):
        a = "".join(map(str, memory[e]))
        my_hor[e] = a
        for n in range(0, d):
            my_vert[n] += str(memory[e][n])
    y12 = get_filled_positions(my_vert)
    filled_points = y12[2]
    x12 = get_filled_positions(my_hor)
    new_memory = []
    y1 = y12[0] - line if y12[0] - line >= 0 else 0
    x1 = x12[0] - line if x12[0] - line >= 0 else 0
    y2 = y12[1] + 1+line if y12[1] + 1+line <= d else d
    x2 = x12[1] + 1+line if x12[1] + 1+line <= d else d
    yi = 0
    for y in range(y1, y2):
        new_memory.append([])
        for x in range(x1, x2):
            el = memory[y][x]
            new_memory[yi].append(el)
        yi += 1
    return new_memory, filled_points, x1, y1


def get_filled_positions(game_map):
    count = 0
    previously_l = re.compile(r'[^0]+0*[^0]+')
    l1 = re.compile(r'[^0]')
    d = game_map.__len__()
    min_hor = d
    max_hor = 0
    for u in game_map.values():
        catched = previously_l.search(u)
        catched1 = l1.search(u)
        allsymb = l1.findall(u)
        count += len(allsymb)
        if catched:
            start = catched.start()
            end = catched.end()
            if start < min_hor:
                min_hor = start
            if end > max_hor:
                max_hor = end
        elif catched1:
            start = catched1.start()
            end = catched1.end()
            if start < min_hor:
                min_hor = start
            if end > max_hor:
                max_hor = end
    return min_hor, max_hor-1, count
