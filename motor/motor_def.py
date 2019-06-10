
import pigpio
import time

AIN1 = 24
AIN2 = 23
PWMA = 18
BIN1 = 25
BIN2 = 21
PWMB = 13

pi1 = pigpio.pi()
pi1.set_mode(AIN1, pigpio.OUTPUT)
pi1.set_mode(AIN2, pigpio.OUTPUT)
pi1.set_mode(PWMA,pigpio.OUTPUT)
pi1.set_mode(BIN1, pigpio.OUTPUT)
pi1.set_mode(BIN2, pigpio.OUTPUT)
pi1.set_mode(PWMB,pigpio.OUTPUT)

def set_motor(pi1, a, b, c, t):
	pi1.write(AIN1, a)
	pi1.write(AIN2, b)
	pi1.write(PWMA,c)
	time.sleep(t)

def motor(left, right):
	left = left * 10000
	right = right * 10000
	if left > 0:
		pi1.write(AIN1, 1)
		pi1.write(AIN2, 0)
	elif left < 0:
		pi1.write(AIN1, 0)
		pi1.write(AIN2, 1)
	else:
		pi1.write(AIN1, 0)
		pi1.write(BIN1, 0)

	if right > 0:
		pi1.write(BIN1, 1)
		pi1.write(BIN2, 0)
	elif right < 0:
		pi1.write(BIN1, 0)
		pi1.write(BIN2, 1)
	else:
		pi1.write(BIN1, 0)
		pi1.write(BIN1, 0)

	pi1.hardware_PWM(PWMA, 200, abs(left))
	pi1.hardware_PWM(PWMB, 200, abs(right))

try:
	motor(0, 0)
	for i in range(2):
		motor(50, 50)
		time.sleep(1)
		motor(0, 0)
		time.sleep(1)

	for i in range(2):
		motor(-50, -50)
		time.sleep(1)
		motor(0, 0)
		time.sleep(1)

	for i in range(2):
		motor(50, -50)
		time.sleep(1)
		motor(0, 0)
		time.sleep(1)

	for i in range(2):
		motor(-50, 50)
		time.sleep(1)
		motor(0, 0)
		time.sleep(1)

except KeyboardInterrupt:
	print ("done!")
