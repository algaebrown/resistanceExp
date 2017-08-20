import unittest
from src import test


class TestStringMethods(unittest.TestCase):

    def test_ab(self):
        self.assertEqual(test.ab(1, 2), 3)


if __name__ == '__main__':
    unittest.main()
