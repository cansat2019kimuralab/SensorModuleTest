import sys
import time
import difflib
import pigpio
import serial
import binascii
import IM920
import gps

if __name__ == '__main__':
	try:
		gps.openGPS()
		print ("DATA - SOFTWARE SERIAL:")
		while 1:
			utctime,lat,lon = gps.readGPS()
			
			if(utctime == -1):
				if(lat == -1):
					print("Reading GPS Error")
					IM920.Send("E")
				else:
					print("Status V")
					IM920.Send("V")
			else:
				print(str(utctime) + "  " + str(lat) + " " + str(lon))
				IM920.Send(str(utctime))
				IM920.Send(str(lat))
				IM920.Send(str(lon))
			
			time.sleep(1)
			
	except KeyboardInterrupt:
		gps.closeGPS()
		print("\r\nKeyboard Intruppted, Serial Closed")
	except:
		gps.closeGPS()
		print("\r\nError, Serial Closed")


'''	
try:
	#pi = pigpio.pi()
	#pi.set_mode(RX, pigpio.INPUT)
	#pi.bb_serial_read_open(RX, 9600, 8)
	gps.openGPS()
	
	print ("DATA - SOFTWARE SERIAL:")
	while 1:
		utctime,lat,lon = gps.readGPS()
		if(utctime == -1):
			if(lat == -1):
				print("Reading GPS Error")
				IM920.Send("REading GPS Error")
			else:
				print("Status V")
				IM920.Send("V")
		else:
			print(str(utctime) + "  " + str(lat) + " " + str(lon))
			IM920.Send(utctime)
			IM920.Send(lat)
			IM920.Send(lon)
		time.sleep(1)
except KeyboardInterrupt:
	closeGPS()
	pass
	pi.bb_serial_read_close(RX)
	pi.stop()
	print ("Keyboard Interrupt, Serial Cloesd")
	IM920.Send('Error')

except:
	closeGPS()
	pi.bb_serial_read_close(RX)
	pi.stop()
	print("Error, Serial closed") 
	IM920.Send("Error")
'''