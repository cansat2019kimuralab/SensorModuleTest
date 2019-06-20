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

for i in range(0,len(byte),2):
	IM920.IMSend(byte[i:i+1])

#convertIMG2BYTES.BYTEStoIMG(st)