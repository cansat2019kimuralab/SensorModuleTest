# -*- coding: utf-8 -*-

import serial
import binascii
import signal
import sys
import platform
import time
import convertIMG2BYTES

portnumber = 'COM4'

def signal_handler(signal, frame):
	'''
	ctrl+cの命令
	'''
	print('exit')
	sys.exit()

def setSerial(mybaudrate = 19200):
	'''
	serial.Serialの設定
	mybaudrate:ボーレート
	'''
	com = serial.Serial(
		port	 = portnumber,
		baudrate = mybaudrate,
		bytesize = serial.EIGHTBITS,
		parity   = serial.PARITY_NONE,
		timeout  = None,
		xonxoff  = False,
		rtscts   = False,
		writeTimeout = None,
		dsrdtr	   = False,
		interCharTimeout = None)

	#bufferクリア
	com.flushInput()
	com.flushOutput()
	return com

def Rdid(mybaudrate = 19200):
	'''
	固有IDの読み出し
	mybaudrate:ボーレート
	'''
	com = setSerial(mybaudrate)
	#print(com)
	com.flushInput()
	com.write(b'RDID' + b'\r\n')
	com.flushOutput()
	#print(dir(com))
	print('固有ID:' + str(com.readline().strip()))
	com.close()

def Rrid(mybaudrate = 19200):
	'''
	受信IDの読み出し
	mybaudrate:ボーレート
	'''
	com = setSerial(mybaudrate)
	com.flushInput()
	com.write(b'RRID' + b'\r\n')
	com.flushOutput()
	print('受信ID:' + str(com.readline().strip()))
	com.close()

def Stch(setch, mybaudrate = 19200):
	'''
	無線通信チャンネルの設定
	mybaudrate:現在のボーレート
	setch:セットするチャンネル(文字列でもってくること)
		01 920.6MHz	09 922.2MHz
		02 920.8MHz	10 922.4MHz
		03 921.0MHz	11 922.6MHz
		04 921.2MHz	12 922.8MHz
		05 921.4MHz	13 923.0MHz
		06 921.6MHz	14 923.2MHz
		07 921.8MHz	15 923.4MHz
		08 922.0MHz
	'''
	com = setSerial(mybaudrate)
	com.flushInput()
	com.write(b'ENWR' + b'\r\n')
	com.flushOutput()
	com.readline()
	com.write(b'Stch ' + setch.encode('utf-8') + b'\r\n')
	com.flushOutput()
	com.readline()
	com.write(b'DSWR' + b'\r\n')
	com.flushOutput()
	com.readline()
	com.close()

def Rdch(mybaudrate = 19200):
	'''
	無線通信チャンネルの読み出し
	mybaudrate:現在のボーレート
	'''
	com = setSerial(mybaudrate)
	com.flushInput()
	com.write(b'RDCH' + b'\r\n')
	com.flushOutput()
	ch = com.readline().strip()
	if ch in ['01']:
		print('無線通信チャンネル:' + '01 920.6MHz')
	elif ch in ['02']:
		print('無線通信チャンネル:' + '02 920.8MHz')
	elif ch in ['03']:
		print('無線通信チャンネル:' + '03 921.0MHz')
	elif ch in ['04']:
		print('無線通信チャンネル:' + '04 921.2MHz')
	elif ch in ['05']:
		print('無線通信チャンネル:' + '05 921.4MHz')
	elif ch in ['06']:
		print('無線通信チャンネル:' + '06 921.6MHz')
	elif ch in ['07']:
		print('無線通信チャンネル:' + '07 921.8MHz')
	elif ch in ['08']:
		print('無線通信チャンネル:' + '08 922.0MHz')
	elif ch in ['09']:
		print('無線通信チャンネル:' + '09 922.2MHz')
	elif ch in ['10']:
		print('無線通信チャンネル:' + '10 922.4MHz')
	elif ch in ['11']:
		print('無線通信チャンネル:' + '11 922.6MHz')
	elif ch in ['12']:
		print('無線通信チャンネル:' + '12 922.8MHz')
	elif ch in ['13']:
		print('無線通信チャンネル:' + '13 923.0MHz')
	elif ch in ['14']:
		print('無線通信チャンネル:' + '14 923.2MHz')
	elif ch in ['15']:
		print('無線通信チャンネル:' + '15 923.4MHz')
	#com.readline()
	com.close()

