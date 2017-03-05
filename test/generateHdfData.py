import h5py
import numpy as np

# spatial coordinate vector (assumed to not change with time)
x = np.linspace(0.0, 1.0, num = 10, endpoint = True)
y = np.linspace(0.0, 1.0, num = 5, endpoint = True)

# data first snapshot
t1 = 0.0
u1 = np.arange(0, x.size*y.size,).reshape(x.size, y.size, order = 'F')

# data second snapshot
t2 = 0.02
u2 = np.arange(x.size*y.size, 2*x.size*y.size).reshape(x.size, y.size, order = 'F')

# write snapshots to hdf5 file
f1 = h5py.File('testrun_001.hdf5', 'w')
f1.create_dataset("X1", data = x)
f1.create_dataset("X2", data = y)
f1.create_dataset("t", data = t1)
f1.create_dataset("u", data = u1)
f1.close()

f2 = h5py.File('testrun_002.hdf5', 'w')
f2.create_dataset("X1", data = x)
f2.create_dataset("X2", data = y)
f2.create_dataset("t", data = t1)
f2.create_dataset("u", data = u1)
f2.close()

