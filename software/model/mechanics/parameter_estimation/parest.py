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

ARM_UP = 1
ARM_DOWN = 0


def decodeMsg(msg):
    msgstr = str(msg)
    motorid = int(msgstr[MOTORIDINDEX])
    datastr = msgstr[MSGSTARTINDEX:msgstr.find('\\')]
    splittedData = datastr.split(',')
    dataints = (int(splittedData[0]), int(splittedData[1]), int(splittedData[2]), int(splittedData[3]))
    if motorid == 1:
        dataUnits = (dataints[0], convertToAngle(dataints[1]), convertToVel_Elbow(dataints[2]), convertToCurrent_Elbow(dataints[3]))
    elif motorid == 2:
        dataUnits = (dataints[0], convertToAngle(dataints[1]), convertToVel_Shoulder(dataints[2]), convertToCurrent_Shoulder(dataints[3]))
    return (motorid, dataUnits)

def convertToAngle(angNoUnit):
    angDeg = -0.296 * angNoUnit + 204
    return angDeg

def convertToCurrent_Elbow(curNoUnit):
    curA = 0.005865* (curNoUnit - 509) # 509 because FUCK LOGIC
    return curA

def convertToVel_Elbow(velNoUnit):
    velRpm = 5.865 * (velNoUnit-511.5)
    velRadS = velRpm * (2*np.pi/60)
    return velRadS

def convertToCurrent_Shoulder(curNoUnit):
    curA = 0.014663 * (curNoUnit - 511.5)
    return curA

def convertToVel_Shoulder(velNoUnit):
    velRpm = 5.865 * (velNoUnit) - 3000
    velRadS = velRpm * 6 * (2*np.pi/360)
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