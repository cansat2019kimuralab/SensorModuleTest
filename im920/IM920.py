#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
パッケージpyserialをインストールすること
pytho2.x系で動作(python3.*系も動作検証済み)
Creater：Kaname Takano
'''
import serial
import binascii
import signal
import sys
import platform

#platformの切り替え
'''
if platform.system() == 'Windows':  #windows用
    portnumber = 'COM4'
elif platform.system() == 'Linux': #Linux用
    portnumber = '/dev/ttyAMA0'
'''
portnumber = '/dev/ttyS0'

'''
ctrl+cの命令
'''
def signal_handler(signal, frame):
    print('exit')
    sys.exit()

'''
serial.Serialの設定
mybaudrate:ボーレート
'''
#mybaudrate=19200
def setSerial(mybaudrate):
    com = serial.Serial(
        port     = portnumber,
        baudrate = mybaudrate,
        bytesize = serial.EIGHTBITS,
        parity   = serial.PARITY_NONE,
        timeout  = None,
        xonxoff  = False,
        rtscts   = False,
        writeTimeout = None,
        dsrdtr       = False,
        interCharTimeout = None)

    #bufferクリア
    com.flushInput()
    com.flushOutput()
    return com

'''
固有IDの読み出し
mybaudrate:ボーレート
'''
def Rdid(mybaudrate):
    com = setSerial(mybaudrate)
    print(com)
    com.flushInput()
    print("b")
    com.write(b'RDID' + b'\r\n')
    print("c")
    com.flushOutput()
    print("d")
    #print(dir(com))
    print('固有ID:' + com.readline().strip())
    print("e")
    com.close()

'''
受信IDの読み出し
mybaudrate:ボーレート
'''
def Rrid(mybaudrate):
    com = setSerial(mybaudrate)
    com.flushInput()
    com.write(b'RRID' + b'\r\n')
    com.flushOutput()
    print('受信ID:' + com.readline().strip())
    com.close()

'''
無線通信チャンネルの設定
mybaudrate:現在のボーレート
setch:セットするチャンネル(文字列でもってくること)
    01 920.6MHz    09 922.2MHz
    02 920.8MHz    10 922.4MHz
    03 921.0MHz    11 922.6MHz
    04 921.2MHz    12 922.8MHz
    05 921.4MHz    13 923.0MHz
    06 921.6MHz    14 923.2MHz
    07 921.8MHz    15 923.4MHz
    08 922.0MHz
'''
def Stch(mybaudrate, setch):
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

'''
無線通信チャンネルの読み出し
mybaudrate:現在のボーレート
'''
def Rdch(mybaudrate):
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
def Sbrt(mybaudrate, setbaudrate):
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

'''
RSSI値(現在の信号強度レベル)読み出し
mybaudrate:現在のボーレート
    ASCII文字(0~9,A~F)2文字で出力
'''
def Rdrs(mybaudrate):
    com = setSerial(mybaudrate)
    com.flushInput()
    com.write(b'RDRS' + b'\r\n')
    com.flushOutput()
    print('信号強度:' + com.readline().strip())
    #com.readline()
    com.close()

'''
送信出力の設定
mybaudrate:現在のボーレート
setoutput:セットする送信出力(文字列でもってくること)
    1 -10dBm(0.1mW)
    2   0dBm(1mW)
    3  10dBm(10mW)
'''
def Stpo(mybaudrate, setoutput):
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

'''
送信出力読み出し
mybaudrate:現在のボーレート
    1 -10dBm(0.1mW)
    2   0dBm(1mW)
    3  10dBm(10mW)
'''
def Rdpo(mybaudrate):
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

'''
無線通信速度の設定
mybaudrate:現在のボーレート
setspeed:セットする無線通信速度(文字列でもってくること)
    1 高速通信モード(無線通信速度 50kbps)
    2 長距離モード(無線通信速度 1.25kbps)
'''
def Strt(mybaudrate, setspeed):
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

'''
無線通信速度の読み出し
mybaudrate:現在のボーレート
    1 高速通信モード(無線通信速度 50kbps)
    2 長距離モード(無線通信速度 1.25kbps)
'''
def Rdrt(mybaudrate):
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

'''
ペアリング
mybaudrate:ボーレート
args:ペアリングしたいID(文字列にすること)
'''
args='3156'
mybaudrate=19200
def Srid(mybaudrate, args):
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

'''
ペアリングの削除
全て削除されるため注意!
mybaudrate:ボーレート
'''
def Erid(mybaudrate):
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

'''
送信
mybaudrate:ボーレート
args:送信したい文字列 (数字の場合も文字列型にすること)
'''
def Send(mybaudrate, args):
    print ('a')
    com = setSerial(mybaudrate)
    print ('b')
    com.flushInput()
    print ('c')
    com.write(b'TXDA' + binascii.b2a_hex(args.encode('utf-8')) + b'\r\n')
    print ('d')
    com.flushOutput()
    print ('e')
    #com.readline()
    print ('f')
    com.close()

'''
受信
アスキーコードから文字列に変換したものを返す
mybaudrate:ボーレート
'''
def Reception(mybaudrate):
    com = setSerial(mybaudrate)
    com.flushInput()

    text = ""
    cngtext = ""
    try:
        text = com.readline().decode('utf-8').strip() #受信と空白の削除
        com.close()
        text = text.replace("\r\n","")
        text = text.split(":")[1]
        text = text.split(",")

        for x in text:
            cngtext += chr(int(x,16))

    except Exception:
        print("not input data")

    return cngtext

'''
中継機化
mybaudrate:ボーレート
'''
def Repeater(mybaudrate):
    signal.signal(signal.SIGINT, signal_handler)

    while True:
        data = Reception(mybaudrate)
        if len(data) != 0:
            print("input data:", data)
            Send(19200, data)

'''
パラメータ一括読み出し
mybaudrate:現在のボーレート
'''
def Rprm(mybaudrate):
    com = setSerial(mybaudrate)
    com.flushInput()
    com.write(b'RPRM' + b'\r\n')
    com.flushOutput()
    print(com.readline().strip())
    #com.readline()
    com.close()
if __name__ == '__main__':
    #ペアリング
    #Srid(19200,'5187')
 
    #削除
    #Erid(19200)
 
    #文字列送信
    Send(19200, 'Hello')
 
    #文字列受信
    #print Reception(19200)
 
    #中継機化
    #Repeater(19200)
 
    #固有ID
    Rdid(19200)
 
    #ボーレート設定
    #Sbrt(19200, '4')
