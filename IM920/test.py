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
print('a')
IM920.Send('hello')
print('b')


img = cv2.imread("/home/pi/git/kimuralab/SensorModuleTest/Camera/photo1.jpg",0)
bytes = convertIMG2BYTES.IMGtoBYTES(img)

for i in range(0,len(bytes)):
	st = str(bytes[i])
	IM920.Send(st)



#print(bytes)
#st = str(bytes)
#print (type(st))
#print(st)
#IM920.Send(st)
#convertIMG2BYTES.BYTEStoIMG(st)