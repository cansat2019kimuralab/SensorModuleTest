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
			utctime, lat, lon = GPS.readGPS()
			if utctime == -1.0:
				if lat == -1.0:
					print("Reading GPS Error")
					IM920.Send("E")
				else:
					print("Status V")
					IM920.Send("V")
			else:
				print(str(utctime) + "  " + str(lat) + " " + str(lon))
				IM920.Send('u'+str(utctime))
				IM920.Send('a'+str(lat))
				IM920.Send('o'+str(lon))

			time.sleep(1)
	except KeyboardInterrupt:
		GPS.closeGPS()
		print("\r\nKeyboard Intruppted, Serial Closed")
	except Exception as e:
		GPS.closeGPS()
		print("\r\nError, Serial Closed")
		print()
		print(e.message) 