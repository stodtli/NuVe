

from Parser import Parser
from DataImporter import ColumnMajorImporter
from DMatrix import FiniteDifference
import numpy as np
from functools import reduce

class Verifier:
    def __init__(self, config_file_name):

        # confiuration file
        self._config_file_name = config_file_name

        # parse input arguments
        self._parser = Parser(self._config_file_name)

        self._data = None

        self._output = None

    def verify(self):
        self.importData()
        self.evaluateEquation()

    def importData(self):
        # import data from hdf file
        self._importer = ColumnMajorImporter()
        self._data = self._importer.importData(self._parser._file_prefix,
                self._parser._file_indices_to_check[0], self._parser._temporal_deriv_order,
                self._parser._file_index_digits, self._parser._field_names,
                self._parser._spatial_coords, self._parser._temporal_coord)

    def evaluateEquation(self):
        self._DM = FiniteDifference()
        self._derivs = self._DM.constructDerivatives(self._parser._derivs_needed, self._parser._spatial_coords, self._parser._temporal_coord, self._data)

        deriv = self._derivs
        data = self._data

        self._output = eval(self._parser._eqn_parsed)

        self._output = self.removeBC(self._output)

    def removeBC(self, output):
        # remove boundary values

        all_coords = self._parser._spatial_coords + [self._parser._temporal_coord]
        mask_vectors = []
        for coord in self._parser._spatial_coords:
            mask_vector = 0*self._data[coord] + 1
            mask_vector[0] = 0
            mask_vector[-1] = 0
            mask_vector = (mask_vector == 1)
            mask_vectors.append(mask_vector)
        mask_vector = 1+0*self._data[self._parser._temporal_coord]
        mask_vector = (mask_vector == 1)
        mask_vectors.append(mask_vector)

        mask = reduce(np.multiply.outer, mask_vectors)
        mask = mask.flatten('F')
        return output[mask]

