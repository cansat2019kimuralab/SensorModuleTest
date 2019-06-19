# -*- coding: utf-8 -*-

import smbus
import time

ACC_ADDRESS = 0x19
ACC_REGISTER_ADDRESS = 0x02
GYR_ADDRESS = 0x69
GYR_REGISTER_ADDRESS = 0x02
MAG_ADDRESS = 0x13
MAG_REGISTER_ADDRESS = 0x42

def bmx055_setup():
	'''
	BMX055セットアップ
	'''
	#time.sleep(3)
	i2c = smbus.SMBus(1)
	data = i2c.read_byte_data(MAG_ADDRESS, 0x4B)
	if(data == 0):
		i2c.write_byte_data(MAG_ADDRESS, 0x4B, 0x83)
		time.sleep(0.1)

	i2c.write_byte_data(MAG_ADDRESS, 0x4B, 0x01)
	time.sleep(0.1)
	i2c.write_byte_data(MAG_ADDRESS, 0x4C, 0x00)
	time.sleep(0.1)
	i2c.write_byte_data(MAG_ADDRESS, 0x4E, 0x84)
	time.sleep(0.1)
	i2c.write_byte_data(MAG_ADDRESS, 0x51, 0x04)
	time.sleep(0.1)
	i2c.write_byte_data(MAG_ADDRESS, 0x52, 0x0F)
	time.sleep(0.1)
	i2c.close()

def acc_dataRead():
	'''
	加速度データ読み込み
	'''
	i2c = smbus.SMBus(1)
	accData = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
	value = [0.0, 0.0, 0.0]
	for i in range(6):
		accData[i] = i2c.read_byte_data(ACC_ADDRESS, ACC_REGISTER_ADDRESS+i)

	for i in range(3):
		value[i] = (accData[2*i+1] * 16) + ((accData[2*i] & 0xF0) / 16)
		value[i] = value[i] if value[int(i)] < 2048 else value[i] - 4096
		value[i] = value[i] * 0.0098

	i2c.close()

	return value

def gyr_dataRead():
	'''
	ジャイロデータ読み込み
	'''
	i2c = smbus.SMBus(1)
	gyrData = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
	value = [0.0, 0.0, 0.0]
	for i in range(6):
		gyrData[i] = i2c.read_byte_data(GYR_ADDRESS, GYR_REGISTER_ADDRESS+i)

	for i in range(3):
		value[i] = (gyrData[2*i+1] * 256) + gyrData[i]
		value[i] = value[i] if value[i] > 32767 else value[i] - 65536
		value[i] = value[i] * 0.0038

	i2c.close()

	return value

def mag_dataRead():
	'''
	地磁気データ読み込み
	'''
	i2c = smbus.SMBus(1)
	magData = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
	value = [0.0, 0.0, 0.0]
	for i in range(8):
		magData[i] = i2c.read_byte_data(MAG_ADDRESS, MAG_REGISTER_ADDRESS + i)
		#print(str(magData[i]) + " ", end="")
	#print()

	for i in range(3):
		if i != 2:
			value[i] = ((magData[2*i+1] *256) + (magData[2*i] & 0xF8)) / 8
			#print(str(value[i]) + " ", end="")
			if value[i] > 4095:
				value[i] = value[i] - 8192
		else:
			value[i] = ((magData[2*i+1] * 256) | (magData[2*i] & 0xF8)) / 2
			#print(str(value[i]) + " ", end="")
			if value[i] > 16383:
				value[i] = value[i] - 32768

	#print()
	i2c.close()

	return value

def bmx055_read():
	'''
	全データ読み込み
	'''
	accx, accy, accz = acc_dataRead()
	gyrx, gyry, gyrz = gyr_dataRead()
	magx, magy, magz = mag_dataRead()

	#print("[%f, %f, %f] " % (accx, accy, accz), end="")
	#print("[%f, %f, %f] " % (gyrx, gyry, gyrz), end="")
	#print("[%f, %f, %f] " % (magx, magy, magz), end="")
	#print()

	value = [accx, accy, accz, gyrx, gyry, gyrz, magx, magy, magz]
	for i in range(len(value)):
		value[i] = round(value[i], 4)

	return 	value

if __name__ == '__main__':
	try:
		bmx055_setup()
		while 1:
			bmxData = bmx055_read()
			for i in range(len(bmxData)):
				print(str(bmxData[i]) + " ", end="")
			print()
			time.sleep(1)

	except KeyboardInterrupt:
		print()
