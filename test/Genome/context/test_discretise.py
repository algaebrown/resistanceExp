import unittest
import pandas as pd
from Genome.context.discretise import *
class TestDiscretiseMethods(unittest.TestCase):
    def test_discretize_equal(self):
        test = pd.DataFrame({1:[0,0.5,1], 2:[0.02,0.6,1]})
        test_ans = pd.DataFrame({1:[0,89,99], 2:[5,92,99]})
        self.assertEqual(discrete_equal_bulk(test, 'refseq')[1].tolist(), test_ans[1].tolist())
        self.assertEqual(discrete_equal_bulk(test, 'refseq')[2].tolist(), test_ans[2].tolist())
if __name__ == '__main__':
        unittest.main()
