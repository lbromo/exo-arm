import parest
import numpy as np
import matplotlib.pyplot as plt

torque = []
angles = []
emg0 = np.empty((0,8));
emg1 = np.empty((0,8));

imu0 = np.empty((0,7));
imu1 = np.empty((0,7));

for tau in parest.torque_out:
    torque = torque + list(tau)

for angle in parest.angles_in:
    angles = angles + list(angle)

for e in parest.emg0_in:
    emg0 = np.concatenate((emg0, e), axis=0)

for e in parest.emg1_in:
    emg1 = np.concatenate((emg1, e), axis=0)

for m in parest.imu0_in:
    imu0 = np.concatenate((imu0, m), axis=0)

for m in parest.imu1_in:
    imu1 = np.concatenate((imu1, m), axis=0)

emg0_vstack = np.vstack([e.flatten() for e in emg0])
emg1_vstack = np.vstack([e.flatten() for e in emg1])
imu0_vstack = np.vstack([m.flatten() for m in imu0[:,1:4]])
imu1_vstack = np.vstack([m.flatten() for m in imu1[:,1:4]])
np.savetxt('emg0.dat', emg0_vstack, delimiter=',', header='POD1, POD2, POD3, POD4, POD5, POD6, POD7, POD8', comments='')
np.savetxt('emg1.dat', emg1_vstack, delimiter=',', header='POD1, POD2, POD3, POD4, POD5, POD6, POD7, POD8', comments='')
np.savetxt('imu0.dat', imu0_vstack, delimiter=',', header='ACC1, ACC2, ACC3', comments='')
np.savetxt('imu1.dat', imu1_vstack, delimiter=',', header='ACC1, ACC2, ACC3', comments='')
np.savetxt('torque.dat', torque, header='TORQUE', comments='')
np.savetxt('angles.dat', angles, header='ANGLE', comments='')

plt.subplot(2, 1, 1)
plt.plot(torque)
plt.subplot(2, 1, 2)
plt.plot(angles)

plt.figure()
for i in range(8):
    plt.subplot(4, 2, i+1)
    plt.plot(emg0[:,i])

plt.figure()
for i in range(8):
    plt.subplot(4, 2, i+1)
    plt.plot(emg1[:,i])

plt.figure()
for i in range(1,4):
    plt.subplot(3, 1, i)
    plt.plot(imu0[:,i])

plt.figure()
for i in range(1,4):
    plt.subplot(3, 1, i)
    plt.plot(imu1[:,i])

plt.show()
