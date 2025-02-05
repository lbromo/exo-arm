import sys, time, pickle, socket
import numpy as np
sys.path.append('mechanics')
sys.path.append('muscles')
sys.path.append('../../../pymyo')
import mech_arm
import activation_signal
import muscle, muscle_utils, emg, pymyo

UDP_IP = '127.0.0.1'
UDP_PORT = 7331

x = []
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

K = np.array([
  [12, 0, 3, 0],
  [0, 12, 0, 3]
])

ref = np.zeros((4,1))

def update(emg_meas):
  global x, n, K, ref
  _emg.on_emg_measurement(emg_meas.sample1)
  _emg.on_emg_measurement(emg_meas.sample2)

  angles = [float(x[1, -1]), float(x[0, -1])]
  tau = np.array([0, 0])
  u = np.array([0, 0])

  for m in muslces:
    tmp = np.array([
      0, #m.get_torque_estimate(angles, muscle_utils.MUSCLE_JOINT.SHOULDER),
      m.get_torque_estimate(angles, muscle_utils.MUSCLE_JOINT.ELBOW),
    ])
    if abs(tmp[1]) < 1:
      tmp = 0
    tau = tau + tmp

  print(tau)

  ref[0] = ref[0] + tau[0] * 0.01
  ref[1] = ref[1] + tau[1] * 0.01
  ref[2] = tau[0] * 0.01
  ref[3] = tau[1] * 0.01
  e = ref - x
  print(ref)
  u_tmp = arm.M(*np.reshape(x, (4,))).dot(K.dot(e)) + arm.N(*np.reshape(x, (4,)))
  u[0] = u_tmp[0]
  u[1] = u_tmp[1]

  x_new = arm.step(u)
  x = np.reshape(x_new, (4,1))
  tmp = "{},{},{},{}".format(
    x_new[0], x_new[1], x_new[2], x_new[3]
  )
  msg = bytes(
    tmp,
    'ascii'
  )
  sock.sendto(msg, (UDP_IP, UDP_PORT))
  #time.sleep(0.25)

## Prepare mech model
ts = 0.01  # sample time
x = np.array([[0], [0], [0], [0]])  # initial conditions
arm = mech_arm.Mech_2_dof_arm(x0=x, ts=ts)


# Setup muscles
with open('2muslces_cleaned.pickle', 'rb') as f:
    pars = pickle.load(f)

_emg = emg.EMG()
muslces = muscle.create_muscles(pars)

for m in muslces:
  _emg.register_observer(m._activation_signal)


## SIMULATE
if (len(sys.argv) == 2):
  with open(sys.argv[1]) as f:
    for line in f:
      start = time.time()
      emg = [int(e) for e in line.split(',')]
      emg = emg[1:]
      update(emg, 0)
      time.sleep(ts - (time.time() - start))
else:
  ## Connect to myo and add the update function as callback
  myo = pymyo.PyMyo(on_emg=update)
  myo.connect()
  myo.enable_services(emg_mode=2)
  while(1):
    myo.waitForNotifications()
