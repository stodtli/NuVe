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

        assert(p._file_prefix == "run_")
        assert(p._file_index_digits == 3)
        assert(p._file_indices_to_check == [1,50,70])

    # Ensure that the equation is parsed properly...
    def testEquationParser(self):
        p = Parser("example_config_02.ini")
        assert(p._derivs_needed == {"t":3,"x":2})
        print(p._eqn_string)
        print(p._eqn_parsed)

    def testCountTemporalDerivOrder(self):
        p = Parser("example_config_01.ini")
        assert(p._temporal_deriv_order == 1)

        l=p.countInteriorTemporalDerivs("D[D[nu * D[u,{t,3}],{x,2}],t] - mu * nu * D[u,t] + D[u^2,{t,2}]",0)
        assert(l==4)
        l=p.countInteriorTemporalDerivs("D[D[nu * D[u,{t,1}],{x,2}],t] - mu * nu * D[u,t] + D[u^2,{t,2}]",0)
        assert(l==2)
        l=p.countInteriorTemporalDerivs("D[D[nu * D[u,{y,1}],{x,2}],t] - mu * nu * D[u,t] + D[u^2,{t,2}]",0)
        assert(l==2)
        l=p.countInteriorTemporalDerivs("D[{t,17},x] + D[D[nu * D[u,{y,1}],{x,2}],t] - mu * nu * D[u,t]",0)
        assert(l==1)
        l=p.countInteriorTemporalDerivs("D[{t,17},x] + D[D[nu * D[u,{y,1}],{x,2}],y] - mu * nu * D[u,t]",0)
        assert(l==1)
        l=p.countInteriorTemporalDerivs("D[D[D[u,t]+D[(v*x+t),t] - nu * D[u,{y,1}],{x,2}],t] - mu * nu * D[u,t]",0)
        assert(l==2)

if __name__ == '__main__':
    unittest.main()
