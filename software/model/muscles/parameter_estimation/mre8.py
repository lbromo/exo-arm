import numpy as np
import scipy.signal

import os
import pwd
user = pwd.getpwuid( os.getuid() )[0]

kinkom=np.genfromtxt(
    "/afs/ies.auc.dk/group/17gr1035/Private/logs/kincom_logs/morten/MRE8_clean",
    delimiter=',')

angle = abs(kinkom[:,1])
force = kinkom[:,-1]

emg1_meas = np.genfromtxt(
    "/afs/ies.auc.dk/group/17gr1035/Private/logs/emg_logs/mr_morten/parsed/MRE8_emg0.log",
    delimiter=',')

emg0_meas = np.genfromtxt(
    "/afs/ies.auc.dk/group/17gr1035/Private/logs/emg_logs/mr_morten/parsed/MRE8_emg1.log",
    delimiter=',')

imu1_meas = np.genfromtxt(
    "/afs/ies.auc.dk/group/17gr1035/Private/logs/emg_logs/mr_morten/parsed/MRE8_imu0.log",
    delimiter=',')

imu0_meas = np.genfromtxt("/afs/ies.auc.dk/group/17gr1035/Private/logs/emg_logs/mr_morten/parsed/MRE8_imu1.log",
    delimiter=',')

tmp = np.array([imu1_meas[1:,1][i] - imu1_meas[1:,1][i-1] for i in range(1, len(imu1_meas[1:,1]))])
dA = np.array([angle[i] - angle[i-1] for i in range(1, len(angle))])

imu_start = np.where( tmp > 0.1 )[0][2] - 12
imu_stop = np.where( tmp > 0.05 )[0][-1]

t_start = imu1_meas[1:,0][imu_start]
t_stop  = imu1_meas[1:,0][imu_stop]

angle_start = np.where( abs(dA) >= 0.4 )[0][0]
angle = angle[angle_start:]

emg0_start_idx = np.where(emg0_meas[1:,0] >= imu1_meas[1:,0][imu_start])[0][0]
emg0_stop_idx  = np.where(emg0_meas[1:,0] >= imu1_meas[1:,0][imu_stop])[0][0]

emg1_start_idx = np.where(emg1_meas[1:,0] >= imu1_meas[1:,0][imu_start])[0][0]
emg1_stop_idx  = np.where(emg1_meas[1:,0] >= imu1_meas[1:,0][imu_stop])[0][0]

## Setup
angles_in = angle
emg0_training = emg0_meas[1:,1:][0:emg0_start_idx]
emg0_in = emg0_meas[1:,1:][emg0_start_idx:emg0_stop_idx]
emg1_training = emg1_meas[1:,1:][0:emg1_start_idx]
emg1_in = emg0_meas[1:,1:][emg1_start_idx:emg1_stop_idx]
torque_out = -force[angle_start:] * 0.2

## Resample
emg0_in = scipy.signal.resample(emg0_in, len(angles_in))
emg1_in = scipy.signal.resample(emg1_in, len(angles_in))
