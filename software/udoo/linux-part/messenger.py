import serial
import time
import numpy as np

BAUD = 230400

READY = b'&'
START_CHAR = '$'
START = str('b\'$\\r\\n\'')
REF_CHAR = b'R'

REF = np.array([np.pi/2, np.pi/2,0,0])

def log1msg(ser):
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
            print(str(data_w_units))

def intTo3Bytes(intvar):
    return str.encode(str(intvar).zfill(3))

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        SER_PORT = sys.argv[1]
    else:
        SER_PORT = "/dev/ttyACM0"

    if len(sys.argv) == 4:
        ref_s = float(sys.argv[2])
        ref_e = float(sys.argv[3])
    else:
        ref_s = 90
        ref_e = 90

    REF = np.array([
        np.radians(ref_s),
        np.radians(ref_e),
        0,
        0
    ])

    print('Goding to: ('+ str(REF[0]) +',', str(REF[1]) + ')')

    ser = serial.Serial(SER_PORT, BAUD, timeout=2)

    if not ser.isOpen():
        ser.open()
        print("Serial Open")
    time.sleep(0.01)
    ref_msg = REF_CHAR + (intTo3Bytes(int(REF[0]*100))) + (intTo3Bytes(int(REF[1]*100))) +(intTo3Bytes(int(REF[2]*100))) +(intTo3Bytes(int(REF[3]*100)))
    ser.write(ref_msg)
    print(ref_msg)

    for idx in range(0,100000):
	try:
            ser.write(READY)
            log1msg(ser)
            log1msg(ser)
        except:
            ser.write(b'S')
            time.sleep(0.01)
            exit()
        else:
            time.sleep(0.01)


