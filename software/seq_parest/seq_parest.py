import serial
import scipy
from scipy import signal
import numpy as np
import time
import sys

import tempfile
import itertools as IT
import os

# For plotting
from multiprocessing import Process, Queue
import matplotlib.pyplot as plt
import collections

PULSE_PERIOD_ELBOW_S = 5
PULSE_PERIOD_SHOULDER_S = 4

T_END_S = 100
SAMPLE_F_HZ = 100

TEST_PWM_ELBOW = 200
TEST_PWM_SHOULDER = 120

SAMPLE_PERIOD_S = 1/SAMPLE_F_HZ
SEQ_LEN = T_END_S * SAMPLE_F_HZ

SER_PORT = sys.argv[1]
BAUD = 115200

PWM_MAX = 230
PWM_MIN = 25

ARM_UP = 1
ARM_DOWN = 0

INPUT_FILE = "./logs/input_" + sys.argv[2] + ".log"
MOTOR1_FILE = "./logs/motor1_" + sys.argv[2] + ".log"
MOTOR2_FILE = "./logs/motor2_" + sys.argv[2] + ".log"
START = str('b\'$\\r\\n\'')
MOTORIDINDEX = 3
MSGSTARTINDEX = 5



# "time,angle,velocity,current\n"
def pPlot(input_queue):
    values = {
        1: {
            'time': collections.deque(np.zeros(1000), maxlen=1000),
            'angle': collections.deque(np.zeros(1000), maxlen=1000),
            'velocity': collections.deque(np.zeros(1000), maxlen=1000),
            'current': collections.deque(np.zeros(1000), maxlen=1000)
        },
        2: {
            'time': collections.deque(np.zeros(1000), maxlen=1000),
            'angle': collections.deque(np.zeros(1000), maxlen=1000),
            'velocity': collections.deque(np.zeros(1000), maxlen=1000),
            'current': collections.deque(np.zeros(1000), maxlen=1000)
        }
    }

#    plt.ion()
    #plt.subplot(2, 3, 1)
#    m1_plot1, = plt.plot(np.zeros(1000), np.ones(1000))
#    print(m1_plot1)
    # plt.subplot(2, 3, 1)
    # m1_plot2 = plt.plot(np.zeros(1000),np.zeros(1000))
    # plt.subplot(2, 3, 2)
    # m1_plot1 = plt.plot(np.zeros(1000),np.zeros(1000))
    # plt.subplot(2, 3, 3)
    # m1_plot3 = plt.plot(np.zeros(1000),np.zeros(1000))
    # plt.subplot(2, 3, 4)
    # m1_plot4 = plt.plot(np.zeros(1000),np.zeros(1000))
    # plt.subplot(2, 3, 5)
    # m1_plot5 = plt.plot(np.zeros(1000),np.zeros(1000))

    t = 0

    while True:
        motorid, datastr = input_queue.get()
        time, angle, vel, current = datastr.split(',')

        # load in new data
        values[motorid]['time'].append(time)
        values[motorid]['angle'].append(time)
        values[motorid]['velocity'].append(vel)
        values[motorid]['current'].append(current)

        # if t % 100 == 0:
 #           print(t)
 #           m1_plot1.set_xdata(values[1]['time'])
 #           m1_plot1.set_ydata(values[1]['angle'])
 #           plt.show()
        t = t+1


def uniquify(path, sep = ''):
    def name_sequence():
        count = IT.count()
        yield ''
        while True:
            yield '{s}{n:d}'.format(s = sep, n = next(count))
    orig = tempfile._name_sequence
    with tempfile._once_lock:
        tempfile._name_sequence = name_sequence()
        path = os.path.normpath(path)
        dirname, basename = os.path.split(path)
        filename, ext = os.path.splitext(basename)
        fd, filename = tempfile.mkstemp(dir = dirname, prefix = filename, suffix = ext)
        tempfile._name_sequence = orig
    return filename

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
    curA = 0.005865* (curNoUnit-511.5) 
    return curA

def convertToVel_Elbow(velNoUnit):
    velRpm = 1.955034 * (velNoUnit-511.5)
    velDegS = velRpm * 6
    return velDegS

def convertToCurrent_Shoulder(curNoUnit):
    curA = 0.014663 * (curNoUnit - 511.5)
    return curA

def convertToVel_Shoulder(velNoUnit):
    velRpm = 1.955034 * (velNoUnit-511.5)
    velDegS = velRpm * 6
    return velDegS


