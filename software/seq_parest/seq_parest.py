import serial
import scipy
from scipy import signal
import numpy as np
import time
import sys

PULSE_PERIOD_S = 5
T_END_S = 10
SAMPLE_F_HZ = 100
SAMPLE_PERIOD_S = 1/SAMPLE_F_HZ

SER_PORT = sys.argv[1]
BAUD = 115200

INPUT_FILE = "input.log"
MOTOR1_FILE = "motor1.log"
MOTOR2_FILE = "motor2.log"
START = str('b\'$\\r\\n\'')
MOTORIDINDEX = 3
MSGSTARTINDEX = 5

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

if __name__ == "__main__":
    ser = serial.Serial(timeout=0.5)
    ser.port = SER_PORT
    ser.baudrate = BAUD
    ser.open()

    motor1_file_h = open(MOTOR1_FILE, 'w')
    motor2_file_h = open(MOTOR2_FILE, 'w')
    input_file_h = open(INPUT_FILE, 'w')

    motor1_file_h.write("time,angle,velocity,current \n")
    motor2_file_h.write("time,angle,velocity,current\n")
    input_file_h.write("on1,dir1,pwm1,on2,dir2,pwm2\n")
    t = np.linspace(0,T_END_S,T_END_S*SAMPLE_F_HZ)
    
    sig_motor1 = signal.square(1/PULSE_PERIOD_S*2*np.pi*t, duty=0.5)
    sig_motor2 = np.zeros(len(t))

    for i in range(0,len(t)):
        sig_motor1[i] = clamp(sig_motor1[i],0,255)
        sig_motor2[i] = clamp(sig_motor2[i],0,255)

    on1 = 1
    dir1 = 1
    on2 = 1
    dir2 = 1

    try:
        if ser.isOpen():
            for i in range(0, len(t)):
                starttime = time.time()
                
                # Parsing
                a = '$' + str(on1) + str(dir1) + str(int(sig_motor1[i])).zfill(3) + str(on2) + str(dir2) + str(int(sig_motor2[i])).zfill(3)
                out = str.encode(a)
                ser.write(out)

                input_file_h.write(str(on1) + ',' + str(dir1) + ',' + str(int(sig_motor1[i])).zfill(3) + ',' + str(on2) + ',' + str(dir2) + ',' + str(int(sig_motor2[i])).zfill(3) + '\n')
                print("Ctrl:" + str(out))
                log1msg(ser)
                log1msg(ser)

                time_to_sleep = starttime+SAMPLE_PERIOD_S-time.time()
                print(time_to_sleep)
                if time_to_sleep > 0:
                    time.sleep(time_to_sleep)

    except Exception as e:
        print(e)
        print("Error: Unable to start Thread")
