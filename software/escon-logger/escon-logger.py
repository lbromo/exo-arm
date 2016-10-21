import serial


if __name__ == "__main__":
	ser = serial.Serial()
	ser.port = '/dev/ttyMCC/'
	ser.baudrate = 9600
	ser.open()
	if ser.isOpen():
		while True:
			print ser.readline()
