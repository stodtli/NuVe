
import unittest

# add parent folder to path so that we can import modules from up there
import os.path
import sys
sys.path.append(os.path.dirname(os.path.realpath(".")))

from Parser import Parser

class TestParser(unittest.TestCase):

    # Ensure that the config file is read in properly
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

        # try on some bad input files
        try:
            p = Parser("example_bad_config_01.ini")
            raise Exception('Parser failed to raise an exception on a bad configuration file')
        except IOError:
            None
        try:
            p = Parser("example_bad_config_02.ini")
            raise Exception('Parser failed to raise an exception on a bad configuration file')
        except IOError:
            None


        # try on a good file
        p = Parser("example_config_01.ini")
        assert(p._parameters == {"nu": 1.0})
        assert(p._field_names ==  {"mu":"MU","x":"X1","y":"Y1","t":"T","u":"U"})
        assert(p._eqn_string == "D[u,{x,2}] - mu * nu * D[u,t]")
        assert(p._spatial_coords == ["y","x"])
        assert(p._temporal_coord == "t")

    # Ensure that the equation is parsed properly...
    def testEquationParser(self):
        p = Parser("example_config_02.ini")
        print(p._eqn_string)
        print(p._eqn_parsed)

if __name__ == '__main__':
    unittest.main()
