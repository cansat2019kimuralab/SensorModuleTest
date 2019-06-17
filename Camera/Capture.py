import time
import picamera

def CAPTURE(count):
    with picamera.PiCamera() as camera:
        camera.hflip = True
        camera.vflip = True
        camera.resoltion = (640,480)
        #camera.start_preview()
        time.sleep(2)
        camera.capture('photo'+str(count)+'.jpg')