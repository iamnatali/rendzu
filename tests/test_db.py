import unittest
import rendzu_main
import parameterized


class TestSequence(unittest.TestCase):
    def setUp(self):
        """мб нужна тестовая бд"""
        self.db = rendzu_main.Database()

    def tearDown(self):
        self.db.clear('mylog')
        self.db.clear('saved')

    @parameterized.parameterized.expand(
        ['saved',
         'mylog']
    )
    def test_insert_line(self, base):
        self.db.insert_line('black', 1, 2, base)
        self.assertEqual(self.db.is_empty(base), False)
        self.db.clear(base)
        self.assertEqual(self.db.is_empty(base), True)

    def test_color(self):
        self.db.insert_line('black', 1, 2, 'saved')
        self.assertEqual(self.db.is_empty('saved'), False)
        list = self.db.get_color('black')
        self.assertEqual(list, [(1, 2)])

    def test_first_step(self):
        self.db.insert_line('True', -1, -1, 'saved')
        self.assertEqual(self.db.is_empty('saved'), False)
        step = self.db.get_first_step()
        self.assertEqual(step[0][0], 'True')
