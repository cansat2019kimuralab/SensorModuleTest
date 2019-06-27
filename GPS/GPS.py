import sys
import time
import difflib
import pigpio

RX=26
pi = pigpio.pi()


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
		if(gpsData[rmc:rmc+20].find("V") != -1):	#Checking GPS Status
			#Status V
			Lat = 0.0
			Lon = 0.0
		elif(gpsData[rmc:rmc+20].find("A") != -1):
			#Status A
			gprmc = gpsData[rmc:rmc+72].split(",")
			gpgga = gpsData[gga:gga+72].split(",")

			#Read Lat and Lon
			if len(gprmc) >= 7:
				utc = gprmc[1]
				lat = gprmc[3]
				lon = gprmc[5]
				Lat = round(float(lat[:2]) + float(lat[2:]) / 60.0, 6)
				Lon = round(float(lon[:3]) + float(lon[3:]) / 60.0, 6)
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
					Lat = -1.0
					Lon = -0.0
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
			#No Status Data
			utc = -1.0
			Lat = -1.0
			Lon = 0.0

	value = [utc, Lat, Lon, sHeight, gHeight]
	return value

def closeGPS():
	pi.bb_serial_read_close(RX)
	pi.stop()

if __name__ == '__main__':
	try:
		openGPS()
		with open("gps.txt", "a") as f:
			pass
		print ("DATA - SOFTWARE SERIAL:")
		while 1:
			utc,lat,lon,sHeight,gHeight = readGPS()
			if(utc == -1):
				if(lat == -1):
					print("Reading GPS Error")
				else:
					print("Status V")
			else:
				print(str(utc) + "  ", end ="")
				print(str(lat) + " ", end ="")
				print(str(lon) + " ", end ="")
				print(str(sHeight) + " ", end="")
				print(str(gHeight), end="")
				print()
				with open("gps.txt", "a") as f:
					f.write(str(utc) + "\t" + str(lat) + "\t" + str(lon) + "\t" + str(sHeight) + "\t" + str(gHeight) + "\n")

			time.sleep(1)
	except KeyboardInterrupt:
		closeGPS()
		print("\r\nKeyboard Intruppted, Serial Closed")
	except Exception as e:
		closeGPS()
		print ("\r\nError, Serial Cloesd")
		print(e.message)
