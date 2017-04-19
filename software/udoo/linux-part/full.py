import sys,pickle
import serial
import numpy as np
sys.path.append('../../model/mechanics')
sys.path.append('../../model/muscles')
sys.path.append('../../../../pymyo')
import mech_arm
import activation_signal
import muscle, muscle_utils, emg, pymyo

BAUD = 230400

READY = b'M'
START_CHAR = '$'
START = str('b\'$\\r\\n\'')
REF_CHAR = b'R'
END_CHAR = b'E'

_angles = None
_emg = None
_ser = None
_logfile = None
_muscles = None


def intTo3Bytes(intvar):
    return str.encode(str(intvar).zfill(3))

def get_angles(ser, logfile):
    """
    Message format:
         [0]       [1]     [2]            [3]              [4]               [5]             [6]        [7]        [8]             [9]         [10]          [11]
    <start char>, time, shoulder, <shoulder pos ref>, <shoulder pos>, <shoulder vel>, <shoulder cur>, elbow, <elbow pos ref>, <elbow pos>, <elbow vel>, <elbow cur>
    """
    if ser.isOpen():
        ser.write(READY)
        initmsg = ser.readline()
        if not len(initmsg):
            return

        initmsg = initmsg.decode()

        if initmsg[0] == START_CHAR:
            # Removeing the <start char,> -- we have the following left
            #  [0]    [1]             [2]               [3]             [4]             [5]        [6]        [7]             [8]          [9]         [10]
            # time, shoulder, <shoulder pos ref>, <shoulder pos>, <shoulder vel>, <shoulder cur>, elbow, <elbow pos ref>, <elbow pos>, <elbow vel>, <elbow cur>

            msg = initmsg[2:]
            # print(msg)
            data_w_units = msg.strip().split(',')
            logfile.write(','.join(str(x) for x in data_w_units) + '\n')

            shoulder_pos = data_w_units[3] * 0.01
            elbow_pos = data_w_units[8] * 0.01
            return shoulder_pos, elbow_pos

def update(emg_meas):
    angles = list(get_angles(_ser, _logfile))
    _emg.on_emg_measurement(emg_meas.sample1)
    _emg.on_emg_measurement(emg_meas.sample2)

    for m in _muslces:
        tmp = np.array([
            0, #m.get_torque_estimate(angles, muscle_utils.MUSCLE_JOINT.SHOULDER),
            m.get_torque_estimate(angles, muscle_utils.MUSCLE_JOINT.ELBOW),
        ])
        if abs(tmp[1]) < 1:
            tmp = 0
            tau = tau + tmp

    ref[0] = ref[0] + tau[0] * 0.01
    ref[1] = ref[1] + tau[1] * 0.01
    ref[2] = tau[0] * 0.01
    ref[3] = tau[1] * 0.01
    print(ref)

    ref_msg = REF_CHAR + (intTo3Bytes(int(ref[0]*100))) + b',' + (intTo3Bytes(int(ref[1]*100))) + b',' + (intTo3Bytes(int(ref[2]*100))) + b',' + (intTo3Bytes(int(ref[3]*100))) + b',' + END_CHAR
    print(ref_msg)
    ser.write(ref_msg)


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

    _logfile = open(log_path, 'w')

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
    while(1):
        myo.waitForNotifications()



