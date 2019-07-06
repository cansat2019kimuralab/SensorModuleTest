import sys
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/BMX055')
import numpy as np
from scipy import odr
from scipy import optimize
from matplotlib.patches import Ellipse
import matplotlib.pyplot as plt
from scipy.stats import norm
import Calibration


def ellipse(B, x):
    return ((x[0]/B[0])**2+(x[1]/B[1])**2-1.)

if __name__ == '__main__':
    file = 'cal_test_1.txt'

    while i <= 100:
        bmx055data = BMX055.bmx055_read()
        with open(file, 'a') as f:
	        for i in range(6, 8):
		        print(str(bmxData[i]) + "\t", end="")
                f.write(str(bmxData[i]) + "\t", end="")
	        print()
            f.write("\n")

    cal_data = Calibration.calibration(file)
    for i in range(4):
        print(cal_data[i])
