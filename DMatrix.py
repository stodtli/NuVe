import numpy as np
import scipy as sp
from scipy.special import factorial
from numpy.linalg import inv
import math
from abc import ABCMeta, abstractmethod

class DMatrix(metaclass=ABCMeta):
    @abstractmethod
    def constructDerivatives(self):
        pass

class FiniteDifference(DMatrix):
    # no class fields, constructor doesn't have to do anything
    def __init__(self):
        pass

    # imports data from hdf5 file
    def constructDerivatives(self, derivatives_needed, spatial_coords, temporal_coord, data):
        return {}

    # construct |order| derivative matrices for the coordinate xcoord
    def oneCoordMatrix(self,xcoord, order):
        n = len(xcoord)
        assert(n > order)

        Dmats = {}
        for o in range(1,order+1):
            Dmats[o] = np.zeros((n,n))

        for i in range(0,n):
            # try to do a central difference if possible.
            # if not possible, imbalance on the side of forward differencing
            offset = -int(math.floor(order/2.))
            # check if the offset will push us off an edge, and fix if necessary
            if (i + offset) < 0:
                offset = -i
            if (i + offset + order) > n-1:
                offset = - order - i + n-1

            # construct the local optimal finite difference for d1x,d2x,...,dox
            H = np.zeros((order+1,order+1))

            for j in range(0,order+1):
                delta = xcoord[i+j+offset] - xcoord[i]
                for k in range(0,order+1):
                    H[j,k] = math.pow(delta,k) / sp.special.factorial(k)
            Hinv = inv(H)
            #print(Hinv)

            # put the local operators into the complete operator
            for o in range(1,order+1):
                # Replace line i of Dmats[o] with the line Hinv[o] at the proper offset
                for c in range(0,order+1):
                    Dmats[o][i, i + offset + c] = Hinv[o,c]

        #print(Dmats[1])
        #print(Dmats[2])
        return(Dmats)
