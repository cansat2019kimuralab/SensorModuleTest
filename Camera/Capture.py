import sys
sys.path.append('/home/pi/git/kimuralab/Other')
import picamera
import time
import Other


def Capture(path):
	with picamera.PiCamera() as camera:
		#camera.hflip = True
		#camera.vflip = True
		camera.rotation = 270
		camera.resolution = (320,240)	#(width,height)
		#camera.start_preview()
		time.sleep(2)
		filepath = Other.fileName(path,"jpg")
		camera.capture(filepath)
	return filepath

if __name__ == "__main__":
	Capture(1)
