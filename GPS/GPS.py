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
	utctime = -1.0
	Lat = -1.0
	Lon = 0.0
	sHight=0.0
	gHight=0.0
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
			utctime = -1.0
			Lat = 0.0
			Lon = 0.0
		elif(gpsData[rmc:rmc+20].find("A") != -1):
			#Status A
			#gprmc = gpsData[rmc+7:]
			utctime = gpsData[rmc+7:rmc+17]
			lat = gpsData[rmc+20:rmc+29]
			lon = gpsData[rmc+32:rmc+42]
			Lat = round(float(lat[:2]) + float(lat[2:]) / 60.0, 6)
			Lon = round(float(lon[:3]) + float(lon[3:]) / 60.0, 6)

			gpgga = gpsData[gga:gga+72]
	
			#print(gpgga)
			

			
			
			hight=gpgga.split(",")
			sHight=hight[9]
			gHight=hight[11]
			#print(sHight)
			#print(gHight)
		else:
			#No Status Data
			utctime = -1.0
			Lat = -1.0
			Lon = 0.0
		
	value = [utctime, Lat, Lon, sHight, gHight]
	return value

def closeGPS():
	pi.bb_serial_read_close(RX)
	pi.stop()

if __name__ == '__main__':
	try:
		openGPS()
		print ("DATA - SOFTWARE SERIAL:")
		while 1:
			utctime,lat,lon,sHight,gHight = readGPS()
			if(utctime == -1):
				if(lat == -1):
					print("Reading GPS Error")
				else:
					print("Status V")
			else:
				print(str(utctime) + "  " + str(lat) + " " + str(lon))
				print(str(sHight))
				print(str(gHight))
				
			time.sleep(1)
	except KeyboardInterrupt:
		closeGPS()
		print("\r\nKeyboard Intruppted, Serial Closed")
	except Exception as e:
		closeGPS()
		print ("\r\nError, Serial Cloesd")
		print(e.message)
