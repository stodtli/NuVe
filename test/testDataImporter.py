
import unittest
import numpy as np
import h5py

# add parent folder to path so that we can import modules from up there
import os.path
import sys
sys.path.append(os.path.dirname(os.path.realpath(".")))

from DataImporter import ColumnMajorImporter

class TestDataImporter(unittest.TestCase):

    # test case with 1 spatial dimension
    def test1DSpatial(self):
        # generate data
        x = np.array([0.0, 0.5, 1.0])
        t1 = 1.0  # data first snapshot
        u1 = np.array([1, 2, 3])
        t2 = 1.2
        u2 = np.array([4, 5, 6])
        t3 = 1.4
        u3 = np.array([7, 8, 9])

        # write it to hdf5 file
        with h5py.File("test1D_001.hdf5", "w") as f:
            f.create_dataset("z", data = x)
            f.create_dataset("time", data=t1)
            f.create_dataset("f", data = u1)
        with h5py.File("test1D_002.hdf5", "w") as f:
            f.create_dataset("z", data = x)
            f.create_dataset("time", data=t2)
            f.create_dataset("f", data = u2)
        with h5py.File("test1D_003.hdf5", "w") as f:
            f.create_dataset("z", data = x)
            f.create_dataset("time", data=t3)
            f.create_dataset("f", data = u3)

        # sample input parameters from Verifier class
        run_name = "test1D"
        start_nr = 1
        temp_deriv_order = 2
        nr_digits = 3
        field_names = {
                "x": "z",
                "t": "time",
                "u": "f",
                }
        spatial_coords = "x"
        temporal_coord = "t"
        
        # read data from file
        importer = ColumnMajorImporter()
        data = importer.importData(run_name, start_nr, temp_deriv_order,
                nr_digits, field_names, spatial_coords, temporal_coord)

        assert(np.array_equal(data["x"], x))
        assert(np.array_equal(data["u"], np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])))
        assert(np.array_equal(data["t"], np.array([1.0, 1.2, 1.4])))

if __name__ == '__main__':
    unittest.main()


        

# try read data
# run_name = "testrun"
# start_nr = 1
# temp_deriv_order = 1
# nr_digits = 3
# spatial_coords = ["x", "y"]
# temporal_coord = "t"
# field_names = {
        # "x": "X1",
        # "y": "X2",
        # "u": "u",
        # "t": "t",
        # }

# importer = ColumnMajorImporter()
# data = importer.importData(run_name, start_nr, temp_deriv_order, nr_digits,
        # field_names, spatial_coords, temporal_coord)

# print(data["u"])


