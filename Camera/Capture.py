import sys
sys.path.append('/home/pi/git/kimuralab/Other')
import picamera
import Other


def Capture(path):
	with picamera.PiCamera() as camera:
		camera.rotation = 270
		camera.resolution = (320,240)	#(width,height)
		filepath = Other.fileName(path,"jpg")
		camera.capture(filepath)
	return filepath

if __name__ == "__main__":
	Capture("photo")
