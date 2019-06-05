import random
import math
import matplotlib.pyplot as plt

if __name__ == "__main__":
    xx = []
    yy = []
    with open("randomC.txt", mode="w") as f:
        for i in range(100):
            r = random.uniform(9.9, 10.1)
            theta = random.uniform(0, 2*math.pi)
            x = 7.0 *r * math.cos(theta) + 11.0
            y = 1.0 * r * math.sin(theta) + 4.0
            f.write("%f %f %f" % (x, y, 0.0))
            f.write("\n")
            xx.append(x)
            yy.append(y)

    plt.scatter(xx, yy)
    plt.axes().set_aspect('equal', 'datalim')
    plt.grid()
    plt.show()
