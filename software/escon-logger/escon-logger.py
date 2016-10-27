import serial
import collections
SER_PORT = "/dev/ttyACM0"
BAUD = 9600

MOTOR1_FILE = "motor1.log"
MOTOR2_FILE = "motor2.log"
START = str('b\'$\\r\\n\'')
MOTORIDINDEX = 3
MSGSTARTINDEX = 5

def decodeMsg(msg):
	msgstr = str(msg)
	motorid = msgstr[MOTORIDINDEX]
	datastr = msgstr[MSGSTARTINDEX:msgstr.find('\\')]
	idAndString = collections.namedtuple('Point', ['id', 'string'])
	returnColl = idAndString(id=motorid, string=datastr)
	return returnColl
	
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
				msgdata = decodeMsg(msg)
				print(msgdata.string)
				if msgdata.id == '1':
					motor1_file_h.write(msgdata.string)
					motor1_file_h.write('\n')
				elif msgdata.id == '2':
					motor2_file_h.write(msgdata.string)
					motor2_file_h.write('\n')