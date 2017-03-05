
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
        t2 = 1.2  # data second snapshot etc.
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

        # and compare
        assert(np.array_equal(data["x"], x))
        assert(np.array_equal(data["u"], np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])))
        assert(np.array_equal(data["t"], np.array([1.0, 1.2, 1.4])))


    # test case with 2 spatial dimensions
    def test2DSpatial(self):
        # generate data
        X1 = np.array([0.0, 0.5, 1.0])
        X2 = np.array([0.0, 1.0])
        t1 = 0.5  # data first snapshot
        # use on purpose X2 as first dimension
        u1 = np.array([[1, 2, 3], [4, 5, 6]])
        t2 = 0.7
        u2 = np.array([[7, 8, 9], [10, 11, 12]])
        
        # write it to hdf5 file
        with h5py.File("test2D_003.hdf5", "w") as f:
            f.create_dataset("X1", data = X1)
            f.create_dataset("X2", data = X2)
            f.create_dataset("t", data = t1)
            f.create_dataset("u", data = u1)
        with h5py.File("test2D_004.hdf5", "w") as f:
            f.create_dataset("X1", data = X1)
            f.create_dataset("X2", data = X2)
            f.create_dataset("t", data = t2)
            f.create_dataset("u", data = u2)

        # sample input parameters from Verifier class
        run_name = "test2D"
        start_nr = 3
        temp_deriv_order = 1
        nr_digits = 3
        field_names = {
                "x": "X2",
                "y": "X1",
                "t": "t",
                "u": "u",
                }
        spatial_coords = ["x", "y"]
        temporal_coord = "t"
        
        # read data from file
        importer = ColumnMajorImporter()
        data = importer.importData(run_name, start_nr, temp_deriv_order,
                nr_digits, field_names, spatial_coords, temporal_coord)

        # and compare
        assert(np.array_equal(data["x"], X2))
        assert(np.array_equal(data["y"], X1))
        assert(np.array_equal(data["u"],
            np.array([1, 4, 2, 5, 3, 6, 7, 10, 8, 11, 9, 12])))
        assert(np.array_equal(data["t"], np.array([0.5, 0.7])))


    # test case with 3 spatial dimensions
    def test3DSpatial(self):
        # generate data
        X1 =np.array([0.0, 1.0])
        X2 = np.array([0.0, 0.5, 1.0])
        X3 = np.array([0.0, 0.25, 0.5, 0.75])
        t1 = 0.5  # data first snapshot
        u1 = np.arange(0, X1.size*X2.size*X3.size).reshape(X1.size, 
                X2.size, X3.size, order = 'F')
        t2 = 0.7  # data second snapshot
        u2 = np.arange(X1.size*X2.size*X3.size, 
                2*X1.size*X2.size*X3.size).reshape(X1.size, 
                        X2.size, X3.size, order = 'F')
        
        # write it to hdf5 file
        with h5py.File("test3D_000.hdf5", "w") as f:
            f.create_dataset("X1", data = X1)
            f.create_dataset("X2", data = X2)
            f.create_dataset("X3", data = X3)
            f.create_dataset("t", data = t1)
            f.create_dataset("u", data = u1)
        with h5py.File("test3D_001.hdf5", "w") as f:
            f.create_dataset("X1", data = X1)
            f.create_dataset("X2", data = X2)
            f.create_dataset("X3", data = X3)
            f.create_dataset("t", data = t2)
            f.create_dataset("u", data = u2)

        # sample input parameters from Verifier class
        run_name = "test3D"
        start_nr = 0
        temp_deriv_order = 1
        nr_digits = 3
        field_names = {
                "x": "X1",
                "y": "X2",
                "z": "X3",
                "t": "t",
                "u": "u",
                }
        spatial_coords = ["x", "y", "z"]
        temporal_coord = "t"
        
        # read data from file
        importer = ColumnMajorImporter()
        data = importer.importData(run_name, start_nr, temp_deriv_order,
                nr_digits, field_names, spatial_coords, temporal_coord)

        # and compare
        assert(np.array_equal(data["x"], X1))
        assert(np.array_equal(data["y"], X2))
        assert(np.array_equal(data["z"], X3))
        assert(np.array_equal(data["u"], np.arange(0, 
            2*X1.size*X2.size*X3.size)))
        assert(np.array_equal(data["t"], np.array([0.5, 0.7])))




        

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


