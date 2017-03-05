
import h5py
import numpy as np

# analytical solution
u = lambda x, t : 4 * np.exp(-(np.pi**2)*t) * np.sin(np.pi * x)

# discretize domain
x = np.linspace(0, 1, num=100)
dt = 1E-4
t_start = [0.01, 0.1, 0.5]

# generate correct solution and write it to file
run_name = "correct_data"
nr_digits = 4
for t in t_start:
    file_nr = int(t / dt)
    file_name = run_name + "_" + str(file_nr).zfill(nr_digits) + ".hdf5"
    with h5py.File(file_name, "w") as f:  # data at t
        f.create_dataset("x", data = x)
        f.create_dataset("t", data = t)
        f.create_dataset("u", data = u(x,t))
    file_name = run_name + "_" + str(file_nr+1).zfill(nr_digits) + ".hdf5"
    with h5py.File(file_name, "w") as f:  # data at t+dt
        f.create_dataset("x", data = x)
        f.create_dataset("t", data = t+dt)
        f.create_dataset("u", data = u(x,t+dt))


# generate corrupted simulation data
run_name = "corrupted_data"
nr_digits = 4
for t in t_start:
    file_nr = int(t / dt)
    file_name = run_name + "_" + str(file_nr).zfill(nr_digits) + ".hdf5"
    with h5py.File(file_name, "w") as f:  # data at t
        f.create_dataset("x", data = x)
        f.create_dataset("t", data = t)
        f.create_dataset("u", data = u(x,t))
    file_name = run_name + "_" + str(file_nr+1).zfill(nr_digits) + ".hdf5"
    with h5py.File(file_name, "w") as f:  # data at t+dt
        f.create_dataset("x", data = x)
        f.create_dataset("t", data = t+dt)
        f.create_dataset("u", data = u(x,t+dt)-np.random.random(x.size))


