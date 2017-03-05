
import unittest

# add parent folder to path so that we can import modules from up there
import os.path
import sys
sys.path.append(os.path.dirname(os.path.realpath(".")))

from DataImporter import ColumnMajorImporter

# try read data
run_name = "testrun"
start_nr = 1
temp_deriv_order = 1
nr_digits = 3
spatial_coords = ["x", "y"]
temporal_coord = "t"
field_names = {
        "x": "X1",
        "y": "X2",
        "u": "u",
        "t": "t",
        }

importer = ColumnMajorImporter()
data = importer.importData(run_name, start_nr, temp_deriv_order, nr_digits,
        field_names, spatial_coords, temporal_coord)

print(data["u"])


