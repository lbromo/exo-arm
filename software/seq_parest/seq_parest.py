import serial
import scipy
from scipy import signal
import numpy as np
import time
import sys

SAMPLE_F_HZ = 100
SAMPLE_PERIOD_S = 1/SAMPLE_F_HZ

SER_PORT = sys.argv[1]
BAUD = 9600

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


def logging_thread(ser):
    if ser.isOpen():
        starttime = time.time()
        initmsg = ser.readline()
        print(str(initmsg))
        if str(initmsg) == START:
            msg = ser.readline()
            motor, data = decodeMsg(msg)
            if motor == 1:
                motor1_file_h.write(data + "\n")
            elif motor == 2:
                motor2_file_h.write(data + "\n")
            print("Logged..")

if __name__ == "__main__":
    ser = serial.Serial(timeout=0.5)
    ser.port = SER_PORT
    ser.baudrate = BAUD
    ser.open()

    motor1_file_h = open(MOTOR1_FILE, 'w');
    motor2_file_h = open(MOTOR2_FILE, 'w');

    motor1_file_h.write("time,angle,velocity,current \n")
    motor2_file_h.write("time,angle,velocity,current\n")
    t = np.linspace(0,20,100)
    sig = signal.square(2*np.pi*t, duty=0.5)
    sig = (sig+1)/2

    try:
        if ser.isOpen():
            for i in range(0, len(sig)):
                starttime = time.time()
                a = '$' + '1' + str(int(255*sig[i])).zfill(3) + '1' + str(int(255*sig[i])).zfill(3)
                out = str.encode(a)
                # print(out)
                ser.write(out)
                print("Controlled..")
                logging_thread(ser);

    except Exception as e:
        print(e)
        print("Error: Unable to start Thread")
