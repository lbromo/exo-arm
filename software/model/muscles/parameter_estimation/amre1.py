import numpy as np
import scipy.signal
import matplotlib.pyplot as plt

import os
import pwd
user = pwd.getpwuid( os.getuid() )[0]

kinkom=np.genfromtxt(
    "/afs/ies.auc.dk/group/17gr1035/Private/logs/kincom_logs/morten/april/MRE1_clean",
    delimiter=','
)

angle = abs(kinkom[:,1])
force = kinkom[:,-1]
kinkom_time = kinkom[:,0]

emg1_meas = np.genfromtxt(
    "/afs/ies.auc.dk/group/17gr1035/Private/logs/emg_logs/mr_morten/april/MRE1_emg0.log",
    delimiter=',')

emg0_meas = np.genfromtxt(
    "/afs/ies.auc.dk/group/17gr1035/Private/logs/emg_logs/mr_morten/april/MRE1_emg1.log",
    delimiter=',')

imu1_meas = np.genfromtxt(
    "/afs/ies.auc.dk/group/17gr1035/Private/logs/emg_logs/mr_morten/april/MRE1_imu0.log",
    delimiter=',')

imu0_meas = np.genfromtxt(
    "/afs/ies.auc.dk/group/17gr1035/Private/logs/emg_logs/mr_morten/april/MRE1_imu1.log",
    delimiter=',')

tmp = np.array([imu1_meas[1:,1][i] - imu1_meas[1:,1][i-1] for i in range(1, len(imu1_meas[1:,1]))])
dA = np.array([angle[i] - angle[i-1] for i in range(1, len(angle))])

imu_start = np.where( tmp > 0.1 )[0][0] + 5
imu_stop = np.where( tmp > 0.1 )[0][-1]

t_start = imu1_meas[1:,0][imu_start]
t_stop  = imu1_meas[1:,0][imu_stop]

angle_start = np.where( abs(dA) >= 0.4 )[0][0]
# We lost some measurements from the myo, so we cut off a after that
angle_stop = np.where(kinkom_time >= imu1_meas[1:,0][imu_stop] - t_start)[0][0] + angle_start
angles = angle[angle_start:angle_stop]
kinkom_time = kinkom_time[angle_start:angle_stop] - kinkom_time[angle_start]

emg0_start_idx = np.where(emg0_meas[1:,0] >= imu1_meas[1:,0][imu_start])[0][0]
emg0_stop_idx  = np.where(emg0_meas[1:,0] >= imu1_meas[1:,0][imu_stop])[0][0]

emg1_start_idx = np.where(emg1_meas[1:,0] >= imu1_meas[1:,0][imu_start])[0][0]
emg1_stop_idx  = np.where(emg1_meas[1:,0] >= imu1_meas[1:,0][imu_stop])[0][0]

## Setup
angles_in = angles
emg0_training = emg0_meas[1:,1:][0:emg0_start_idx]
emg0_in = emg0_meas[1:,1:][emg0_start_idx:emg0_stop_idx]
emg1_training = emg1_meas[1:,1:][0:emg1_start_idx]
emg1_in = emg1_meas[1:,1:][emg1_start_idx:emg1_stop_idx]
torque_out = -force[angle_start:angle_stop] * 0.25

# Resample
emg0_time = emg0_meas[1:,0][emg0_start_idx:emg0_stop_idx] - emg0_meas[1:,0][emg0_start_idx]
emg1_time = emg1_meas[1:,0][emg1_start_idx:emg1_stop_idx] - emg1_meas[1:,0][emg1_start_idx]

emg0_in = scipy.signal.resample(emg0_in[0:,], len(angles_in), emg0_time)[0]
emg1_in = scipy.signal.resample(emg1_in[0:,], len(angles_in), emg1_time)[0]

imu0_meas = scipy.signal.resample(imu0_meas[imu_start:imu_stop], len(angles_in))
imu1_meas = scipy.signal.resample(imu1_meas[imu_start:imu_stop], len(angles_in))
