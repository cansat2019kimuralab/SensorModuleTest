
import pigpio
import time

AIN1 = 24
AIN2=23
PWMA=18

pi1 = pigpio.pi()
pi1.set_mode(AIN1, pigpio.OUTPUT)
pi1.set_mode(AIN2, pigpio.OUTPUT)
pi1.set_mode(PWMA,pigpio.OUTPUT)

def set_motor(pi1, a, b, c, t):
	pi1.write(AIN1, a)
	pi1.write(AIN2, b)
	pi1.write(PWMA,c)
	time.sleep(t)

try:
	set_motor(pi1, 0, 0, 1, 0.5) # stop (neutral)
	for i in range(4):
	set_motor(pi1, 1, 0, 1, 0.3) # normal rotation
	set_motor(pi1, 0, 0, 1, 2.0) # brake


for i in range(4):
	set_motor(pi1, 0, 1, 1, 0.3) # reverse rotation
	set_motor(pi1, 0, 0, 1, 2.0) # brake

except KeyboardInterrupt:
	print "done."

set_motor(pi1, 0, 0, 1, 0.5) # stop (neutral)
pi1.set_mode(AIN1, pigpio.INPUT)
pi1.set_mode(AIN2, pigpio.INPUT)
pi1.set_mode(PWMA,pigpio.INPUT)
pi1.stop()