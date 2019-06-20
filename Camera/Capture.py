import time
import picamera

def Capture(count):
    with picamera.PiCamera() as camera:
        camera.hflip = True
        camera.vflip = True
        camera.resolution = (240,320)
        #camera.start_preview()
        time.sleep(2)
        camera.capture('photo'+str(count)+'.jpg')

if __name__ == "__main__":
	Capture(1)