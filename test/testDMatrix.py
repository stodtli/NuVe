import unittest

# add parent folder to path so that we can import modules from up there
import os.path
import sys
sys.path.append(os.path.dirname(os.path.realpath(".")))

from DMatrix import FiniteDifference

class TestDMatrix(unittest.TestCase):

    def assertArraysAlmostEqual(self,arr1,arr2,places=7):
        n = len(arr1)
        for r in range(0,n):
            for c in range(0,n):
                self.assertAlmostEqual(arr1[r][c],arr2[r][c],places=places)


    # Test some finite difference matrices
    def testFinDiff(self):
        DM = FiniteDifference()

        x = [0,1,2,3]
        Dmats = DM.oneCoordMatrix(x,1)
        correct= [[-1., 1., 0., 0.],
                  [ 0.,-1., 1., 0.],
                  [ 0., 0.,-1., 1.],
                  [ 0., 0.,-1., 1.]]
        self.assertArraysAlmostEqual(Dmats[1],correct)

        x = [0,1.1,1.2,3.82]
        Dmats = DM.oneCoordMatrix(x,2)
        correct1 = [[   -1.7424,  10.9091,  -9.1667,        0],
                    [   -0.0758,  -9.0909,   9.1667,        0],
                    [         0,  -9.6324,   9.6183,   0.0140],
                    [         0,   9.6324, -10.3817,   0.7493]]
        correct2 = [[    1.5152, -18.1818,  16.6667,        0],
                    [    1.5152, -18.1818,  16.6667,        0],
                    [         0,   7.3529,  -7.6336,   0.2806],
                    [         0,   7.3529,  -7.6336,   0.2806]]
        self.assertArraysAlmostEqual(Dmats[1],correct1,places=3)
        self.assertArraysAlmostEqual(Dmats[2],correct2,places=3)


if __name__ == '__main__':
    unittest.main()

