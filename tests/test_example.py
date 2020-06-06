import unittest
from unittest.mock import Mock
import example
import parameterized
import multiprocessing as mp


memory1 = [
    [1, 0, 0, 0, 0],
    [0, 1, 0, 0, 0],
    [0, 0, 1, 0, 0],
    [0, 0, 0, 1, 0],
    [0, 0, 0, 0, 1]]
memory2 = [
    [1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0]]


class TestSequence(unittest.TestCase):

    @parameterized.parameterized.expand(
        [parameterized.param(memory2, 0, 4)]
    )
    def test_victory_check(self, mem, x, y):
        q = mp.Queue()
        example.main(mem, q)
        x1 = q.get()
        y1 = q.get()
        self.assertEqual(y, x1)
        self.assertEqual(x, y1)
