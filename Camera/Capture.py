import sys
sys.path.append('/home/pi/git/kimuralab/Other')
import picamera
import Other


def Capture(path, width = 320, height = 240):
	with picamera.PiCamera() as camera:
		camera.rotation = 270
		camera.resolution = (width,height)	#(width,height)
		filepath = Other.fileName(path,"jpg")
		camera.capture(filepath)
	return filepath

if __name__ == "__main__":
	Capture("photo/photo", 160, 120)
