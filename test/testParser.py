
import unittest

# add parent folder to path so that we can import modules from up there
import os.path
import sys
sys.path.append(os.path.dirname(os.path.realpath(".")))

from Parser import Parser

class TestParser(unittest.TestCase):

    # Ensure that ApproxJacobian returns the expected value on a 1D input
    def testReadConfigFile(self):

        # Make sure Parser throws an exception if it's given a bad config filename
        try:
            p = Parser("nonexistent file")
            raise Exception('Parser failed to raise an exception on the missing input config file')
        except IOError:
            None
        try:
            p = Parser(None)
            raise Exception('Parser failed to raise an exception on a nonstring input')
        except TypeError:
            None


if __name__ == '__main__':
    unittest.main()
