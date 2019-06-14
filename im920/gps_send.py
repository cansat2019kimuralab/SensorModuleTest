import sys
import time
import difflib
import pigpio
import serial
import binascii
import IM920
import gps
RX=26
	
try:
	*pi = pigpio.pi()
	*pi.set_mode(RX, pigpio.INPUT)
	*pi.bb_serial_read_open(RX, 9600, 8)
	gps.openGPS()
	
	print ("DATA - SOFTWARE SERIAL:")
	while 1:
		(count, data) = pi.bb_serial_read(RX)
		if count:
			gpsData = data.decode('utf-8', 'replace')
			#print(gpsData)
			
			gga = gpsData.find('$GPRMC,')
			rmc = gpsData.find('$GPRMC,')
			#gsa = gpsData.find('$GPGSA,')
			#gsv = gpsData.find('$GPGSV,')
			#vtg = gpsData.find('$GPVTGM')
			if(gpsData[rmc:rmc+20].find("V") != -1):	#Checking GPS Status
				#Status V
				print("Status V ", end="")
				print()
				IM920.Send('V')
			elif(gpsData[rmc:rmc+20].find("A") != -1):
				#Status A
				gprmc = gpsData[rmc+7:]
				utctime = gpsData[rmc+7:rmc+17]
				lat = gpsData[rmc+20:rmc+29]
				lon = gpsData[rmc+32:rmc+42]
				Lat = round(float(lat[:2]) + float(lat[2:]) / 60.0, 6)
				Lon = round(float(lon[:3]) + float(lon[3:]) / 60.0, 6)
				print("Time:" + str(utctime) + " ", end="")
				print("Lat:" + str(Lat) + " ", end="")
				print("Lon:" + str(Lon) + " ")#, end="")
				IM920.Send(str(Lat))
				IM920.Send(str(Lon))
				'''
				gpgga = gpsData[gga:gga+60]
				hight = gpgga.find(",M,")
				#sHight = float(gpgga[hight-2:hight-1])
				#gHight = float(gpgga[hight+4:hight+4])
				#print("sHight:" + str(sHight) + " ")
				#print("gHight:" + str(gHight) + " ")
		
				'''
			else:
				#No Status Data
				print("Reading GPS Error")
	
		time.sleep(1)
except KeyboardInterrupt:
	pass
	pi.bb_serial_read_close(RX)
	pi.stop()
	print ("Keyboard Interrupt, Serial Cloesd")
	IM920.Send(19200, 'Error')

except:
	pi.bb_serial_read_close(RX)
	pi.stop()
	print("Error, Serial closed") 