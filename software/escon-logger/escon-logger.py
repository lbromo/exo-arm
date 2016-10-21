import serial
SER_PORT = "/dev/ttyMCC"
BAUD = 9600

MOTOR1_FILE = "motor1.log"
MOTOR2_FILE = "motor2.log"

if __name__ == "__main__":
	ser = serial.Serial()
	ser.port = SER_PORT
	ser.baudrate = BAUD
	ser.open()
	if ser.isOpen():
		while True:
			print ser.readline()
	else: