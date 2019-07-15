import numpy as np

def Cal_rho(lon_a,lat_a,lon_b,lat_b):
	ra=6378.140  # equatorial radius (km)
	rb=6356.755  # polar radius (km)
	F=(ra-rb)/ra # flattening of the earth
	rad_lat_a = np.radians(lat_a)
	rad_lon_a = np.radians(lon_a)
	rad_lat_b = np.radians(lat_b)
	rad_lon_b = np.radians(lon_b)
	pa = np.arctan(rb/ra*np.tan(rad_lat_a))
	pb = np.arctan(rb/ra*np.tan(rad_lat_b))
	xx = np.arccos(np.sin(pa)*np.sin(pb) + np.cos(pa)*np.cos(pb)*np.cos(rad_lon_a-rad_lon_b))
	c1 = (np.sin(xx)-xx)*(np.sin(pa) + np.sin(pb))**2 / np.cos(xx/2)**2
	c2 = (np.sin(xx)+xx)*(np.sin(pa) - np.sin(pb))**2 / np.sin(xx/2)**2
	dr=F/8*(c1-c2)
	rho=ra*(xx + dr) * 1000	#Convert To [m]
	angle = 0
	return rho, angle

if __name__ == "__main__":
	lat_a = 35.902633
	lon_a = 139.717223
	lat_b = 35.902637
	lon_b = 139.717983
	dis, angle = Cal_rho(lon_a, lat_a, lon_b, lat_b)
	print(dis)
