import unittest
from ccat.evaluation import evaluation
import numpy as np

"""
TODO Unit test ideas
Check that the subject variables get checked after functions assign them.
Test the shape of data structures.
"""

class TestEval(unittest.TestCase):

    def test_accuracy_fn(self):
        # Testing the eval function
        m = 15

        x = np.array([14, 13, 10, 12,  8,  7,  4,  1,  6,  2,  5,  0, 11,  9,  3])
        Mc = np.reshape(x, (3, 5))

        x = np.array([6, 13, 10, 14,  2,  3,  7,  8, 12, 11,  4,  9,  0,  1,  5])
        Lc = np.reshape(x, (3, 5))

        m = len(x)

        error = evaluation.accuracy_fn(m, Mc, Lc)
        expected = 8/15.0
        
        # Check the answer to an example calculated by hand.
        self.assertEqual(error, expected)

        error = evaluation.accuracy_fn(m, Mc, Mc)
        expected = 1.0 

        # Check the evaluation of a the same cluster.
        self.assertEqual(error, expected)


if __name__ == '__main__':
    unittest.main()
    # log_file = 'test_eval_out.txt'
    # f = open(log_file, "w")
    # runner = unittest.TextTestRunner(f)
    # unittest.main(testRunner=runner)
    # f.close()
