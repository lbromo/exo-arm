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

PULSE_PERIOD_S = 1
T_END_S = 10
SAMPLE_F_HZ = 100
SAMPLE_PERIOD_S = 1/SAMPLE_F_HZ

SER_PORT = sys.argv[1]
BAUD = 115200

ts = str(time.time())

INPUT_FILE = "input.log"
MOTOR1_FILE = "motor1.log"
MOTOR2_FILE = "motor2.log"
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

    plt.ion()
    #plt.subplot(2, 3, 1)
    m1_plot1, = plt.plot(np.zeros(1000), np.ones(1000))
    print(m1_plot1)
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

        if t % 100 == 0:
            print(t)
            m1_plot1.set_xdata(values[1]['time'])
            m1_plot1.set_ydata(values[1]['angle'])
            plt.show()
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
    return (motorid, datastr)


def log1msg(ser, q):
    if ser.isOpen():
        starttime = time.time()
        initmsg = ser.readline()

        if str(initmsg) == START:
            msg = ser.readline()
            motor, data = decodeMsg(msg)
            print("Received msg: " + str(data))
            if motor == 1:
                motor1_file_h.write(data + "\n")
            elif motor == 2:
                motor2_file_h.write(data + "\n")

            q.put((motor, data))

def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)

if __name__ == "__main__":
    q = Queue()
    p = Process(target=pPlot, args=(q,))
    p.start()

    ser = serial.Serial(timeout=0.5)
    ser.port = SER_PORT
    ser.baudrate = BAUD
    ser.open()

    motor1_file_h = open(uniquify(MOTOR1_FILE), 'w')
    motor2_file_h = open(uniquify(MOTOR2_FILE), 'w')
    input_file_h = open(uniquify(INPUT_FILE), 'w')

    motor1_file_h.write("time,angle,velocity,current \n")
    motor2_file_h.write("time,angle,velocity,current\n")
    input_file_h.write("on1,dir1,pwm1,on2,dir2,pwm2\n")
    t = np.linspace(0,T_END_S,T_END_S*SAMPLE_F_HZ)

    sig_motor1 = 30 * signal.square(1/PULSE_PERIOD_S*2*np.pi*t, duty=0.5)
    sig_motor2 = np.zeros(len(t))

    on1 = 1
    dir1 = signal.square(1/PULSE_PERIOD_S*2*np.pi*t, duty=0.5)
    on2 = 1
    dir2 = 1

    for i in range(0,len(t)):
        sig_motor1[i] = clamp(sig_motor1[i],30,230)
        sig_motor2[i] = clamp(sig_motor2[i],30,230)
        dir1[i] = clamp(dir1[i], 0,1);




    try:
        if ser.isOpen():
            for i in range(0, len(t)-1):
                starttime = time.time()

                # Parsing
                a = '$' + str(on1) + str(int(dir1[i])) + str(int(sig_motor1[i])).zfill(3) + str(on2) + str(dir2) + str(int(sig_motor2[i])).zfill(3)
                out = str.encode(a)
                ser.write(out)

                input_file_h.write(str(on1) + ',' + str(dir1[i]) + ',' + str(int(sig_motor1[i])).zfill(3) + ',' + str(on2) + ',' + str(dir2) + ',' + str(int(sig_motor2[i])).zfill(3) + '\n')
                print("Ctrl:" + str(out))
                log1msg(ser, q)
                log1msg(ser, q)

                time_to_sleep = starttime+SAMPLE_PERIOD_S-time.time()
                print(time_to_sleep)
                if time_to_sleep > 0:
                    time.sleep(time_to_sleep)
            ser.write(b'$0001000010')

    except Exception as e:
        print(e)
        print("Error: Unable to start Thread")

    print('done')
    p.join()
