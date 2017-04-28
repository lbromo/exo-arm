import time, io, threading
import serial
import numpy as np

BAUD = 230400

READY = b'M'
START_CHAR = '$'
START = str('b\'$\\r\\n\'')
REF_CHAR = b'R'
END_CHAR = b'E'

SER_LOCK = threading.Lock()

LOGGING = True

def intTo3Bytes(intvar):
    return str.encode(str(intvar).zfill(3))

def log1msg(ser, logfile):
    msg = ser.read(ser.in_waiting)

    if msg:
        msg = msg.replace(b'$,', b'').replace(b'\r', b'')
        logfile.write(msg)

    return len(msg)

def tLogger(ser, f):
    while LOGGING:
        with SER_LOCK:
            ser.write(READY)
        log1msg(ser,f)
        time.sleep(0.01)

    #ser.reset_output_buffer()
    #ser.reset_input_buffer()

def updateRef(ser):
    try:
        ref_shoulder, ref_elbow = [int(var) for var in raw_input("Enter new reference: ").split()]
    except KeyboardInterrupt:
        raise
    except:
        print("Error getting new ref. Please input as <shoulder_ref elbow_ref>")
    else:
        ref = np.array([
            np.radians(ref_shoulder),
            np.radians(ref_elbow),
            0,
            0
        ])
        print('Going to: ('+ str(ref[0]) +',', str(ref[1]) + ')')
        ref_msg = REF_CHAR + (intTo3Bytes(int(ref[0]*100))) + b',' + (intTo3Bytes(int(ref[1]*100))) + b',' + (intTo3Bytes(int(ref[2]*100))) + b',' + (intTo3Bytes(int(ref[3]*100))) + b',' + END_CHAR
        with SER_LOCK:
            ser.write(ref_msg)

def manual_input_mode(ser, logger_h, log_file_h):
    global LOGGING

    while True:
        try:
            updateRef(ser)
        except:
            LOGGING = False
            logger_h.join()
            log_file_h.close()
            ser.write(b'S')
            ser.close()
            break
        else:
            time.sleep(0.01)

def csv_input_mode(ser, logger_h, log_file_h, datafile):
    global LOGGING
    data = np.genfromtxt(datafile,delimiter=',')

    start_time = time.time()

    for idx in range(1,len(data),1):
        begin = time.time()

        ref_msg = REF_CHAR + \
                  intTo3Bytes(int(data[idx,0]*100)) + b',' + \
                  intTo3Bytes(int(data[idx,0]*100)) + b',' + \
                  intTo3Bytes(int(data[idx,1]*100)) + b',' + \
                  intTo3Bytes(int(data[idx,1]*100)) + b',' + \
                  END_CHAR

        with SER_LOCK:
            ser.write(ref_msg)

        sleep_time = 0.01 - (time.time() - begin)
        if sleep_time > 0:
            time.sleep(sleep_time)

    print(time.time() - start_time)
    LOGGING = False
    logger_h.join()
    log_file_h.close()

    ser.write(b'S')
    ser.close()

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 2:
        LOG_FILE = sys.argv[1]
        SER_PORT = sys.argv[2]
    else:
        LOG_FILE = "default.log"
        SER_PORT = "/dev/ttyUSB0"

    ser = serial.Serial(SER_PORT, BAUD, timeout=2)
    bw = io.BufferedWriter(io.FileIO(LOG_FILE, 'wb'))

    t = threading.Thread(target=tLogger, args=(ser, bw))
    t.daemon = False
    t.start()

    if not ser.isOpen():
        ser.open()
        print("Serial Open")

    if len(sys.argv) == 4:
        csv_input_mode(ser, t, bw, sys.argv[3])
    else:
        manual_input_mode(ser, t, bw)




