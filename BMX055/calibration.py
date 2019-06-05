import numpy as np
from scipy import odr
from scipy import optimize
from matplotlib.patches import Ellipse
import matplotlib.pyplot as plt
from scipy.stats import norm

def f(B, x):
    return ((x[0]/B[0])**2+(x[1]/B[1])**2-1.)

#Least squares method with scipy.optimize
def fit_func(parameter,xy):
    a = parameter[0]
    b = parameter[1]
    c = parameter[2]
    residual = (a*xy[0]+b*xy[1]+c)
    return residual

def g(B, x):
    return ((x[0]/B[0])**2+(x[1]/B[1])**2-1.)

if __name__ == '__main__':
    #f = open("bmx055test.txt", "r")
    f  = open("randomC.txt", "r")
    lines = f.readlines()
    x_csv = []
    y_csv = []
    xx_csv = x_csv
    yy_csv = y_csv
    for line in lines:
        word = line.split()
        x_csv.append(float(word[0]))
        y_csv.append(float(word[1]))

    for i in range(len(x_csv)):
        print(str(x_csv[i]) + " " + str(y_csv[i]))
    print()
    f.close()

    # sub average
    x_ave=np.average(x_csv)
    y_ave=np.average(y_csv)
    x_csv = x_csv-x_ave
    y_csv = y_csv-y_ave

    xy = np.array([x_csv, y_csv])

    #mdr = odr.Model(f, implicit=True)
    mdr = odr.Model(g, implicit=True)
    mydata = odr.Data(xy,y=1)
    #myodr = odr.ODR(mydata, mdr, beta0=[1., 2.])
    myodr = odr.ODR(mydata, mdr, beta0=[1., 2.,3.,4.])
    myoutput = myodr.run()
    myoutput.pprint()

    ax = plt.subplot(111, aspect='equal')
    plt.axes().set_aspect('equal', 'datalim')
    plt.scatter(x_csv, y_csv, c="red")
    plt.scatter(xx_csv, yy_csv, c="blue")
    ell = Ellipse(xy=(0., 0.), width=2.*myoutput.beta[0], height=2.*myoutput.beta[1], angle=0.0)
    ell.set_facecolor('none')
    ell.set_edgecolor('black')
    ax.add_artist(ell) # fitted curve
    plt.grid()
    plt.show()
