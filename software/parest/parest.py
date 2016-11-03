import serial
import collections
import threading
import scipy
from scipy import signal
import numpy as np
import time

SAMPLE_F_HZ = 10
SAMPLE_PERIOD_S = 1/SAMPLE_F_HZ

SER_PORT = "/dev/ttyMCC"
BAUD = 9600

MOTOR1_FILE = "motor1.log"
MOTOR2_FILE = "motor2.log"
START = str('b\'$\\r\\n\'')
MOTORIDINDEX = 3
MSGSTARTINDEX = 5

stop = False

def decodeMsg(msg):
    msgstr = str(msg)
    motorid = int(msgstr[MOTORIDINDEX])
    datastr = msgstr[MSGSTARTINDEX:msgstr.find('\\')]
    return (motorid, datastr)


def logging_thread(ser):
    print("Logging thread started")
    if ser.isOpen():
        print("Port is open!")
        while not stop:
            initmsg = ser.readline()
            print(str(initmsg))
            if str(initmsg) == START:
                msg = ser.readline()
                print(str(msg))
                motor, data = decodeMsg(msg)
                #print(data)
                if motor == 1:
                    motor1_file_h.write(data + "\n")
                elif motor == 2:
                    motor2_file_h.write(data + "\n")
        print("Logging stopped")
        ser.close()


def control_thread(ser, sig):
    global stop
    if ser.isOpen():
        for i in range(0, len(sig)):
            starttime = time.time()
            a = '1' + str(int(127*sig[i])).zfill(3) + '1' + str(int(127*sig[i])).zfill(3)
            out = str.encode(a)
            print(out)
            ser.write(out)
            time_to_sleep = starttime+SAMPLE_PERIOD_S - time.time()
            if time_to_sleep > 0:
                time.sleep(time_to_sleep)
        print("Ctrl stopped")
        stop = True

if __name__ == "__main__":
    ser = serial.Serial()
    ser.port = SER_PORT
    ser.baudrate = BAUD
    ser.open()

    motor1_file_h = open(MOTOR1_FILE, 'w');
    motor2_file_h = open(MOTOR2_FILE, 'w');

    motor1_file_h.write("time,angle,velocity,current\n")
    motor2_file_h.write("time,angle,velocity,current\n")
    t = np.linspace(0,20,100)
    sig = signal.square(1/10*np.pi*t, duty=0.5)
    sig = (sig+1)/2

    try:
        print("Starting threads")
        log = threading.Thread(target=logging_thread,args=(ser,))
        ctrl= threading.Thread(target=control_thread,args=(ser, sig))
        log.daemon=True
        ctrl.daemon=True
        log.start()
        ctrl.start()
        log.join()
        ctrl.join()
    except Exception as e:
        print(e)
        print("Error: Unable to start Thread")
