import math
import sys
import time
import difflib
import pigpio
import numpy as np

RX=26
pi = pigpio.pi()

ELLIPSOID_GRS80 = 1	# GRS80
ELLIPSOID_WGS84 = 2	# WGS84

# Long Axis Radius and Flat Rate
GEODETIC_DATUM = {
    ELLIPSOID_GRS80: [
        6378137.0,         # [GRS80] Long Axis Radius
        1 / 298.257222101, # [GRS80] Flat Rate
 	   ],
    ELLIPSOID_WGS84: [
        6378137.0,         # [WGS84] Long Axis Radius
        1 / 298.257223563, # [WGS84] Flat Rate
    ],
}

# Limited times of Itereation
ITERATION_LIMIT = 1000

def openGPS():
	pi.set_mode(RX, pigpio.INPUT)
	pi.bb_serial_read_open(RX, 9600, 8)

def readGPS():
	utc = -1.0
	Lat = -1.0
	Lon = 0.0
	sHeight=0.0
	gHeight=0.0
	value = [0.0, 0.0, 0.0, 0.0, 0.0]

	(count, data) = pi.bb_serial_read(RX)
	if count:
		gpsData = data.decode('utf-8', 'replace')
		#print(gpsData)
		
		gga = gpsData.find('$GPGGA,')
		rmc = gpsData.find('$GPRMC,')
		#gsa = gpsData.find('$GPGSA,')
		#gsv = gpsData.find('$GPGSV,')
		#vtg = gpsData.find('$GPVTGM')
		#print(gpsData[rmc:rmc+20].find("V"))
		if(gpsData[rmc:rmc+20].find("V") != -1):	#Checking GPS Status
			#print("a")
			#Status V
			utc = -1.0
			Lat = 0.0
		elif(gpsData[rmc:rmc+20].find("A") != -1):
			#print("b")
			#Status A
			gprmc = gpsData[rmc:rmc+72].split(",")
			gpgga = gpsData[gga:gga+72].split(",")

			#Read Lat and Lon
			if len(gprmc) >= 7:
				utc = gprmc[1]
				lat = gprmc[3]
				lon = gprmc[5]
				try:
					Lat = round(float(lat[:2]) + float(lat[2:]) / 60.0, 6)
					Lon = round(float(lon[:3]) + float(lon[3:]) / 60.0, 6)
				except:
					Lat = 0.0
					Lon = 0.0
				if(gprmc[4] == "S"):
					Lat = Lat * -1
				if(gprmc[6] == "W"):
					Lon = Lon * -1
			elif len(gpgga) >= 6:
				utc = gpgga[1]
				lat = gpgga[2]
				lon = gpgga[4]
				try:
					Lat = round(float(lat[:2]) + float(lat[2:]) / 60.0, 6)
					Lon = round(float(lon[:3]) + float(lon[3:]) / 60.0, 6)
				except:
					Lat = 0.0
					Lon = 0.0
				if(gpgga[3] == "S"):
					Lat = Lat * -1.0
				if(gpgga[5] == "W"):
					Lon = Lon * -1.0
			else:
				pass

			#Read Height
			if len(gpgga) >= 12:
				sHeight=gpgga[9]
				gHeight=gpgga[11]
		else:
			#print("c")
			#No Status Data
			utc = -1.0
			Lat = -1.0
			Lon = 0.0

	value = [utc, Lat, Lon, sHeight, gHeight]
	#print(value)
	return value

def closeGPS():
	pi.bb_serial_read_close(RX)
	pi.stop()

def Cal_RhoAng(lat_a, lon_a, lat_b ,lon_b):
	if(lat_a == lat_b and lon_a == lon_b):
		return 0.0, 0.0
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
	angle = math.atan2(lon_a-lon_b,  lat_b-lat_a) * 180 / math.pi	#[deg]
	return rho, angle

