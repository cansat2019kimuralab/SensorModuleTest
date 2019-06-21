import sys
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/IM920')
import time
import difflib
import pigpio
import serial
import binascii
import IM920
import convertIMG2BYTES
import cv2

'''
pi=pigpio.pi()
pi.set_mode(22,pigpio.OUTPUT)
pi.write(22,0)
time.sleep(1)
pi.write(22,0)
'''



img = cv2.imread("/home/pi/git/kimuralab/SensorModuleTest/Camera/photo1.jpg",0)
byte = convertIMG2BYTES.IMGtoBYTES(img)
#print(byte[0:100])

for i in range(0,len(byte),64):
	IM920.IMSend(byte[i:i+63])
	print(i,'/',len(byte))
'''
for i in range(0,len(byte)):
	IM920.IMSend(byte[i])
	print(i,'/',len(byte))


for i in range(0,len(byte),16):
	st = str(byte[i:i+15])
	IM920.Send(st)
	print(i,'/',len(byte))
'''
#IM920.IMSend(byte)
#convertIMG2BYTES.BYTEStoIMG(st)