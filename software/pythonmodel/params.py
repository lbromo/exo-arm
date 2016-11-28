import scipy.constants as consts
import numpy as np

# join 1 -- shoulder to elbow
l1 = 224e-3
a1 = 330e-3
m1 = 1491.070e-3

I1_xx = 17401661.51e-9
I1_yy = 49708861.39e-9
I1_zz = 33589941.15e-9
I1_xy = -9363.03e-9
I1_yz = -40923.12e-9
I1_xz = -10657124.30e-9

I1 = np.matrix([
  [I1_xx, I1_xy, I1_yz],
  [I1_xy, I1_yy, I1_yz],
  [I1_xz, I1_xy, I1_zz]
])


# join 2 -- elbow to hand
l2 = 89e-3
a2 = 227e-3
m2 = 547.77e-3

I2_xx = 658642.154e-9
I2_yy = 3806398.210e-9
I2_zz = 3444384.466e-9
I2_xy = 3462.100e-9
I2_yz = -4984.582e-9
I2_xz = -443444.240e-9

I2 = np.matrix([
  [I2_xx, I2_xy, I2_yz],
  [I2_xy, I2_yy, I2_yz],
  [I2_xz, I2_xy, I2_zz]
])


# misc
g = consts.g
