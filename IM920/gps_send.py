import sys
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/GPS')
import time
import difflib
import pigpio
import serial
import binascii
import IM920
import GPS

if __name__ == '__main__':
	try:
		GPS.openGPS()
		print ("DATA - SOFTWARE SERIAL:")
		while 1:
			utctime,lat,lon,sHeight,gHeight = GPS.readGPS()
			if utctime == -1.0:
				if lat == -1.0:
					print("Reading GPS Error")
					IM920.Send("E")
				else:
					print("Status V")
					IM920.Send("V")
			else:
				#print(str(utctime) + "  " + str(lat) + " " + str(lon), end="")
				#print(str(sHeight)+str(gHeight))
				IM920.Send('G'+", "+str(utctime) + ',' + str(lat) + ',' + str(lon) + ',' + str(sHeight) + ',' + str(gHeight) + ',')
				with open("gps.txt", "a") as f:
					f.write("UTC:" + str(utctime) + "\tLat:" + str(lat) + "\tLon:" + str(lon) + "\tsH:" + str(sHeight) + "\tgH:" + str(gHeight) + "\n")

			time.sleep(1)
	except KeyboardInterrupt:
		GPS.closeGPS()
		print("\r\nKeyboard Intruppted, Serial Closed")
	except Exception as e:
		GPS.closeGPS()
		print("\r\nError, Serial Closed")
		print()
		print(e.message) 
