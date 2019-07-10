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
motor_prior_r = 0	#Right Motor Speed Prior

def motor(left, right, t = 0.001):
	global motor_prior_l
	global motor_prior_r
	t1 = time.time()

	#if motor wiring changed, check these val
	left = left * (-1)
	right = right * 1

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

def motor_stop():
	pi1.hardware_PWM(PWMA, 200, 0)
	pi1.hardware_PWM(PWMB, 200, 0)

if __name__ == "__main__":
	try:
		motor(50, -50, 3)
		motor(0, 0, 1)
	except KeyboardInterrupt:
		motor_stop()
	except:
		motor_stop()
