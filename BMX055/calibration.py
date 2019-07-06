import numpy as np
from scipy import odr
from scipy import optimize
from matplotlib.patches import Ellipse
import matplotlib.pyplot as plt
from scipy.stats import norm

def ellipse(B, x):
    return ((x[0]/B[0])**2+(x[1]/B[1])**2-1.)

def calibration(path):
    #f = open("bmx055test.txt", "r")

    with open(path, "r") as f:
        lines = f.readlines()
        x_csv = []
        y_csv = []
        for line in lines:
            word = line.split()
            x_csv.append(float(word[0]))
            y_csv.append(float(word[1]))

    '''
    for i in range(len(x_csv)):
        print(str(x_csv[i]) + " " + str(y_csv[i]))
    print()
    '''

    xx_csv = x_csv
    yy_csv = y_csv
    
    # sub average
    x_ave=np.average(x_csv)
    y_ave=np.average(y_csv)

    x_csv = x_csv-x_ave
    y_csv = y_csv-y_ave

    xy = np.array([x_csv, y_csv])

    mdr = odr.Model(ellipse, implicit=True)
    mydata = odr.Data(xy,y=1)
    myodr = odr.ODR(mydata, mdr, beta0=[1.,2.])
    myoutput = myodr.run()

    """from ellipse to Circle"""
    x_csv = x_csv / 100.*myoutput.beta[1]
    y_csv = y_csv / 100.*myoutput.beta[0]

    cal_data = [x_ave, y_ave, 100.*myoutput.beta[1], 100.*myoutput.beta[0]]

    ax = plt.subplot(111, aspect='equal')
    plt.scatter(xx_csv, yy_csv, c="blue")
    plt.scatter(x_csv, y_csv, c="red")
    plt.grid()
    plt.show()

    return cal_data


if __name__ == '__main__':
    file = 'randomC.txt'
    cal_data = calibration(file)
    for i in range(4):
        print(cal_data[i])
