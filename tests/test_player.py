import unittest
from unittest.mock import Mock
import rendzu_main
import parameterized


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
memory22 = [
    [1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0]]
memory3 = [
    [0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 1, 0],
    [0, 0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0, 0],
    [0, 1, 0, 0, 0, 0],
    [2, 0, 0, 0, 0, 0]]
memory4 = [
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0]]


class TestSequence(unittest.TestCase):

    @parameterized.parameterized.expand(
        [parameterized.param(memory1, True),
         parameterized.param(memory22, False),
         parameterized.param(memory3, True)]
    )
    def test_victory_check(self, mem, b_res):
        db = Mock()
        my_list = []
        db.insert_line = lambda color, x, y, base: my_list.append(
            [color, x, y, base])
        pl = rendzu_main.Player('black', db)
        pl.memory = mem
        res = pl.victory_check()
        self.assertEqual(res, b_res)

    @parameterized.parameterized.expand(
        [parameterized.param(memory1, memory4),
         parameterized.param(memory2, memory4),
         parameterized.param(memory3, memory4)]
    )
    def test_make_step(self, mem1, mem2):
        db = Mock()
        my_list = []
        db.insert_line = lambda color, x, y, base: my_list.append(
            [color, x, y, base])
        pl = rendzu_main.Player('black', db)
        pl.memory = mem1
        res = pl.make_step(0, 4, mem2)
        self.assertEqual(res, 'VICTORY white')
