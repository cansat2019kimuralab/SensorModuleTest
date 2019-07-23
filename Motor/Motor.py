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

def motor(left, right, t = 0.001, mode = 0):
	global motor_prior_l
	global motor_prior_r
	t1 = time.time()

	#if motor wiring changed, check these val
	left = left * (-1)
	right = right * (-1)

	while(time.time() - t1 < t):
		#print(motor_prior_l, motor_prior_r)
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
		motorPL = int(motorPL * 10000)
		motorPR = int(motorPR * 10000)

		if(mode == 1):
			motorPL = int(left * 10000)
			motorPR = int(right * 10000)

		if motorPL > 0:
			pi1.write(AIN1, 1)
			pi1.write(AIN2, 0)
		elif motorPL < 0:
			pi1.write(AIN1, 0)
			pi1.write(AIN2, 1)
		else:
			pi1.write(AIN1, 0)
			pi1.write(BIN1, 0)

		if motorPR > 0:
			pi1.write(BIN1, 1)
			pi1.write(BIN2, 0)
		elif motorPR < 0:
			pi1.write(BIN1, 0)
			pi1.write(BIN2, 1)
		else:
			pi1.write(BIN1, 0)
			pi1.write(BIN1, 0)

		pi1.hardware_PWM(PWMA, 200, abs(motorPL))
		pi1.hardware_PWM(PWMB, 200, abs(motorPR))

		if(mode == 1):
			time.time(t)
		else:
			time.sleep(0.005)

def motor_stop():
	pi1.hardware_PWM(PWMA, 200, 0)
	pi1.hardware_PWM(PWMB, 200, 0)

if __name__ == "__main__":
	try:
		motor(70, 70, 3)
		motor(-70, -70, 3)
		motor(0, 0, 2, 0)
		motor_stop()
	except KeyboardInterrupt:
		motor_stop()
	except Exception as e:
		print(e.message)
		motor_stop()
