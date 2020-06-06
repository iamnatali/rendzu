from collections import defaultdict
import numpy as np


def one_diag(mem3):
    new_my = defaultdict(lambda: "", {})
    arr = np.array(mem3)
    sh = np.shape(arr)
    min = sh[0]
    max = sh[1]
    if min > max:
        t = max
        min = t
        max = min
    index = 0
    for e in range(-min, max):
        d = np.diagonal(arr, e)
        d1 = d.tolist()
        a = "".join(str(x) for x in d1)
        new_my[index] = a
        index += 1
    return new_my


def another_diag(mem3):
    new_my = defaultdict(lambda: "", {})
    arr = np.array(mem3)
    arr = arr[::-1]
    sh = np.shape(arr)
    min = sh[0]
    max = sh[1]
    if min > max:
        t = max
        min = t
        max = min
    index = 0
    for e in range(-min, max):
        d = np.diagonal(arr, e)
        d1 = d.tolist()
        a = "".join(str(x) for x in d1)
        new_my[index] = a
        index += 1
    return new_my
