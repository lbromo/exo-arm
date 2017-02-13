import serial
import collections
import time
SER_PORT = "/dev/ttyACM2"
BAUD = 115200

MOTOR1_FILE = "motor1.log"
MOTOR2_FILE = "motor2.log"
START = str('b\'$\\r\\n\'')
MOTORIDINDEX = 3
MSGSTARTINDEX = 5

SAMPLE_F_HZ = 100
SAMPLE_T_S = 1/SAMPLE_F_HZ

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
	ser.timeout = 0
	ser.open()

	motor1_file_h = open(MOTOR1_FILE, 'w');
	motor2_file_h = open(MOTOR2_FILE, 'w');

	motor1_file_h.write("time,angle,velocity,current\n")
	motor2_file_h.write("time,angle,velocity,current\n")

	if ser.isOpen():
		while ser.inWaiting() > 0:
			ser.read()
			print("flushing")
		print("Starting loop")
		while True:
			starttime = time.time()
			ser.write(b'$1100011000')
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
			time_to_sleep = starttime+SAMPLE_T_S-time.time()
			print("tts:")
			print(time_to_sleep)
			if time_to_sleep > 0:
				time.sleep(time_to_sleep)
			else:
				while ser.inWaiting() > 0:
					ser.read()
					print("flushing")
