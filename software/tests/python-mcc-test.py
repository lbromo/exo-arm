import serial
import sys

SER_PORT = sys.argv[1]
BAUD = 115200
TIMEOUT = 0.5

if __name__ == "__main__":
	ser = serial.Serial(timeout = TIMEOUT, baudrate = BAUD, port = SER_PORT)
	
	if not ser.isOpen():
		ser.open()
	else:
		for i in range(1,100):
			out = str.encode(str(i))
			ser.write(out)
			ret = str(ser.read())
			print(ret)
	ser.close()