def Sbrt(setbaudrate, mybaudrate = 19200):
	'''
	ボーレート(シリアル通信速度)の設定
	mybaudrate:現在のボーレート
	setbaudrate:セットするボーレート(文字列でもってくること)
		0 1200bps
		1 2400bps
		2 4800bps
		3 9600bps
		4 19200bps
		5 38400bps
	'''
	com = setSerial(mybaudrate)
	com.flushInput()
	com.write(b'ENWR' + b'\r\n')
	com.flushOutput()
	com.readline()
	com.write(b'SBRT ' + setbaudrate.encode('utf-8') + b'\r\n')
	com.flushOutput()
	com.readline()
	com.write(b'DSWR' + b'\r\n')
	com.flushOutput()
	com.readline()
	com.close()

def Rdrs(mybaudrate = 19200):
	'''
	RSSI値(現在の信号強度レベル)読み出し
	mybaudrate:現在のボーレート
		ASCII文字(0~9,A~F)2文字で出力
	'''
	com = setSerial(mybaudrate)
	com.flushInput()
	com.write(b'RDRS' + b'\r\n')
	com.flushOutput()
	print('信号強度:' + str(com.readline().strip()))
	#com.readline()
	com.close()

def Stpo(setoutput, mybaudrate = 19200):
	'''
	送信出力の設定
	mybaudrate:現在のボーレート
	setoutput:セットする送信出力(文字列でもってくること)
		1 -10dBm(0.1mW)
		2   0dBm(1mW)
		3  10dBm(10mW)
	'''
	com = setSerial(mybaudrate)
	com.flushInput()
	com.write(b'ENWR' + b'\r\n')
	com.flushOutput()
	com.readline()
	com.write(b'STPO ' + setoutput.encode('utf-8') + b'\r\n')
	com.flushOutput()
	com.readline()
	com.write(b'DSWR' + b'\r\n')
	com.flushOutput()
	com.readline()
	com.close()

def Rdpo(mybaudrate = 19200):
	'''
	送信出力読み出し
	mybaudrate:現在のボーレート
		1 -10dBm(0.1mW)
		2   0dBm(1mW)
		3  10dBm(10mW)
	'''
	com = setSerial(mybaudrate)
	com.flushInput()
	com.write(b'RDPO' + b'\r\n')
	com.flushOutput()
	op = com.readline().strip()
	if op in ['1']:
		print('送信出力:' + '1 -10dBm(0.1mW)')
	elif op in ['2']:
		print('送信出力:' + '2   0dBm(1mW)')
	elif op in ['3']:
		print('送信出力:' + '3  10dBm(10mW)')
	#com.readline()
	com.close()

def Strt(setspeed, mybaudrate = 19200):
	'''
	無線通信速度の設定
	mybaudrate:現在のボーレート
	setspeed:セットする無線通信速度(文字列でもってくること)
		1 高速通信モード(無線通信速度 50kbps)
		2 長距離モード(無線通信速度 1.25kbps)
	'''
	com = setSerial(mybaudrate)
	com.flushInput()
	com.write(b'ENWR' + b'\r\n')
	com.flushOutput()
	com.readline()
	com.write(b'STRT ' + setspeed.encode('utf-8') + b'\r\n')
	com.flushOutput()
	com.readline()
	com.write(b'DSWR' + b'\r\n')
	com.flushOutput()
	com.readline()
	com.close()

def Rdrt(mybaudrate = 19200):
	'''
	無線通信速度の読み出し
	mybaudrate:現在のボーレート
		1 高速通信モード(無線通信速度 50kbps)
		2 長距離モード(無線通信速度 1.25kbps)
	'''
	com = setSerial(mybaudrate)
	com.flushInput()
	com.write(b'RDRT' + b'\r\n')
	com.flushOutput()
	sp = com.readline().strip()
	if sp in ['1']:
		print('無線通信速度:' + '高速通信モード(無線通信速度 50kbps)')
	elif sp in ['2']:
		print('無線通信速度:' + '2 長距離モード(無線通信速度 1.25kbps)')
	#com.readline()
	com.close()

