import serial
import sys

SER_PORT = sys.argv[1]
BAUD = 115200
TIMEOUT = 0.5

if __name__ == "__main__":
	ser = serial.Serial(timeout = TIMEOUT, baudrate = BAUD, port = SER_PORT)
	ser.close()
	if not ser.isOpen():
		print("Opening Serial...")
		ser.open()
		print("Flushing Serial...")
		while ser.inWaiting() > 0:
			ser.read()
	if ser.isOpen():
		for i in range(1,10):
			out = str.encode(str(i))
			ser.write(out)
			ret = str(ser.read())
			if not ret[2] == str(i):
				print("We messed up..")
			else:
				print("Its all good..")
		ser.close()


