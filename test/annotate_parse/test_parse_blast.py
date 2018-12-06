# test parser_blast
import unittest
from Genome.annotate_parser.parse_blast import *

class TestParseDmnd(unittest.TestCase):
    def test_df_size(self):
        df = parse_diamond('/home/hermuba/resistanceExp/test/test_file/dmnd_output')
        self.assertEqual(df.shape, (10,12))



if __name__ == '__main__':
    unittest.main()
