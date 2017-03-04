import numpy as np
import h5py

spatial_coords = ["x"]
temporal_coord = "t"
field_names = {
        "x": "x",
        "u": "u",
        "t": "t",
        }

# retreive data from hdf5 file
# data = dict((x, []) for x in field_names.keys())
data = {}

with h5py.File("testrun_001.hdf5", "r") as f:
    for field in field_names.keys():
        data[field] = np.array(f[field])
    # data["u"]=np.array(f["u"])

print(data["t"])


