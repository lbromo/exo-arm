import threading
import time
import serial
import numpy as np

BAUD = 230400

READY = b'M'
START_CHAR = '$'
START = str('b\'$\\r\\n\'')
REF_CHAR = b'R'
END_CHAR = b'E'

SER_LOCK = threading.Lock()

def log1msg(ser, logfile):
    if ser.isOpen():
        initmsg = ser.readline()
        if not len(initmsg):
            return

        # print(initmsg)
        initmsg = initmsg.decode()

        if initmsg[0] == START_CHAR:
            msg = initmsg[2:]
            # print(msg)
            data_w_units = msg.strip().split(',')
            # NICE PRINTING FUNCTION
            # print(','.join(str(x) for x in data_w_units))
            logfile.write(','.join(str(x) for x in data_w_units) + '\n')

def tUpdateRef(ser):
    while True:
        try:
            ref_shoulder, ref_elbow = [int(var) for var in raw_input("Enter new reference: ").split()]
        except:
            print("Error getting new ref. Please input as <shoulder_ref elbow_ref>")
        else:
            ref = np.array([
                np.radians(ref_shoulder),
                np.radians(ref_elbow),
                0,
                0
            ])
            with SER_LOCK:
                if ser.isOpen():
                    print('Going to: ('+ str(ref[0]) +',', str(ref[1]) + ')')
                    ref_msg = REF_CHAR + (intTo3Bytes(int(ref[0]*100))) + b',' + (intTo3Bytes(int(ref[1]*100))) + b',' + (intTo3Bytes(int(ref[2]*100))) + b',' + (intTo3Bytes(int(ref[3]*100))) + b',' + END_CHAR
                    ser.write(ref_msg)

def tLogger(ser, f):
    with SER_LOCK:
        ser.write(READY)
    log1msg(ser,f)
    threading.Timer(0.01, tLogger, (ser, f)).start()



def manual_input_mode(ser, logfile):
    t = threading.Thread(target=tUpdateRef, args=(ser,))
    t.daemon = True
    t.start()

    f = open(logfile, 'w')

    while True:
        try:
            with SER_LOCK:
                ser.write(READY)
                log1msg(ser, f)
        except:
            time.sleep(0.01)
            ser.write(b'S')
            time.sleep(0.01)
            f.close()
            exit()
        else:
            time.sleep(0.01)

def csv_input_mode(ser, logfile, datafile):
    f = open(logfile, 'w')
    data = np.genfromtxt(datafile,delimiter=',')
    
    # print(data.shape)
    print(time.time())
    #
    for idx in range(1,len(data)):
        begin = time.time()
        
        ref_msg = REF_CHAR + intTo3Bytes(int(data[idx,0]*100)) + b',' + intTo3Bytes(int(data[idx,0]*100)) + b',' + intTo3Bytes(int(data[idx,1]*100)) + b',' + intTo3Bytes(int(data[idx,1]*100)) + b',' + END_CHAR
        ser.write(ref_msg)
        
        ser.write(READY)
        log1msg(ser,f)
        
        sleep_time = 0.01 - (time.time() - begin)
        if sleep_time > 0:
            time.sleep(sleep_time)
    #
    print(time.time())

def intTo3Bytes(intvar):
    return str.encode(str(intvar).zfill(3))

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 2:
        LOG_FILE = sys.argv[1]
        SER_PORT = sys.argv[2]
    else:
        LOG_FILE = 'default.log'
        SER_PORT = "/dev/ttyUSB0"

    ser = serial.Serial(SER_PORT, BAUD, timeout=2)

    if not ser.isOpen():
        ser.open()
        print("Serial Open")

    if len(sys.argv) == 4:
        csv_input_mode(ser, LOG_FILE, sys.argv[3])
    else:
        manual_input_mode(ser, LOG_FILE)




