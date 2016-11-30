import parest as pe
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

PULSE_PERIOD_ELBOW_S = 20
PULSE_PERIOD_SHOULDER_S = 4

T_END_S = 120

SEQ_LEN = T_END_S * pe.SAMPLE_F_HZ

SER_PORT = "/dev/ttyACM0"
BAUD = 115200

def makeStep(frq, amp, t_end):
        # Signal Vectors
    seq_len = int(t_end * pe.SAMPLE_F_HZ)
    t = np.linspace(0,t_end,seq_len)

    sig_motor = amp * np.sign(np.sin(frq* 2*np.pi*t))

    sig_motor, dir_v = pe.parseSignal(sig_motor)
    # Clamp signals to range
    for i in range(0,seq_len):
        sig_motor[i] = pe.clamp(np.abs(sig_motor[i]),pe.PWM_MIN,pe.PWM_MAX)    
        dir_v[i] = pe.clamp(dir_v[i], pe.ARM_DOWN,pe.ARM_UP)
    return (t, sig_motor, dir_v)

if __name__ == "__main__":
 #   q = Queue()
 #   p = Process(target=pPlot, args=(q,))
 #   p.start()

    # Serial stuff
    ser = serial.Serial(SER_PORT, BAUD, timeout=0.5)
    if not ser.isOpen():
        ser.open()
    
    ser.write(b'$00' + pe.intTo3Bytes(pe.PWM_MIN) + b'00' + pe.intTo3Bytes(pe.PWM_MIN))

    amps = np.linspace(2,9,8);
    TEST_LEN = len(amps);

    # Main loop!
    for idx in range(0,TEST_LEN):
        name = 'step_test_2_' + str(int(amps[idx]))

    # File initialization

        INPUT_FILE = "./logs/input_" + name + ".log"
        MOTOR1_FILE = "./logs/motor1_" + name + ".log"
        MOTOR2_FILE = "./logs/motor2_" + name + ".log"

        motor1_file_h = open((MOTOR1_FILE), 'w')
        motor2_file_h = open((MOTOR2_FILE), 'w')
        input_file_h = open((INPUT_FILE), 'w')

        motor1_file_h.write("time,angle,velocity,current \n")
        motor2_file_h.write("time,angle,velocity,current\n")
        input_file_h.write("on1,dir1,pwm1,on2,dir2,pwm2\n")

        t, sig_motor1, dir1 = makeStep(1/PULSE_PERIOD_ELBOW_S, amps[idx], T_END_S)
        sig_motor2  = np.ones(SEQ_LEN)
        dir2 = np.ones(SEQ_LEN)
        on1 = 1
        on2 = 0


        print('Starting loop')

        try:
            if ser.isOpen():
                for i in range(0, SEQ_LEN-1):
                    starttime = time.time()
                    
                    out = pe.parseMsg(on1, dir1[i], sig_motor1[i], on2, dir2[i], sig_motor2[i])

                    # Writing on serial
                    ser.write(out)

                    # Logging
                    input_file_h.write(str(on1) + ',' + str(dir1[i]) + ',' + str(int(sig_motor1[i])).zfill(3) + ',' + str(on2) + ',' + str(int(dir2[i])) + ',' + str(int(sig_motor2[i])).zfill(3) + '\n')
    #                print("Ctrl:" + str(out))
                    pe.log1msg(ser,motor1_file_h,motor2_file_h)
                    pe.log1msg(ser,motor1_file_h,motor2_file_h)

                    # Wait for next sample period
                    time_to_sleep = starttime+pe.SAMPLE_PERIOD_S-time.time()
    #                print(time_to_sleep)
                    # Only wait if we made it in time 
                    if time_to_sleep > 0:
                        time.sleep(time_to_sleep)
                # Make sure that arm stops a rest after the run
            

        except Exception as e:
            raise e
    ser.write(b'$00' + pe.intTo3Bytes(pe.PWM_MIN) + b'00' + pe.intTo3Bytes(pe.PWM_MIN))
    print('done')
    # p.join()
