
import numpy as np
import h5py
from abc import ABCMeta, abstractmethod

class DataImporter(metaclass=ABCMeta):
    @abstractmethod
    def importData(self):
        pass

class ColumnMajorImporter(DataImporter):
    # no class fields, constructor doesn't have to do anything
    def __init__(self):
        pass

    # imports data from hdf5 file
    def importData(self, run_name, start_nr, temp_deriv_order, nr_digits,
            field_names, spatial_coords, temporal_coord):

        data = {}
        # first file: read time invariant coordinate and temporal data
        file_name = run_name + "_" + str(start_nr).zfill(nr_digits) + ".hdf5"
        print("reading from " + str(file_name))
        with h5py.File(file_name, "r") as f:
            for field in field_names.keys():
                # align data in column-major order 'F' (i.e. first coordinate
                # varies fastest)
                data[field] = np.array(f[field_names[field]]).flatten('F')

        # consecutive files: only read temporal data
        for file_nr in range(start_nr+1, start_nr+temp_deriv_order+1):
            file_name = run_name + "_" + str(file_nr).zfill(nr_digits) + ".hdf5"
            print("reading from " + str(file_name))
            with h5py.File(file_name, "r") as f:
                for field in field_names.keys():
                    if field not in spatial_coords:
                        data[field] = np.append(data[field],
                            np.array(f[field_names[field]]).flatten('F'))

        return data


