import sys, pickle, io
import time, threading
import serial
import numpy as np
import scipy.signal as sc
sys.path.append('../../model/mechanics')
sys.path.append('../../model/muscles')
import mech_arm
import activation_signal
import muscle, muscle_utils, emg, pymyo

from collections import deque
from iir_filter import iir_filter

BAUD = 230400

READY = b'M'
STOP = b'S'
START_CHAR = '$'
START = str('b\'$\\r\\n\'')
REF_CHAR = b'R'
END_CHAR = b'E'

LOGGING = True
SER_LOCK = threading.Lock()

_angles = None
_emg = None
_emg_logger = None
_ser = None
_logfile = None
_muscles = None
_raf = None
_raf_lock = threading.Lock()

_ref_log = None

_t_start = None

M = 1
B = 8
D = 0

tau = deque([0]*3, maxlen=3)
vel = deque([0]*3, maxlen=3)
num = [0, B, 0]
den = [M, B, D]
sysd = sc.cont2discrete( (num, den), dt=0.01, method='tustin')
numd = sysd[0][0]
dend = sysd[1]

ref = np.zeros((4,))

MAX_LOG_MSG_LEN = 1 + 10 + 11*12

# Hacky flag
first = True

def intTo3Bytes(intvar):
    return str.encode(str(intvar).zfill(3))

def log1msg(ser, logfile):
    msg = ser.read(ser.in_waiting)

    if msg:
        msg = msg.replace(b'$,', b'').replace(b'\r', b'')
        with _raf_lock:
            logfile.write(msg)

    return len(msg)

def tLogger(ser, f):
    while LOGGING:
        t_start = time.time()
        with SER_LOCK:
            ser.write(READY)
        log1msg(ser,f)
        time.sleep(0.008)

def get_angles(f):
    global _angles
    """
    Message format:
         [0]       [1]     [2]            [3]              [4]               [5]             [6]        [7]        [8]             [9]         [10]          [11]
    <start char>, time, shoulder, <shoulder pos ref>, <shoulder pos>, <shoulder vel>, <shoulder cur>, elbow, <elbow pos ref>, <elbow pos>, <elbow vel>, <elbow cur>
    """
    offset = -2 * MAX_LOG_MSG_LEN
    with _raf_lock:
        f.seek(offset, io.SEEK_END)
        buff = f.read(abs(offset))
        f.seek(0, io.SEEK_END)

    msgs = buff.split(b'\n')
    lastest_full_msg = msgs[-2]  # The last line may not fu a "full" line, so we go 2 back
    lastest_full_msg = lastest_full_msg.decode('ascii').split(',')
    shoulder_angle = int(lastest_full_msg[5])  * 0.01 if int(lastest_full_msg[5]) * 0.01 > 0 else 0
    elbow_angle    = int(lastest_full_msg[14]) * 0.01 if int(lastest_full_msg[14]) * 0.01 > 0 else 0

    _angles = [shoulder_angle, elbow_angle]

    return _angles


def update(emg_meas):
    global _raf, tau_int, tau_diff
    _emg.on_emg_measurement(emg_meas.sample1)
    _emg.on_emg_measurement(emg_meas.sample2)

    angles = get_angles(_raf)
    tau_tmp = np.array([0, 0])
    for m in _muslces:
        tmp = np.array([
            0, #m.get_torque_estimate(angles, muscle_utils.MUSCLE_JOINT.SHOULDER),
            m.get_torque_estimate([angles[1], angles[0]], muscle_utils.MUSCLE_JOINT.ELBOW),
        ])
        # HACK used in <best.log> with 8*s/(s+8)
        if m.muscle_type == muscle_utils.MUSCLE_NAME.BICEPS_BRACHII:
            tmp = 1.5 * tmp
        tau_tmp = tau_tmp + tmp

    tau.append(tau_tmp[1])
    tmp = iir_filter(numd, dend, tau, vel)
    vel.append(tmp)

    #tmp = 2.5*tau_tmp[1]

	if first == True:
		ref[1] = angles[1]
		first == False

    ref[0] = 0
    # ref[1] = angles[1] + 0.01 * tmp
    ref[1] = ref[1] + 0.01 * tmp
    ref[2] = 0
    ref[3] = 2*tau_tmp[1]

    # Antiwindup
    if ref[1] > 1.6:
    	ref[1] = 1.6
    if ref[1] < 0:
    	ref[1] = 0

    ref_msg = REF_CHAR + (intTo3Bytes(int(ref[0]*100))) + b',' + (intTo3Bytes(int(ref[1]*100))) + b',' + (intTo3Bytes(int(ref[2]*100))) + b',' + (intTo3Bytes(int(ref[3]*100))) + b',' + END_CHAR

    print_msg = "{},{},{},{},{},{},{}".format(
        time.time() - t_start,
        ref[0], ref[1],
        ref[2], ref[3],
        tau_tmp[0], tau_tmp[1]
    )
    print(print_msg)
    _ref_log.write(print_msg + '\n')
    with SER_LOCK:
        _ser.write(ref_msg)


if __name__ == "__main__":
    import sys
    if len(sys.argv) >2:
        log_path = sys.argv[1]
        ser_port = sys.argv[2]
    elif len(sys.argv) > 1:
        log_path = sys.argv[1]
        ser_port = "/dev/ttyUSB0"
    else:
        log_path = 'default.log'
        ser_port = "/dev/ttyUSB0"

    _ser = serial.Serial(ser_port, BAUD, timeout=2)
    if not _ser.isOpen():
        _ser.open()
        print("Serial Open")
    _ser.write(STOP)

    _raf = io.BufferedRandom(io.FileIO(log_path, 'wb+'))
    _ref_log = open(log_path + '.ref', 'w')
    _ref_log.write("time,spos,epos,svel,evel,stau,etau" + '\n')

    # Setup muscles
    with open('../../../software/model/2muslces_cleaned.pickle', 'rb') as f:
        pars = pickle.load(f)

    _emg = emg.EMG()
    _emg_logger = emg.EMG_logger(log_path + '.emg')
    _emg.register_observer(_emg_logger)
    _muslces = muscle.create_muscles(pars)

    for m in _muslces:
        _emg.register_observer(m._activation_signal)

    tmp = 0
    _muslces[0]._activation_signal._d = tmp
    _muslces[1]._activation_signal._d = tmp

    # _muslces[0].Fcemax = _muslces[0].Fcemax * 1.5 for test1
    _muslces[0].Fcemax = _muslces[0].Fcemax
    _muslces[1].Fcemax = _muslces[1].Fcemax

    myo = pymyo.PyMyo(on_emg=update)
    myo.connect()
    myo.set_sleep_mode(sleep_mode=pymyo.lib.myohw_sleep_mode_never_sleep)
    myo.enable_services(emg_mode=2)

    t = threading.Thread(target=tLogger, args=(_ser, _raf))
    t.daemon = False
    t.start()

    t_start = time.time()
    while True:
        try:
            myo.waitForNotifications()
        except KeyboardInterrupt as e:
            print(e)
            break
        except Exception as e:
            print(e)
            break

    LOGGING = False
    t.join()
    _raf.close()
    _ref_log.close()
    _ser.write(STOP)



