import time
import picamera

def CAPTURE(count):
    with picamera.PiCamera() as camera:
        camera.hflip = True
        camera.vflip = True
        camera.resolution = (640,480)
        camera.start_preview()
        time.sleep(2)
        camera.capture('photo'+str(count)+'.jpg')

if __name__ == "__main__":
	CAPTURE(1)
