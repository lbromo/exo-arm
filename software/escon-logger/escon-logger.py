import serial
SER_PORT = "/dev/ttyMCC"
BAUD = 9600

MOTOR1_FILE = "motor1.log"
MOTOR2_FILE = "motor2.log"
START = str('b\'$\\r\\n\'')

if __name__ == "__main__":
	ser = serial.Serial()
	ser.port = SER_PORT
	ser.baudrate = BAUD
	ser.open()

	motor1_file_h = open(MOTOR1_FILE, 'w');
	motor2_file_h = open(MOTOR2_FILE, 'w');

	motor1_file_h.write("time,angle,velocity,current\n")
	motor2_file_h.write("time,angle,velocity,current\n")

	if ser.isOpen():
		while True:
			initmsg = ser.readline()
			if str(initmsg) == START:
				msg = ser.readline()
				msgstr = str(msg)
				if msgstr[3] == '1':
					i = 5
					print("motor1")
					print(msgstr)
					while msgstr[i] != '\\':
						motor1_file_h.write(msgstr[i])
						i += 1
					motor1_file_h.write('\n')
				elif msgstr[3] == '2':
					print("motor2")
					print(msgstr)
					i = 5
					while msgstr[i] != '\\':
						motor2_file_h.write(msgstr[i])
						i += 1
					motor2_file_h.write('\n')