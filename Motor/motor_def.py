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

motor_prior_l = 0	#Left Motor Speed Prior
motor_prior_r = 0 #Motor Right Speed Prior

def motor(left, right, t = 0.001):
	global motor_prior_l
	global motor_prior_r
	t1 = time.time()
	left = left * (-1)
	while(time.time() - t1 < t):
		if left < motor_prior_l:
			motorPL = motor_prior_l  - 1
		elif left > motor_prior_l:
			motorPL = motor_prior_l + 1
		else:
			motorPL = motor_prior_l

		if right < motor_prior_r:
			motorPR = motor_prior_r - 1
		elif right > motor_prior_r:
			motorPR = motor_prior_r + 1
		else :
			motorPR = motor_prior_r

		motor_prior_l = motorPL
		motor_prior_r = motorPR
		#print(str(motorPL) + "\t" + str(motorPR))
		motorPL = motorPL * 10000
		motorPR = motorPR * 10000
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

		pi1.hardware_PWM(PWMA, 200, abs(motorPL))
		pi1.hardware_PWM(PWMB, 200, abs(motorPR))
		time.sleep(0.005)

try:
	motor(50, 50, 1)
	motor(0, 0, 1)
except KeyboardInterrupt:
	print ("\ndone!")
	pi1.hardware_PWM(PWMA, 0, 0)
	pi1.hardware_PWM(PWMB, 0, 0)
except:
	motor(0,0)
