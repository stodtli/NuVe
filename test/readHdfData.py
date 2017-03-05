import numpy as np
import h5py

# input parameters
run_name = "testrun"
start_nr = 1
temp_deriv_order = 1
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

# first file: read time invariant coordinates and temporal data
file_name = run_name + "_" + str(start_nr).zfill(3) + ".hdf5"
print(file_name)
with h5py.File(file_name, "r") as f:
    for field in field_names.keys():
        data[field] = np.array(f[field_names[field]]).flatten('F')

# consecutive files: only read temporal data
for file_nr in range(start_nr+1, start_nr+temp_deriv_order+1):
    file_name = run_name + "_" + str(file_nr).zfill(3) + ".hdf5"
    print(file_name)
    with h5py.File(file_name, "r") as f:
        for field in field_names.keys():
            if field not in spatial_coords:
                data[field] = np.append(data[field],
                        np.array(f[field_names[field]]).flatten('F'))

# check results
print(data["x"])
print(data["y"])
print(data["u"])
print(data["t"])

    


# for file_nr in range(start_nr, start_nr+temp_deriv_order+1):
    # file_name = run_name + "_" + str(file_nr).zfill(3) + ".hdf5"
    # print(file_name)
    # # open file
    # f = h5py.File(file_name, "r")
    # # with h5py.File(file_name, "r") as f:
    # for field in field_names.keys():
        # print(np.array(f[field_names[field]]))
        # if field not in data:
            # data[field] = np.array(f[field_names[field]]).flatten('F')
        # else:
                # # data[field] = np.array(f[field_names[field]]).flatten('F')
            # data[field] = np.append(data[field],
                    # np.array(f[field_names[field]]).flatten('F'))
    # f.close()

# print(data["x"])
# print(data["y"])
# print(data["u"])

# with h5py.File("testrun_001.hdf5", "r") as f:
    # for field in field_names.keys():
        # data[field] = np.array(f[field_names[field]]).flatten('F')

# print(data["u"])


