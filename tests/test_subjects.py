import unittest
import subjects

"""
Check that the subject variables get checked after functions assign them.
Test the shape of data structures.
Could add a unit test to check if the current algorithm scores higher than the kmedoids approach.
SETTING CSV TO NONE SHOULD NOT BREAK IT
"""

class TestSubject(unittest.TestCase):

    def test_subject_init(self):
        print "Testing Subject initialisation"

        # Init some test paths
        fname = "/home/joe/Downloads/This"
        sdir = "/home/joe/Documents/data/ADHD200_CC200/connectivity"
        csv_path = "/home/joe/Documents/data/ADHD200_CC200_CSV"

        # Init the subject model, applying no CSV should be fine
        sbj = subjects.Subject(sdir, fname)

        # Extract the results
        result_f_name = sbj.f_name
        result_directory = sbj.directory
        result_csv = sbj.csv

        # Test the results
        self.assertEqual(result_f_name, "/home/joe/Downloads/This")
        self.assertEqual(result_directory,
                         "/home/joe/Documents/data/ADHD200_CC200/connectivity")
        self.assertEqual(None, result_csv )

        # Init with csv
        sbj = subjects.Subject(sdir, fname, csv=csv_path)

    def test_subject_load_connectivity_mx(self):
        print "Testing the load connectivity matrix"

        # Use mocks to connectivity matrix

    def test_subject_build_distance_mx(self):
        print "Testing the load connectivity matrix"

        # Use mock fnames

if __name__ == '__main__':
    unittest.main()
    # log_file = 'unittest_out.txt'
    # f = open(log_file, "w")
    # runner = unittest.TextTestRunner(f)
    # unittest.main(testRunner=runner)
    # f.close()
