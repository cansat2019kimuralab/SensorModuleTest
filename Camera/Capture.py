import time
import picamera

def Capture(count):
    with picamera.PiCamera() as camera:
        camera.hflip = True
        camera.vflip = True
        camera.resolution = (320,240)	#(width,height)
        #camera.start_preview()
        time.sleep(2)
        camera.capture('/home/pi/photo/photo'+str(count)+'.jpg')

if __name__ == "__main__":
	Capture(1)
