import serial
import numpy as np
ser = serial.Serial('/dev/ttyACM0', 9600)
while True:
	x=float(ser.readline())
	angle=-8.723e-08*x**4 - 4.832e-05*x**3 + 0.01916*x**2 - 2.413*x + 114.1
	print angle



## angle/adcvalue fit func


# import matplotlib.pyplot as plt

# # Scientific libraries
# import numpy as np

# points = np.array([(0, 113), (5, 102), (10, 93), (15, 83), (20, 75), (25, 65), (30, 58), (35, 50), (40, 44), (45, 38), (50, 32), (55, 30), (60, 27), (65, 25), (70, 22), (75, 20), (80, 17), (85, 13), (90, 10), (95, 8), (100, 7), (105, 5), (110, 3), (115, 1), (120, 0)])

# # get x and y vectors
# x = points[:,0]
# y = points[:,1]

# # calculate polynomial
# z = np.polyfit(x, y, 4)
# f = np.poly1d(z)
# print f

# # calculate new x's and y's
# x_new = np.linspace(x[0], x[-1], 50)
# y_new = f(x_new)

# plt.plot(x_new,y_new)
# plt.plot(x,y,'*')
# plt.show()