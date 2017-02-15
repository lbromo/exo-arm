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

ELBOW = 1
SHOULDER = 2

PULSE_PERIOD_ELBOW_S =10
PULSE_PERIOD_SHOULDER_S = 4

T_END_S = 0.1
NAME = "col_0.5"
#AMPS = np.linspace(10,100,10)
AMPS = np.array([0.5])

SEQ_LEN = T_END_S * pe.SAMPLE_F_HZ

SER_PORT = "/dev/ttyMCC"
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


def makeSine(frq, amp, t_end):
    # Signal Vectors
    seq_len = int(t_end * pe.SAMPLE_F_HZ)
    t = np.linspace(0,t_end,seq_len)

    sig_motor = amp * np.sin(frq* 2*np.pi*t)

    sig_motor, dir_v = pe.parseSignal(sig_motor)
    # Clamp signals to range
    for i in range(0,seq_len):
        sig_motor[i] = pe.clamp(np.abs(sig_motor[i]),pe.PWM_MIN,pe.PWM_MAX)    
        dir_v[i] = pe.clamp(dir_v[i], pe.ARM_DOWN,pe.ARM_UP)
    return (t, sig_motor, dir_v)

def randStep(max_frq, amp, t_end):
    seq_len = int(t_end * pe.SAMPLE_F_HZ)
    t = np.linspace(0,t_end,seq_len)
    max_per = 1/max_frq
    sig = []
    while len(sig) < seq_len:
        T = max_per*scipy.rand()
        frq = 1/T
        tnow = np.linspace(0,T,np.floor(T/pe.SAMPLE_PERIOD_S))
        sig.append(amp * np.sign(np.sin(2 * np.pi * frq * tnow)))
    sig = pe.flat(sig)
    sig_motor = sig[:len(t)]        
    sig_motor, dir_v = pe.parseSignal(sig_motor)
    for i in range(0,seq_len):
        sig_motor[i] = pe.clamp(np.abs(sig_motor[i]),pe.PWM_MIN,pe.PWM_MAX)    
        dir_v[i] = pe.clamp(dir_v[i], pe.ARM_DOWN,pe.ARM_UP)
    return (t, sig_motor, dir_v)

def sineSweep(min_frq, max_frq, amp, t_end):
    seq_len = int(t_end * pe.SAMPLE_F_HZ)
    t = np.linspace(0,t_end,seq_len)

    f = np.array(np.linspace(min_frq, max_frq, seq_len))

    sig_motor = amp * np.sin(2*np.pi*f*np.array(t))
    sig_motor = sig_motor[::-1]

    sig_motor, dir_v = pe.parseSignal(sig_motor)

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
    
    print(NAME)
    time.sleep(2)

    ser.write(b'$00' + pe.intTo3Bytes(pe.PWM_MIN) + b'00' + pe.intTo3Bytes(pe.PWM_MIN))

#    amps = np.linspace(20,30,11);
    amps = pe.cur_pwm(AMPS,ELBOW)
    TEST_LEN = len(amps)

    # Main loop!
    try:
        for idx in range(0,TEST_LEN):
            name = NAME#+ str(int(amps[idx]))
        # File initialization

            INPUT_FILE = "./logs/input_" + name + ".log"
            MOTOR1_FILE = "./logs/motor1_" + name + ".log"
            MOTOR2_FILE = "./logs/motor2_" + name + ".log"

            motor1_file_h = open((MOTOR1_FILE), 'w')
            motor2_file_h = open((MOTOR2_FILE), 'w')
            input_file_h = open((INPUT_FILE), 'w')

            motor1_file_h.write("time,angle,velocity,current\n")
            motor2_file_h.write("time,angle,velocity,current\n")
            input_file_h.write("on1,dir1,pwm1,on2,dir2,pwm2\n")

            t, sig_motor1, dir1 = randStep(1/pe.ELBOW_PULSE_PERIOD_MAX_S, amps[idx], T_END_S)
            #t, sig_motor1, dir1 = sineSweep(1/pe.ELBOW_PULSE_PERIOD_MAX_S, 5, amps[idx], T_END_S)
            sig_motor2  = np.ones(SEQ_LEN)
            dir2 = np.ones(SEQ_LEN)
            on1 = 1
            on2 = 0
            print(amps[idx])

            print('Starting loop')

            if ser.isOpen():
                for i in range(0, int(SEQ_LEN-1)):
                    starttime = time.time()
                    #sig_motor1[i] = 25
                    out = pe.parseMsg(on1, dir1[i], sig_motor1[i], on2, dir2[i], sig_motor2[i])
                    print(out)
                    # Writing on serial
                    print(ser.write(out))

                    # Logging
                    input_file_h.write(str(on1) + ',' + str(dir1[i]) + ',' + str(round(sig_motor1[i])).zfill(3) + ',' + str(on2) + ',' + str(int(dir2[i])) + ',' + str(round(sig_motor2[i])).zfill(3) + '\n')
    #                print("Ctrl:" + str(out))
                    pe.log1msg(ser,motor1_file_h,motor2_file_h)
                    pe.log1msg(ser,motor1_file_h,motor2_file_h)

                    # Wait for next sample period
                    time_to_sleep = starttime+pe.SAMPLE_PERIOD_S-time.time()
    #                print(time_to_sleep)
                    # Only wait if we made it in time 
                    if time_to_sleep > 0:
                        time.sleep(time_to_sleep)
                    else:
                        print("Missed it")
        ser.write(b'$00' + pe.intTo3Bytes(pe.PWM_MIN) + b'00' + pe.intTo3Bytes(pe.PWM_MIN))
        print('done')
    except:
        out = pe.parseMsg(0, 0, pe.PWM_MIN, 0, 0, pe.PWM_MIN)
        ser.write(out)
        print(sys.exc_info()[0])
        exit()
    # p.join()
