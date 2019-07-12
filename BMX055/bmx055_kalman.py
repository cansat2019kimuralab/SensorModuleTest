import time
import numpy as np
import BMX055


def lkf(T, Y, U, mu0, Sigma0, A, B, C, Q, R):
	mu = mu0
	Sigma = Sigma0
	M = mu

	mu = A * mu + B * U[i]
	Sigma_ = Q + A * Sigma * A.T

	yi = Y[i+1] - C + mu_
	S = C * Sigma_ * C.T + R
	K = Sigma_ * C.T * S.I
	mu = mu_ + K * yi
	Sigma = Sigma_ - K * C * Sigma_

	return M

if __name__ == "__main__":
	try:
		BMX055.bmx055_setup()

		acc = []
		gyr = []
		for i in range(1000):
			bmx055data = BMX055.bmx055_read()
			accdata = [bmx055data[0], bmx055data[1], bmx055data[2]]
			acc.append(accdata)

		for i in range(len(acc)):
			for j in range(3):
			print(str(acc[i][j]) + "\t", end="")
			print()

		accAve = np.average(acc,0)
		accVar = np.var(acc, 0)
		print(accAve, accVar)
		dt = 0.001

		A = np.mat([[1, dt], [0, 1]])
		B = np.mat([[0],[1]])
		C = np.mat([[1, 0],[0, 1]])
		D = np.mat([[1, 0],[0, 1]])

		Q = np.mat([[0], [accVar[0]]])
		R = np.mat([[0], [0]])

		dt = 0.001
		mu = mu0
		Sigma = Sigma0

		while 1:
			mu = mu0
			Sigma = Sigma0

			mu_ = A * mu + B * U[i]
			Sigma_ = Q + A * Sigma * A.T

			yi = Y[i+1] - C * mu_
			S = C * Sigma_ * C.T + R
			K = Sigma_ * C.T * S.I
			mu = mu_ + K * yi
			Sigma = Sigma_ - K * C * Sigma_

			print(M)
	except KeyboardInterrupt:
		print("KeyboardInterrupt")
	except Exception as e:
		print(e.message)
