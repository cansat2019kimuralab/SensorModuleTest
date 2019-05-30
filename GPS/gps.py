import sys
import time
import difflib
import pigpio

RX=26
i = 0

try:
	pi = pigpio.pi()
	pi.set_mode(RX, pigpio.INPUT)
	pi.bb_serial_read_open(RX, 9600, 8)

	
	print ("DATA - SOFTWARE SERIAL:")
	while 1:
		#print("a ", end="")
		(count, data) = pi.bb_serial_read(RX)
		#print("b ", end="")
		if count:

			#print("c ", end="")

			gpsData = data.decode('utf-8', 'replace')
			#print("d ", end="")
			#print(gpsData)
			
			#gga = gpsData.find('$GPRMC,')
			rmc = gpsData.find('$GPRMC,')
			#gsa = gpsData.find('$GPGSA,')
			#gsv = gpsData.find('$GPGSV,')
			#vtg = gpsData.find('$GPVTGM')
			#print("e ", end="")
			if(gpsData[rmc:rmc+20].find("A") == -1): 
				print("Status V ", end="")
				i = i + 1
				print()
				
			else:
				gprmc = gpsData[rmc+7:]
				utctime = gpsData[rmc+7:rmc+17]
				lat = gpsData[rmc+20:rmc+30]
				lon = gpsData[rmc+32:rmc+43]
				print(str(utctime) + " ", end="")
				print(str(lat) + " ", end="")
				print(str(lon) + " ")
						
		#print("f ")	
		time.sleep(1)
except KeyboardInterrupt:
	pass
	pi.bb_serial_read_close(RX)
	pi.stop()
	print("\r\nKeyboard Intruppted, Serial Closed")
except:
	pi.bb_serial_read_close(RX)
	pi.stop()
	print ("Error, Serial Cloesd")