def log1msg(ser):
    if ser.isOpen():
        starttime = time.time()
        initmsg = ser.readline()

        if str(initmsg) == START:
            msg = ser.readline()
            motor, data_w_units = decodeMsg(msg)
            print("Received msg: " + str(data_w_units))
            if motor == 1:
                motor1_file_h.write(','.join([str(x) for x in data_w_units]) + "\n")
            elif motor == 2:
                motor2_file_h.write(','.join([str(x) for x in data_w_units]) + "\n")

            #q.put((motor, data))

def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)

def intTo3Bytes(intvar):
    return str.encode(str(intvar).zfill(3))

def parseMsg(on1, dir1, pwm1, on2, dir2, pwm2):
    return str.encode('$' + str(on1) + str(int(dir1)) + str(int(pwm1)).zfill(3) + str(on2) + str(int(dir2)) + str(int(pwm2)).zfill(3))

def parseSignal(inputsignal):
    dirsig = np.sign(inputsignal)
    inputsignal = np.abs(inputsignal)
    return (inputsignal, dirsig)

if __name__ == "__main__":
 #   q = Queue()
 #   p = Process(target=pPlot, args=(q,))
 #   p.start()

    # Serial stuff
    ser = serial.Serial(SER_PORT, BAUD, timeout=0.5)
    if not ser.isOpen():
        ser.open()
    
    ser.write(b'$00' + intTo3Bytes(PWM_MIN) + b'00' + intTo3Bytes(PWM_MIN))

# File initialization
    motor1_file_h = open((MOTOR1_FILE), 'w')
    motor2_file_h = open((MOTOR2_FILE), 'w')
    input_file_h = open((INPUT_FILE), 'w')

    motor1_file_h.write("time,angle,velocity,current \n")
    motor2_file_h.write("time,angle,velocity,current\n")
    input_file_h.write("on1,dir1,pwm1,on2,dir2,pwm2\n")

# Signal Vectors
    t = np.linspace(0,T_END_S,SEQ_LEN)

#    sig_motor1 = TEST_PWM_ELBOW * np.ones(SEQ_LEN) # signal.square(1/PULSE_PERIOD_S*2*np.pi*t, duty=0.5)
    sig_motor2 = TEST_PWM_SHOULDER * np.ones(SEQ_LEN)

    sig_motor1 = TEST_PWM_ELBOW * np.sin(1/PULSE_PERIOD_ELBOW * 2*np.pi*t)
    #sig_motor1 = TEST_PWM_ELBOW * np.ones(SEQ_LEN)
    # sig_motor1 = PWM_MAX * np.linspace(-1,1,SEQ_LEN)


    sig_motor1, dir1 = parseSignal(sig_motor1)
    sig_motor2, dir2 = parseSignal(sig_motor2)
    sig_motor1 = sig_motor1 + PWM_MIN

    on1 = 1
    on2 = 1


# Clamp signals to range
    for i in range(0,SEQ_LEN):
        sig_motor1[i] = clamp(np.abs(sig_motor1[i]),PWM_MIN,PWM_MAX)
        sig_motor2[i] = clamp(sig_motor2[i],PWM_MIN,PWM_MAX)
        dir1[i] = clamp(dir1[i], ARM_DOWN,ARM_UP)
        dir2[i] = clamp(dir2[i], ARM_DOWN,ARM_UP)

    print('Starting loop')

    try:
        if ser.isOpen():
            for i in range(0, SEQ_LEN-1):
                starttime = time.time()
                
                out = parseMsg(on1, dir1[i], sig_motor1[i], on2, dir2[i], sig_motor2[i])

                # Writing on serial
                ser.write(out)

                # Logging
                input_file_h.write(str(on1) + ',' + str(dir1[i]) + ',' + str(int(sig_motor1[i])).zfill(3) + ',' + str(on2) + ',' + str(int(dir2[i])) + ',' + str(int(sig_motor2[i])).zfill(3) + '\n')
#                print("Ctrl:" + str(out))
                log1msg(ser)
                log1msg(ser)

                # Wait for next sample period
                time_to_sleep = starttime+SAMPLE_PERIOD_S-time.time()
#                print(time_to_sleep)
                # Only wait if we made it in time 
                if time_to_sleep > 0:
                    time.sleep(time_to_sleep)
            # Make sure that arm stops a rest after the run
        ser.write(b'$00' + intTo3Bytes(PWM_MIN) + b'00' + intTo3Bytes(PWM_MIN))

    except Exception as e:
        raise e

    print('done')
    # p.join()