def Srid(args, mybaudrate = 19200):
	'''
	ペアリング
	mybaudrate:ボーレート
	args:ペアリングしたいID(文字列にすること)
	'''
	com = setSerial(mybaudrate)
	com.flushInput()
	com.write(b'ENWR' + b'\r\n')
	com.flushOutput()
	com.readline()
	com.write(b'SRID ' + args.encode('utf-8') + b'\r\n')
	com.flushOutput()
	com.readline()
	com.write(b'DSWR' + b'\r\n')
	com.flushOutput()
	com.readline()
	com.close()

def Erid(mybaudrate = 19200):
	'''
	ペアリングの削除
	全て削除されるため注意!
	mybaudrate:ボーレート
	'''
	com = setSerial(mybaudrate)
	com.flushInput()
	com.write(b'ENWR' + b'\r\n')
	com.flushOutput()
	com.readline()
	com.write(b'ERID' + b'\r\n')
	com.flushOutput()
	com.readline()
	com.write(b'DSWR' + b'\r\n')
	com.flushOutput()
	com.readline()
	com.close()

def Send(args, mybaudrate = 19200):
	'''
	送信
	mybaudrate:ボーレート
	args:送信したい文字列 (数字の場合も文字列型にすること)
	'''
	com = setSerial(mybaudrate)
	com.flushInput()
	com.write(b'TXDA' + binascii.b2a_hex(args.encode('utf-8')) + b'\r\n')
	com.readline()
	com.flushOutput()
	com.close()

	
def IMSend(byte, mybaudrate = 19200):
	'''
	送信
	mybaudrate:ボーレート
	args:送信したい文字列 (数字の場合も文字列型にすること)
	'''
	com = setSerial(mybaudrate)
	com.flushInput()
	com.write(b'TXDA' + byte + b'\r\n')
	com.readline()
	com.flushOutput()
	com.close()

def Reception(mybaudrate = 19200):
	'''
	受信
	アスキーコードから文字列に変換したものを返す
	mybaudrate:ボーレート
	'''
	com = setSerial(mybaudrate)
	com.flushInput()

	text = ""
	cngtext = []

	try:
		text = com.readline().decode('utf-8').strip() #受信と空白の削除
		com.close()
		text = text.replace("\r\n","")
		text = text.split(":")[1]
		text = text.split(",")

		for x in text:
			cngtext.append(int(x,16))

	except Exception:
		print("not input data")

	return cngtext

def Repeater(mybaudrate = 19200):
	'''
	中継機化
	mybaudrate:ボーレート
	'''
	signal.signal(signal.SIGINT, signal_handler)

	while True:
		data = Reception(mybaudrate)
		if len(data) != 0:
			print("input data:", data)
			Send(19200, data)

def Rprm(mybaudrate = 19200):
	'''
	パラメータ一括読み出し
	mybaudrate:現在のボーレート
	'''
	com = setSerial(mybaudrate)
	com.flushInput()
	com.write(b'RPRM' + b'\r\n')
	com.flushOutput()
	print(com.readline().strip())
	#com.readline()
	com.close()


if __name__ == '__main__':
	#Send('Hello')  #文字列送信
	txt = []
	count = 0
	try:		
		while 1:
			count += 1
			print(count)
			txt.append(Reception())
	except KeyboardInterrupt:
		cngbyte = bytes(txt)
		convertIMG2BYTES.BYTEStoIMG(cngbyte)
		#print(cngbyte)
		print(type(cngbyte))
	'''
	
	try:
		txt.append(Reception())
		count += 1
		print(count)

	except TimeoutError:
		cngbyte = bytes(txt)
		print(cngbyte)
		print(type(cngbyte))
	'''

	#Rdid()		#固有ID 