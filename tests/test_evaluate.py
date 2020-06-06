import unittest
from unittest.mock import Mock
import evaluate
import parameterized
import multiprocessing as mp


memory1 = [
    [0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0]]


class TestSequence(unittest.TestCase):

    @parameterized.parameterized.expand(
        [parameterized.param(memory1)]
    )
    def test_victory_check(self, mem):
        res = evaluate.main(mem)
        self.assertEqual(1350, res)
