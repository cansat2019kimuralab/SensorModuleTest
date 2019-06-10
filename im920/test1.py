# -*- coding: UTF-8 -*-
import serial
import binascii
import signal
import sys
import time


com = serial.Serial('/dev/ttyS0',19200)

com.flushInput()

com.write(b'TXDA ABCD'+ b'\r\n')
com.readline()
com.write(b'RDID' + b'\r\n')
com.flushOutput()
print('固有ID:' + str(com.readline().strip()))
com.close()

