import unittest
import cycle
import collections
import parameterized


mem1 = [[1, 4],
        [2, 5],
        [3, 6]]
new_my1 = collections.defaultdict(lambda: "",
                                  {0: "3", 1: "26", 2: "15", 3: "4"})
new_my3 = collections.defaultdict(lambda: "",
                                  {0: "1", 1: "24", 2: "35", 3: "6"})
mem2 = [[1, 2],
        [3, 4]]
new_my2 = collections.defaultdict(lambda: "", {0: "", 1: "3", 2: "14", 3: "2"})
new_my4 = collections.defaultdict(lambda: "", {0: "", 1: "1", 2: "32", 3: "4"})


class TestSequence(unittest.TestCase):
    @parameterized.parameterized.expand([
        [mem1, new_my1],
        [mem2, new_my2]
    ])
    def test_right_diag(self, mem, resdict):
        self.assertEqual(cycle.one_diag(mem), resdict)

    @parameterized.parameterized.expand([
        [mem1, new_my3],
        [mem2, new_my4]
    ])
    def test_left_diag(self, mem, expected):
        self.assertEqual(cycle.another_diag(mem), expected)
