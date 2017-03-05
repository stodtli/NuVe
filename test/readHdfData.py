import numpy as np
import h5py

spatial_coords = ["x", "y"]
temporal_coord = "t"
field_names = {
        "x": "X1",
        "y": "X2",
        "u": "u",
        "t": "t",
        }

# retreive data from hdf5 file
data = {}

with h5py.File("testrun_001.hdf5", "r") as f:
    for field in field_names.keys():
        data[field] = np.array(f[field_names[field]]).flatten('F')

print(data["u"])


