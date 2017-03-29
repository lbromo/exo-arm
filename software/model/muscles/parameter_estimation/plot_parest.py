import parest
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

import pickle
import glob, os

import sys
sys.path.append("../")
import muscle_utils

import pprint
pp = pprint.PrettyPrinter(indent=2)

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

FILE_MSE = {}

for file in glob.glob("/afs/ies.auc.dk/group/17gr1035/Private/exo-arm/software/model/muscles/parameter_estimation/*.pickle"):
    with open(file, 'rb') as tmp:
        values = pickle.load(tmp)
        FILE_MSE[file] = values['MSE']

pp.pprint(FILE_MSE)

best_parest = min(FILE_MSE, key=FILE_MSE.get)

pars = {}
with open(best_parest, 'rb') as tmp:
    pars = pickle.load(tmp)

pp.pprint(pars)

triceps_pars = [
    pars[muscle_utils.MUSCLE_NAME.TRICEPS_BRACHII]['C1'],
    pars[muscle_utils.MUSCLE_NAME.TRICEPS_BRACHII]['C2'],
    pars[muscle_utils.MUSCLE_NAME.TRICEPS_BRACHII]['A'],
    pars[muscle_utils.MUSCLE_NAME.TRICEPS_BRACHII]['d'],
    pars[muscle_utils.MUSCLE_NAME.TRICEPS_BRACHII]['max_length'],
    pars[muscle_utils.MUSCLE_NAME.TRICEPS_BRACHII]['optimal_fiber_length'],
    pars[muscle_utils.MUSCLE_NAME.TRICEPS_BRACHII]['tensor_slack_length'],
    pars[muscle_utils.MUSCLE_NAME.TRICEPS_BRACHII]['max_force'],
    pars[muscle_utils.MUSCLE_NAME.TRICEPS_BRACHII]['alpha'],
    pars[muscle_utils.MUSCLE_NAME.TRICEPS_BRACHII]['Spe'],
    pars[muscle_utils.MUSCLE_NAME.TRICEPS_BRACHII]['Sse'],
    pars[muscle_utils.MUSCLE_NAME.TRICEPS_BRACHII]['phi_m'],
    pars[muscle_utils.MUSCLE_NAME.TRICEPS_BRACHII]['phi_v'],
]

biceps_pars = [
    pars[muscle_utils.MUSCLE_NAME.BICEPS_BRACHII]['C1'],
    pars[muscle_utils.MUSCLE_NAME.BICEPS_BRACHII]['C2'],
    pars[muscle_utils.MUSCLE_NAME.BICEPS_BRACHII]['A'],
    pars[muscle_utils.MUSCLE_NAME.BICEPS_BRACHII]['d'],
    pars[muscle_utils.MUSCLE_NAME.BICEPS_BRACHII]['max_length'],
    pars[muscle_utils.MUSCLE_NAME.BICEPS_BRACHII]['optimal_fiber_length'],
    pars[muscle_utils.MUSCLE_NAME.BICEPS_BRACHII]['tensor_slack_length'],
    pars[muscle_utils.MUSCLE_NAME.BICEPS_BRACHII]['max_force'],
    pars[muscle_utils.MUSCLE_NAME.BICEPS_BRACHII]['alpha'],
    pars[muscle_utils.MUSCLE_NAME.BICEPS_BRACHII]['Spe'],
    pars[muscle_utils.MUSCLE_NAME.BICEPS_BRACHII]['Sse'],
    pars[muscle_utils.MUSCLE_NAME.BICEPS_BRACHII]['phi_m'],
    pars[muscle_utils.MUSCLE_NAME.BICEPS_BRACHII]['phi_v'],
]

brachialis_pars = [
    pars[muscle_utils.MUSCLE_NAME.BRACHIALIS]['C1'],
    pars[muscle_utils.MUSCLE_NAME.BRACHIALIS]['C2'],
    pars[muscle_utils.MUSCLE_NAME.BRACHIALIS]['A'],
    pars[muscle_utils.MUSCLE_NAME.BRACHIALIS]['d'],
    pars[muscle_utils.MUSCLE_NAME.BRACHIALIS]['max_length'],
    pars[muscle_utils.MUSCLE_NAME.BRACHIALIS]['optimal_fiber_length'],
    pars[muscle_utils.MUSCLE_NAME.BRACHIALIS]['tensor_slack_length'],
    pars[muscle_utils.MUSCLE_NAME.BRACHIALIS]['max_force'],
    pars[muscle_utils.MUSCLE_NAME.BRACHIALIS]['alpha'],
    pars[muscle_utils.MUSCLE_NAME.BRACHIALIS]['Spe'],
    pars[muscle_utils.MUSCLE_NAME.BRACHIALIS]['Sse'],
    pars[muscle_utils.MUSCLE_NAME.BRACHIALIS]['phi_m'],
    pars[muscle_utils.MUSCLE_NAME.BRACHIALIS]['phi_v'],
]

