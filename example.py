import itertools
import evaluate
import cut
import sys


def key_func(ch):
    return ch.ancestor


def main(memory, que):
    wow = cut.main(memory, 2)
    mymemory = wow[0]
    deep = wow[1]-1
    root = Node("white", deep+1, mymemory)
    lists = []
    get_var(mymemory, root, lists, deep+1)
    while lists[0].depth != deep+1:
        f = sorted(lists, key=key_func)
        fathers = itertools.groupby(f, key_func)
        lists = []
        for k, g in fathers:
            if k.color == "black":
                kam = list(g)
                k.score += min(f.score for f in kam)
            else:
                kam = list(g)
                k.score += max(f.score for f in kam)
            lists.append(k)
    max_score = -sys.maxsize
    res_move = []
    for e in root.kids:
        if max_score < e.score:
            max_score = e.score
            res_move = copy_matrix(e.matrix)
    xi, yi = compare(mymemory, res_move)
    que.put(xi+wow[2])
    que.put(yi+wow[3])


def compare(mem1, mem2):
    d1 = len(mem1)
    d2 = len(mem1[0])
    for x in range(0, d1):
        for y in range(0, d2):
            b = mem2[x][y]
            if mem1[x][y] != b:
                return y, x


def get_var(mem, father, children, main_deep):
    d1 = mem.__len__()
    d2 = mem[0].__len__()
    depth = father.depth+1
    player = "black"
    if father.color == "black":
        player = "white"
    if depth == main_deep + 1 + 2:
        children.append(father)
        father.score = evaluate.main(father.matrix)
    else:
        if player == "black":
            for e in range(0, d1):
                for p in range(0, d2):
                    new_mem = copy_matrix(mem)
                    if new_mem[e][p] == 0:
                        new_mem[e][p] = 1
                        new_father1 = Node("black", depth, new_mem)
                        father.kids.append(new_father1)
                        new_father1.ancestor = father
                        get_var(new_mem, new_father1, children, main_deep)
        if player == "white":
            for e in range(0, d1):
                for p in range(0, d2):
                    new_mem = copy_matrix(mem)
                    if new_mem[e][p] == 0:
                        new_mem[e][p] = 2
                        new_father2 = Node("white", depth, new_mem)
                        father.kids.append(new_father2)
                        new_father2.ancestor = father
                        get_var(new_mem, new_father2, children, main_deep)


def copy_matrix(m):
    d1 = m.__len__()
    d2 = m[0].__len__()
    new_mem = [[0 for n in range(0, d2)] for n in range(0, d1)]
    for e in range(0, d1):
        for p in range(0, d2):
            new_mem[e][p] = m[e][p]
    return new_mem


class Node:
    def __lt__(self, other):
        return str(self) < str(other)

    def __init__(self, c, d, mat):
        self.matrix = mat
        self.kids = []
        self.depth = d
        self.ancestor = ""
        self.color = c
        self.score = 0

    def learn_father(self, node):
        self.ancestor = node

    def count_scores(self, node):
        self.score = node.score
