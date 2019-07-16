import numpy as np
import math
#\import GPS

if __name__ == "__main__":
	lat_a, lon_a = 35.917281, 139.906248
	lat_b, lon_b = 35.917280, 139.906248
	dis, angle = GPS.Cal_RhoAng(lat_a, lon_a, lat_b, lon_b)
	print(dis, angle)
