from Verifier import Verifier
import numpy as np
from matplotlib import pyplot
from matplotlib import cm

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
    vgood = Verifier("test/simulation2D_config.ini")
    vgood.verify()
    vbad = Verifier("test/simulation2Dcorrupt_config.ini")
    vbad.verify()

    x = vgood._data["x"]
    y = vgood._data["y"]
    t = vgood._data["t"]
    u = vgood._data["u"]
    ubad = vbad._data["u"]

    print("2D MAX ERROR: ",str(np.amax(np.abs(vgood._output))))
    contourPlotVector(x,y,t,u,title="Correct data\nDynamic heat equation in isotropic material",nobc=False,tstep=1,filename="correct_data_2D.png")
    contourPlotVector(x,y,t,ubad,title="Incorrect data\nDynamic heat equation in isotropic material",nobc=False,tstep=1,filename="incorrect_data_2D.png")
    contourPlotVector(x,y,t,np.abs(vbad._output),title="Identified error",colormap=cm.afmhot,filename="error_2D.png")
    pyplot.show()


def contourPlotVector(x,y,t,vec,title="",nobc=True,tstep=0,colormap=cm.jet,filename=""):
    pyplot.figure()
    reshaped_output = np.reshape(vec, (len(x)-2*nobc,len(y)-2*nobc,len(t)), order = 'F')
    reshaped_output = reshaped_output[:,:,tstep]

    if nobc:
        xv,yv = np.meshgrid(x[1:-1],y[1:-1])
    else:
        xv,yv = np.meshgrid(x,y)

    #xdouble = np.concatenate((x,1+x))
    cp = pyplot.contourf(xv,yv,reshaped_output,100, cmap=colormap)
    pyplot.xlabel("x")
    pyplot.ylabel("y")
    pyplot.title(title)
    pyplot.colorbar(cp)
    if (filename != ""):
        pyplot.savefig("plots/" + filename)

test1DConfig()
test2DConfig()
