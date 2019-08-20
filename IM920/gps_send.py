import sys
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/GPS')
sys.path.append('/home/pi/git/kimuralab/IntegratedProgram/Running')
sys.path.append('/home/pi/git/kimuralab/Other')

import binascii
import difflib
import pigpio
import serial
import traceback
import time
import GPS
import IM920
import RunningGPS
import Other

if __name__ == '__main__':
	try:
		GPS.openGPS()
		while 1:
			gpsData = GPS.readGPS()
			IM920.Send("G" + str(gpsData[1]) + ":" + str(gpsData[2]))
			print("G" + str(gpsData[1]) + ":" + str(gpsData[2]))
			if(RunningGPS.checkGPSstatus(gpsData)):
				Other.saveLog("logGPS.txt", time.time(), gpsData)
			time.sleep(1)
	except KeyboardInterrupt:
		GPS.closeGPS()
		print("\r\nKeyboard Intruppted, Serial Closed")
	except:
		GPS.closeGPS()
		print("\r\nError, Serial Closed")
		print(traceback.format_exc()) 
