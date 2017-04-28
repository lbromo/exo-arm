import sys, pickle, io
import time, threading
import serial
import numpy as np
sys.path.append('../../model/mechanics')
sys.path.append('../../model/muscles')
import mech_arm
import activation_signal
import muscle, muscle_utils, emg, pymyo

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
_ser = None
_logfile = None
_muscles = None
_raf = None

ref = np.zeros((4,))
B = 0.25

MAX_LOG_MSG_LEN = 1 + 10 + 11*12

def intTo3Bytes(intvar):
    return str.encode(str(intvar).zfill(3))

def log1msg(ser, logfile):
    msg = ser.read(ser.in_waiting)

    if msg:
        msg = msg.replace(b'$,', b'').replace(b'\r', b'')
        logfile.write(msg)

    return len(msg)

def tLogger(ser, f):
    while LOGGING:
        t_start = time.time()
        with SER_LOCK:
            ser.write(READY)
        log1msg(ser,f)
        time.sleep(0.01)

def get_angles(f):
    global _angles
    """
    Message format:
         [0]       [1]     [2]            [3]              [4]               [5]             [6]        [7]        [8]             [9]         [10]          [11]
    <start char>, time, shoulder, <shoulder pos ref>, <shoulder pos>, <shoulder vel>, <shoulder cur>, elbow, <elbow pos ref>, <elbow pos>, <elbow vel>, <elbow cur>
    """
    offset = -2 * MAX_LOG_MSG_LEN
    f.seek(offset, io.SEEK_END)
    buff = f.read(abs(offset))
    msgs = buff.split(b'\n')
    lastest_full_msg = msgs[-2]  # The last line may not fu a "fulll" line, so we go 2 back
    shoulder_angle = int(lastest_full_msg[4]) * 0.01
    elbow_angle    = int(lastest_full_msg[14]) * 0.01

    _angles = [shoulder_angle, elbow_angle]
    return _angles


def update(emg_meas):
    global _raf
    _emg.on_emg_measurement(emg_meas.sample1)
    _emg.on_emg_measurement(emg_meas.sample2)

    t_start = time.time()
    angles = get_angles(_raf)
    tau = np.array([0, 0])
    for m in _muslces:
        tmp = np.array([
            0, #m.get_torque_estimate(angles, muscle_utils.MUSCLE_JOINT.SHOULDER),
            m.get_torque_estimate(angles, muscle_utils.MUSCLE_JOINT.ELBOW),
        ])
        if abs(tmp[1]) < 1:
            tmp = 0
        tau = tau + tmp

    tmp = tau * B

    ref[0] = ref[0] + ref[2] * 0.01
    ref[1] = ref[1] + ref[3] * 0.01
    ref[2] = tmp[0]
    ref[3] = tmp[1]

    ref_msg = REF_CHAR + (intTo3Bytes(int(ref[0]*100))) + b',' + (intTo3Bytes(int(ref[1]*100))) + b',' + (intTo3Bytes(int(ref[2]*100))) + b',' + (intTo3Bytes(int(ref[3]*100))) + b',' + END_CHAR
    print(ref_msg)
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

    t = threading.Thread(target=tLogger, args=(_ser, _raf))
    t.daemon = False
    t.start()

    # Setup muscles
    with open('../../../software/model/2muslces_cleaned.pickle', 'rb') as f:
        pars = pickle.load(f)

    _emg = emg.EMG()
    _muslces = muscle.create_muscles(pars)

    for m in _muslces:
        _emg.register_observer(m._activation_signal)

    myo = pymyo.PyMyo(on_emg=update)
    myo.connect()
    myo.enable_services(emg_mode=2)
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
    _ser.write(STOP)