def vincentyInverse(lat1, lon1, lat2, lon2, ellipsoid=None):
    if lat1 == lat2 and lon1 == lon2:
        return 0.0, 0.0
	
    # Calculate Short Axis Radius
    # if Ellipsoid is not specified, it uses GRS80
    a, f = GEODETIC_DATUM.get(ellipsoid, GEODETIC_DATUM.get(ELLIPSOID_GRS80))
    b = (1 - f) * a

    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    lambda1 = math.radians(lon1)
    lambda2 = math.radians(lon2)

    # Corrected Latitude
    U1 = math.atan((1 - f) * math.tan(phi1))
    U2 = math.atan((1 - f) * math.tan(phi2))

    sinU1 = math.sin(U1)
    sinU2 = math.sin(U2)
    cosU1 = math.cos(U1)
    cosU2 = math.cos(U2)

    # Diffrence of Longtitude between 2 points
    L = lambda2 - lambda1

    # Reset lamb to L
    lamb = L

    # Calculate lambda untill it converges
    # if it doesn't converge, returns None
    for i in range(ITERATION_LIMIT):
        sinLambda = math.sin(lamb)
        cosLambda = math.cos(lamb)
        sinSigma = math.sqrt((cosU2 * sinLambda) ** 2 + (cosU1 * sinU2 - sinU1 * cosU2 * cosLambda) ** 2)
        cosSigma = sinU1 * sinU2 + cosU1 * cosU2 * cosLambda
        sigma = math.atan2(sinSigma, cosSigma)
        sinAlpha = cosU1 * cosU2 * sinLambda / sinSigma
        cos2Alpha = 1 - sinAlpha ** 2
        cos2Sigmam = cosSigma - 2 * sinU1 * sinU2 / cos2Alpha
        C = f / 16 * cos2Alpha * (4 + f * (4 - 3 * cos2Alpha))
        lambdaʹ = lamb
        lamb = L + (1 - C) * f * sinAlpha * (sigma + C * sinSigma * (cos2Sigmam + C * cosSigma * (-1 + 2 * cos2Sigmam ** 2)))

		#Deviation is udner 1e-12, break
        if abs(lamb - lambdaʹ) <= 1e-12:
            break
    else:
        return None

    # if it converges, calculates distance and angle
    u2 = cos2Alpha * (a	 ** 2 - b ** 2) / (b ** 2)
    A = 1 + u2 / 16384 * (4096 + u2 * (-768 + u2 * (320 - 175 * u2)))
    B = u2 / 1024 * (256 + u2 * (-128 + u2 * (74 - 47 * u2)))
    dSigma = B * sinSigma * (cos2Sigmam + B / 4 * (cosSigma * (-1 + 2 * cos2Sigmam ** 2) - B / 6 * cos2Sigmam * (-3 + 4 * sinSigma ** 2) * (-3 + 4 * cos2Sigmam ** 2)))

    s = b * A * (sigma - dSigma)															#Distance between 2 points
    alpha = -1 * math.atan2(cosU2 * sinLambda, cosU1 * sinU2 - sinU1 * cosU2 * cosLambda)	#Angle between 2 points

    # return s(distance), and alpha(angle)
    return s, math.degrees(alpha)

if __name__ == '__main__':
	try:
		openGPS()
		with open("gps.txt", "a") as f:
			pass
		print ("DATA - SOFTWARE SERIAL:")
		while 1:
			utc,lat,lon,sHeight,gHeight = readGPS()
			#print(utc, lat, lon)
			if(utc == -1.0):
				if(lat == -1.0):
					print("Reading GPS Error")
					#pass
				else:
					print("Status V")
			else:
				print(utc, lat, lon)
				#with open("gps.txt", "a") as f:
				#	f.write(str(utc) + "\t" + str(lat) + "\t" + str(lon) + "\t" + str(sHeight) + "\t" + str(gHeight) + "\n")

			time.sleep(1)
	except KeyboardInterrupt:
		closeGPS()
		print("\r\nKeyboard Intruppted, Serial Closed")
	except Exception as e:
		closeGPS()
		print ("\r\nError, Serial Cloesd")
		print(e.message)
