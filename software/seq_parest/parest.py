import serial
import scipy
from scipy import signal
import numpy as np
import time
import sys

import tempfile

# For plotting
import matplotlib.pyplot as plt

START = str('b\'$\\r\\n\'')
MOTORIDINDEX = 3
MSGSTARTINDEX = 5

SAMPLE_F_HZ = 100

SAMPLE_PERIOD_S = 1/SAMPLE_F_HZ
PWM_MAX = 230
PWM_MIN = 25

ELBOW_PULSE_PERIOD_MAX_S = 1
SHOULDER_PULSE_PERIOD_MAX_S = 1

ARM_UP = 1
ARM_DOWN = 0


def cur_pwm(cur,motorid):
    if motorid == 1:
        max_cur=1
    elif motorid == 2:
        max_cur=3
    slope=(PWM_MAX-PWM_MIN)/max_cur
    pwm=cur*slope
    return pwm

def decodeMsg(msg):
    msgstr = str(msg)
    motorid = int(msgstr[MOTORIDINDEX])
    datastr = msgstr[MSGSTARTINDEX:msgstr.find('\\')]
    splittedData = datastr.split(',')
    dataints = (int(splittedData[0]), int(splittedData[1]), int(splittedData[2]), int(splittedData[3]))
    if motorid == 1:
        dataUnits = (dataints[0], convertToAngle_Elbow(dataints[1]), convertToVel_Elbow(dataints[2]), convertToCurrent_Elbow(dataints[3]))
    elif motorid == 2:
        dataUnits = (dataints[0], convertToAngle_Shoulder(dataints[1]), convertToVel_Shoulder(dataints[2]), convertToCurrent_Shoulder(dataints[3]))
    return (motorid, dataUnits)

def convertToAngle_Elbow(angNoUnit):
    angRad = ( 474.3750 - angNoUnit) * 2 * np.pi / 793.2692;
    return angDeg

def convertToAngle_Shoulder(angNoUnit):
    angRad = ( 415.0385 - angNoUnit) * 2 * np.pi / 784.3846;
    return angDeg


def convertToCurrent_Elbow(curNoUnit):
    curA = 0.005865* (curNoUnit - 509) # 509 because FUCK LOGIC
    return curA

def convertToVel_Elbow(velNoUnit):
    velRpm = 5.865 * (velNoUnit-511.5)
    velRadS = velRpm * (2*np.pi/60)
    return velRadS

def convertToCurrent_Shoulder(curNoUnit):
    curA = 0.005865 * (curNoUnit - 511.5)
    return curA

def convertToVel_Shoulder(velNoUnit):
    velRpm = 5.865 * (velNoUnit) - 3000
    velRadS = velRpm * (2*np.pi/60)
    return velRadS

def log1msg(ser, motor1_file_h, motor2_file_h):
    if ser.isOpen():
        starttime = time.time()
        initmsg = ser.readline()

        if str(initmsg) == START:
            msg = ser.readline()
            motor, data_w_units = decodeMsg(msg)
            #print("Received msg: " + str(data_w_units))
            if motor == 1:
                motor1_file_h.write(','.join([str(x) for x in data_w_units]) + "\n")
            elif motor == 2:
                motor2_file_h.write(','.join([str(x) for x in data_w_units]) + "\n")

def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)

def intTo3Bytes(intvar):
    return str.encode(str(intvar).zfill(3))

def parseMsg(on1, dir1, pwm1, on2, dir2, pwm2):
    return str.encode('$' + str(on1) + str(int(dir1)) + str(int(pwm1)).zfill(3) + str(on2) + str(int(dir2)) + str(int(pwm2)).zfill(3))

def parseSignal(inputsignal):
    dirsig = np.sign(inputsignal)
    inputsignal = np.abs(inputsignal) + PWM_MIN
    return (inputsignal, dirsig)

def flat(sig):
    return [item for sublist in sig for item in sublist]