import serial
import time

SER_PORT = "/dev/ttyMCC"
BAUD = 115200

READY = b'&'
START = str('b\'$\\r\\n\'')

def log1msg(ser):
    if ser.isOpen():
        initmsg = ser.readline()
        print(initmsg)

        if str(initmsg) == START:
            msg = ser.readline()
            motor, data_w_units = decodeMsg(msg)
            print("Received msg: " + str(data_w_units))

if __name__ == "__main__":
    ser = serial.Serial(SER_PORT, BAUD, timeout=2)

    if not ser.isOpen():
        ser.open()
        print("Serial Open")

    for idx in range(0,100000):
        ser.write(READY)
        log1msg(ser)
        log1msg(ser)
        #time.sleep(0.01)


