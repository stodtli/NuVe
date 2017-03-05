from Verifier import Verifier
import numpy
from matplotlib import pyplot

v = Verifier("test/simulation_config.ini")
v.verify()

x = v._data["x"]
u = v._data["u"]
d2x = v._derivs["x"][2]
dt  = v._derivs["t"][1]
uxx = d2x @ u
ut = dt @ u

print("MAX ERROR: ",str(numpy.amax(numpy.abs(v._output))))

y = numpy.concatenate((x,1+x))
pyplot.plot(y,uxx,'r',y,ut,'b')
pyplot.show()
