from Genome.context.transform_evalue import *
import unittest

# test the transform function itself
class TestTransform(unittest.TestCase):
    def test_second_best(self):
        self.assertEqual(find_second_best('hermuba', 'blastp_out_max_evalue'), 203)
    def test_transform_greater_one(self):
        self.assertEqual(transform_evalue(203, 5), 0)
    def test_transform_zero(self):
        self.assertEqual(transform_evalue(203, 0), 1)
    def test_transform_normal(self):
        self.assertEqual(transform_evalue(203, 0.2),math.log(0.2)/-203)


if __name__ == '__main__':
    unitest.main()