brachioradialis_pars = [
    pars[muscle_utils.MUSCLE_NAME.BRACHIORADIALIS]['C1'],
    pars[muscle_utils.MUSCLE_NAME.BRACHIORADIALIS]['C2'],
    pars[muscle_utils.MUSCLE_NAME.BRACHIORADIALIS]['A'],
    pars[muscle_utils.MUSCLE_NAME.BRACHIORADIALIS]['d'],
    pars[muscle_utils.MUSCLE_NAME.BRACHIORADIALIS]['max_length'],
    pars[muscle_utils.MUSCLE_NAME.BRACHIORADIALIS]['optimal_fiber_length'],
    pars[muscle_utils.MUSCLE_NAME.BRACHIORADIALIS]['tensor_slack_length'],
    pars[muscle_utils.MUSCLE_NAME.BRACHIORADIALIS]['max_force'],
    pars[muscle_utils.MUSCLE_NAME.BRACHIORADIALIS]['alpha'],
    pars[muscle_utils.MUSCLE_NAME.BRACHIORADIALIS]['Spe'],
    pars[muscle_utils.MUSCLE_NAME.BRACHIORADIALIS]['Sse'],
    pars[muscle_utils.MUSCLE_NAME.BRACHIORADIALIS]['phi_m'],
    pars[muscle_utils.MUSCLE_NAME.BRACHIORADIALIS]['phi_v'],
]


params = triceps_pars + biceps_pars + brachialis_pars + brachioradialis_pars

print(len(params))

estimated = parest.FlexProblem()
muscles = estimated.set_up_muscles(params)
tau, act, m_tau = estimated.simulate(muscles)

act = np.transpose(np.array(act))
m_tau = np.transpose(np.array(m_tau))

b, a = signal.butter(4, 1/(0.5*100), 'lowpass')
tau_lp = signal.lfilter(b, a, tau)

time = np.linspace(0, len(tau)*0.01, len(tau))

act_vstack = np.vstack([a.flatten() for a in act])
m_tau_vstack = np.vstack([t.flatten() for t in m_tau])

np.savetxt('tau_est.dat', tau, header='TORQUE', comments='')
np.savetxt('tau_est_lp.dat', tau_lp, header='TORQUE', comments='')
np.savetxt('act.dat', act_vstack, header='TRICEPS, BICEPS, BRACHIALIS, BRACHIORADIALIS', comments='')
np.savetxt('m_tau.dat', m_tau_vstack, header='TRICEPS, BICEPS, BRACHIALIS, BRACHIORADIALIS', comments='')
np.savetxt('tau_est_lp.dat', tau_lp, header='TORQUE', comments='')


plt.subplot(2, 1, 1)
plt.title('Torque')
plt.plot(time, torque, linewidth=0.5)
plt.plot(time, tau_lp, '--',linewidth=0.5)
plt.subplot(2, 1, 2)
plt.title('Angle')
plt.plot(time, angles, linewidth=0.5)

plt.figure()
plt.subplot(2, 1, 1)
plt.title('Activation Signals')
plt.plot(time, act, linewidth=0.5)
plt.subplot(2, 1, 2)
plt.title('Torque Contributions')
plt.plot(time, m_tau, linewidth=0.5)

## 
# plt.figure()
# for i in range(8):
#     plt.subplot(4, 2, i+1)
#     plt.plot(emg0[:,i])

# plt.figure()
# for i in range(8):
#     plt.subplot(4, 2, i+1)
#     plt.plot(emg1[:,i])

# plt.figure()
# for i in range(1,4):
#     plt.subplot(3, 1, i)
#     plt.plot(imu0[:,i])

# plt.figure()
# for i in range(1,4):
#     plt.subplot(3, 1, i)
#     plt.plot(imu1[:,i])

plt.show()


