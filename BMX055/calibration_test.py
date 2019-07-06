import sys
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/BMX055')
import numpy as np
import math
from scipy import odr
from scipy import optimize
from matplotlib.patches import Ellipse
import matplotlib.pyplot as plt
from scipy.stats import norm
import Calibration
import BMX055


if __name__ == '__main__':
	try:
		file = 'cal_test_1.txt'
		BMX055.bmx055_setup()
		count = 0

		while count <= 300:
			count = count + 1
			bmx055data = BMX055.bmx055_read()
			with open(file, 'a') as f:
				for i in range(6, 8):
					print(str(bmx055data[i]) + "\t", end="")
					f.write(str(bmx055data[i]) + "\t")
				print()
				f.write("\n")

		cal_data = Calibration.calibration(file)
		for i in range(4):
			print(cal_data[i])

		while 1:
			bmx055data = BMX055.bmx055_read()
			dir = math.atan2(bmx055data[6], bmx055data[7])*180/math.pi
			print(dir, end="")
			dir = math.atan2((bmx055data[6]-cal_data[0])/cal_data[2], (bmx055data[7]-cal_data[1])/cal_data[3])*180/math.pi
			print("\t" + str(dir))
	except KeyboadInterrupt:
		pass
	except e:
		print(e.message)
