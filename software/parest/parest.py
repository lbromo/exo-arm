import serial
import collections
import threading
import scipy
from scipy import signal
import numpy as np
import time

SAMPLE_F_HZ = 4
SAMPLE_PERIOD_S = 1/SAMPLE_F_HZ

SER_PORT = "/dev/ttyACM0"
BAUD = 9600

MOTOR1_FILE = "motor1.log"
MOTOR2_FILE = "motor2.log"
START = str('b\'$\\r\\n\'')
MOTORIDINDEX = 3
MSGSTARTINDEX = 5

stop = False

def decodeMsg(msg):
	msgstr = str(msg)
	motorid = msgstr[MOTORIDINDEX]
	datastr = msgstr[MSGSTARTINDEX:msgstr.find('\\')]
	idAndString = collections.namedtuple('Point', ['id', 'string'])
	returnColl = idAndString(id=motorid, string=datastr)
	return returnColl

def logging_thread(ser):
	print("Logging thread started")
	if ser.isOpen():
		while not stop:
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
		print("Logging stopped")
		ser.close();
	

def control_thread(ser, sig):
	if ser.isOpen():
		for i in range(0, len(sig)):
			starttime = time.time()
			a = '1' + str(int(127*sig[i])).zfill(3) + '1' + str(int(127*sig[i])).zfill(3)
			out = str.encode(a)
			print(out);
			ser.write(out)
			while (time.time()<starttime+SAMPLE_PERIOD_S):
				pass
	global stop
	stop = True

if __name__ == "__main__":
	ser = serial.Serial()
	ser.port = SER_PORT
	ser.baudrate = BAUD
	ser.open()

	motor1_file_h = open(MOTOR1_FILE, 'w');
	motor2_file_h = open(MOTOR2_FILE, 'w');

	motor1_file_h.write("time,angle,velocity,current\n")
	motor2_file_h.write("time,angle,velocity,current\n")
	t = np.linspace(0,20,100)
	sig = signal.square(2*np.pi*t, duty=0.5)
	sig = (sig+1)/2

	try:
		print("Starting threads")
		log = threading.Thread(target=logging_thread,args=(ser,))
		ctrl= threading.Thread(target=control_thread,args=(ser, sig))
		log.daemon=True
		ctrl.daemon=True
		log.start()
		ctrl.start()
		while log.is_alive():
			pass
	except Exception as e:
		print(e)
		print("Error: Unable to start Thread")
