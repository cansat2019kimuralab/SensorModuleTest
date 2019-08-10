import sys
sys.path.append('/home/pi/git/kimuralab/Other')
import picamera
import time
import Other

def Capture(path, width = 320, height = 240):
	filepath = ""
	try:
		with picamera.PiCamera() as camera:
			camera.rotation = 270
			camera.resolution = (width,height)	#(width,height)
			filepath = Other.fileName(path,"jpg")
			camera.capture(filepath)
	except picamera.exc.PiCameraMMALError:
		filepath = "Null"
		time.sleep(0.8)
	return filepath

if __name__ == "__main__":
	photoName = Capture("photo/photo", 160, 120)
	print(photoName)
