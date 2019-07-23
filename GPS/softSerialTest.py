import sys
import time
import difflib
import pigpio

RX=26

if __name__ == "__main__":
	try:
		pi = pigpio.pi()
		pi.set_mode(RX, pigpio.INPUT)
		pi.bb_serial_read_open(RX, 9600, 8)

		print("DATA - SOFTWARE SERIAL")
		while 1:
			(count, data) = pi.bb_serial_read(RX)
			if count:
				data = data.decode('utf-8', 'replace')
				print(data)
				
			time.sleep(1)

	except:
		print("Error")
		pi.bb_serial_read_close(RX)
		pi.stop()
	
