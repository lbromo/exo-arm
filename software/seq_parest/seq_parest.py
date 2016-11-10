import serial
import scipy
from scipy import signal
import numpy as np
import time
import sys

import tempfile
import itertools as IT
import os

PULSE_PERIOD_S = 2
T_END_S = 1
SAMPLE_F_HZ = 100
SAMPLE_PERIOD_S = 1/SAMPLE_F_HZ
SEQ_LEN = T_END_S * SAMPLE_F_HZ

SER_PORT = sys.argv[1]
BAUD = 115200

PWM_MAX = 230
PWM_MIN = 10

ARM_UP = 1
ARM_DOWN = 0

INPUT_FILE = "./logs/input_.log"
MOTOR1_FILE = "./logs/motor1_.log"
MOTOR2_FILE = "./logs/motor2_.log"
START = str('b\'$\\r\\n\'')
MOTORIDINDEX = 3
MSGSTARTINDEX = 5

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


def log1msg(ser):
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

def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)

def intTo3Bytes(intvar):
    return str.encode(str(intvar).zfill(3))

def parseMsg(on1, dir1, pwm1, on2, dir2, pwm2):
    return str.encode('$' + str(on1) + str(int(dir1)) + str(int(pwm1)).zfill(3) + str(on2) + str(int(dir2)) + str(int(pwm2)).zfill(3))

if __name__ == "__main__":
# Serial stuff
    ser = serial.Serial(SER_PORT, BAUD, timeout=0.5)
    if not ser.isOpen():
        ser.open()
    
    ser.write(b'$000' + intTo3Bytes(PWM_MIN) + b'00' + intTo3Bytes(PWM_MIN))

# File initialization
    motor1_file_h = open(uniquify(MOTOR1_FILE), 'w')
    motor2_file_h = open(uniquify(MOTOR2_FILE), 'w')
    input_file_h = open(uniquify(INPUT_FILE), 'w')

    motor1_file_h.write("time,angle,velocity,current \n")
    motor2_file_h.write("time,angle,velocity,current\n")
    input_file_h.write("on1,dir1,pwm1,on2,dir2,pwm2\n")

# Signal Vectors
    t = np.linspace(0,T_END_S,SEQ_LEN)

    sig_motor1 = 30 * np.ones(SEQ_LEN)
    sig_motor2 = 30 * np.ones(SEQ_LEN)#signal.square(1/PULSE_PERIOD_S*2*np.pi*t, duty=0.5)

    on1 = 0
    dir2 = signal.square(1/PULSE_PERIOD_S*2*np.pi*t, duty=0.5)
    on2 = 0
    dir1 = signal.square(1/PULSE_PERIOD_S*2*np.pi*t, duty=0.5)


# Clamp signals to range
    for i in range(0,SEQ_LEN):
        sig_motor1[i] = clamp(sig_motor1[i],PWM_MIN,PWM_MAX)
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
                print("Ctrl:" + str(out))
                
                log1msg(ser)
                log1msg(ser)

                # Wait for next sample period
                time_to_sleep = starttime+SAMPLE_PERIOD_S-time.time()
                print(time_to_sleep)
                # Only wait if we made it in time 
                if time_to_sleep > 0:
                    time.sleep(time_to_sleep)
            # Make sure that arm stops a rest after the run
        ser.write(b'$000' + intTo3Bytes(PWM_MIN) + b'00' + intTo3Bytes(PWM_MIN))

    except Exception as e:
        print(e)
