from Verifier import Verifier
import numpy as np
from matplotlib import pyplot

# run 1D simulation
def test1DConfig():
    v = Verifier("test/simulation1D_config.ini")
    v.verify()

    x = v._data["x"]
    u = v._data["u"]
    d2x = v._derivs["x"][2]
    dt  = v._derivs["t"][1]
    uxx = d2x @ u
    ut = dt @ u

    print("1D MAX ERROR: ",str(np.amax(np.abs(v._output))))

    #xdouble = np.concatenate((x,1+x))
    #pyplot.plot(xdouble,uxx,'r',xdouble,ut,'b')
    #pyplot.show()

# run 2D simulation
def test2DConfig():
    v = Verifier("test/simulation2D_config.ini")
    print(v._parser._eqn_parsed)
    v.verify()

    x = v._data["x"]
    y = v._data["y"]
    t = v._data["t"]
    u = v._data["u"]
    #d2x = v._derivs["x"][2]
    #dt  = v._derivs["t"][1]
    #uxx = d2x @ u
    #ut = dt @ u

    print("2D MAX ERROR: ",str(np.amax(np.abs(v._output))))

    reshaped_output = np.reshape(v._output, (len(x)-2,len(y)-2,len(t)))
    reshaped_output = reshaped_output[:,:,1]

    xv,yv = np.meshgrid(x[1:-1],y[1:-1])

    #xdouble = np.concatenate((x,1+x))
    cp = pyplot.contourf(xv,yv,reshaped_output)
    pyplot.colorbar(cp)
    pyplot.show()


test1DConfig()
test2DConfig()
