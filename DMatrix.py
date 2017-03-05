import numpy as np
import scipy as sp
from scipy.special import factorial
from numpy.linalg import inv
import math
from abc import ABCMeta, abstractmethod
from copy import copy

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

        coord_sizes = {}
        for coord in spatial_coords + [temporal_coord]:
            coord_sizes[coord] = len(data[coord])

        return {}

    # given a matrix mat, that represents this_coord (e.g. "x"), upgrade it to the supermatrix.
    # coords is the set of all coords (spatial + temporal)
    # coord_sizes is a dictionary relating each coordinate to the number of points in that coordinate
    def upgradeMatrix(self, mat, this_coord, coords, coord_sizes):
        c_n = len(coords)
        dims = []
        for coord in coords:
            dims.append(coord_sizes[coord])

        index = coords.index(this_coord)

        # the provided coord_size better match the given matrix
        assert(dims[index] == len(mat))

        # master array size
        N = 1
        for d in dims:
            N *= d

        M = np.zeros((N,N))

        # convert a set of paired indices (one pair for each coord) to a master coordinate pair
        def upgradeIndex(idict):
            r_master = 0
            c_master = 0
            scale = 1
            for j in range(0,c_n):
                (r,c) = idict[coords[j]]
                r_master += r*scale
                c_master += c*scale
                scale *= dims[j]
            return (r_master,c_master)

        # DO WE NEED TO COPY IDICT???
        def addAllPoints(val,idict,remaining_coords):
            if (len(remaining_coords) > 0):
                coord = remaining_coords[0]
                for r in range(0,coord_sizes[coord]):
                    #for c in range(0,coord_sizes[coord]):
                        #idict[coord] = (r,c)
                        idict[coord] = (r,r)
                        addAllPoints(val,idict,remaining_coords[1:])
            else:
                (r_master,c_master) = upgradeIndex(idict)
                #print(r_master,c_master)
                M[r_master,c_master] = val

        #idict = {"x":(0,0),"y":(0,0),"t":(0,0)}
        #print(upgradeIndex(idict))

        for r in range(0,coord_sizes[this_coord]):
            for c in range(0,coord_sizes[this_coord]):
                if mat[r,c] != 0:
                    remaining_coords = copy(coords)
                    remaining_coords.remove(this_coord)
                    addAllPoints(mat[r,c],{this_coord:(r,c)},remaining_coords)


        return M


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
