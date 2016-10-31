# Add pyo to the python path
import sys
sys.path.append('pyo')
import myo_raw
import time

global meas_no

NO_OF_MEAS = 200


emg_file_h = None

starttime = time.time()
meas_no = 0

def on_emg(emg, moving):
    global meas_no
    now = time.time() - starttime
    now_ms = int(now * 1000)
    datastr = str(now_ms) + ',' + ','.join([str(i) for i in emg]) + '\n'
    emg_file_h.write(datastr)
#    print(datastr)
    meas_no = meas_no+1


if __name__ == '__main__':
    NO_OF_SAMPLES = int(sys.argv[1])
    myo = myo_raw.MyoRaw()
    myo.connect()
    myo.mc_start_collection()
    myo.add_emg_handler(on_emg)

    try:
        for sample_no in range(0,NO_OF_SAMPLES):
            EMG_FILE = "./logs/"+sys.argv[2]+str(sample_no)+".log"
            emg_file_h = open(EMG_FILE, 'w')
            print("Rep " + str(sample_no+1) + ", move arm")
            meas_no = 0
            while(meas_no<NO_OF_MEAS):
                myo.run(1)
            emg_file_h.close()        
    except (KeyboardInterrupt, SystemExit):
        emg_file_h.close()
