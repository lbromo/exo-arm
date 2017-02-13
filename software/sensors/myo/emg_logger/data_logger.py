# Add pyo to the python path
import sys
sys.path.append('pyo')
import myo_raw

EMG_FILE = "emg.log"
ACC_FILE = "acc.log"
GYRO_FILE = "gyro.log"
QUAT_FILE = "quat.log"

emg_file_h = None
acc_file_h = None
gyro_file_h = None
quat_file_h = None


def on_emg(emg, moving):
    emg_file_h.write(','.join([str(i) for i in emg]) + '\n')


def on_imu(quat, acc, gyro):
    quat_file_h.write(','.join([str(i) for i in quat]) + '\n')
    acc_file_h.write(','.join([str(i) for i in acc]) + '\n')
    gyro_file_h.write(','.join([str(i) for i in gyro]) + '\n')


if __name__ == '__main__':
    emg_file_h = open(EMG_FILE, 'w')
    acc_file_h = open(ACC_FILE, 'w')
    gyro_file_h = open(GYRO_FILE, 'w')
    quat_file_h = open(QUAT_FILE, 'w')

    myo = myo_raw.MyoRaw()
    myo.connect()

    myo.add_emg_handler(on_emg)
    myo.add_imu_handler(on_imu)

    print("GO!")

    try:
        while(1):
            myo.run(1)
    except (KeyboardInterrupt, SystemExit):
        emg_file_h.close()
        acc_file_h.close()
        gyro_file_h.close()
        quat_file_h.close()
