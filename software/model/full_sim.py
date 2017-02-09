import sys
sys.path.append('mechanics')
sys.path.append('muscles')
sys.path.append("../myo/pyo")
import matplotlib
matplotlib.use('GTKAgg')
import mech_arm
import activation_signal
import muscle
import muscle_utils
import params
import emg
import time
import matplotlib.pyplot as plt
import myo_raw as myo
import numpy as np
from collections import deque

x = []

def update(emg_meas, moving):
  global x, n
  _emg.on_emg_measurement(emg_meas)

  angles = [float(x[1, -1]), float(x[0, -1])]
  biceps_tau = np.array([
    biceps.get_torque_estimate(angles, muscle_utils.MUSCLE_JOINT.SHOULDER),
    biceps.get_torque_estimate(angles, muscle_utils.MUSCLE_JOINT.ELBOW)
  ])
  triceps_tau = np.array([
    triceps.get_torque_estimate(angles, muscle_utils.MUSCLE_JOINT.SHOULDER),
    triceps.get_torque_estimate(angles, muscle_utils.MUSCLE_JOINT.ELBOW)
  ])
  tot = biceps_tau + triceps_tau

  x_new = np.reshape(arm.step(tot), (4,1))
  x = np.append(x, x_new, axis=1)

  ## Plot stuff we dont care about

  lines.set_data([0,
                 params.l1 * np.sin(x[0, -1]),
                 params.l1 * np.sin(x[0, -1]) + params.l2 * np.sin(x[1, -1])],
                [0,
                 params.l1 * -np.cos(x[0, -1]),
                 params.l1 * -np.cos(x[0, -1]) - params.l2 * np.cos(x[1, -1])])

  fig.canvas.restore_region(background)
  ax.draw_artist(lines)
  fig.canvas.blit(ax.bbox)


## Prepare mech model
ts = 0.01  # sample time
x = np.array([[0], [0], [0], [0]])  # initial conditions
arm = mech_arm.Mech_2_dof_arm(x0=x, ts=ts)

# Setup mucles
_emg = emg.EMG()
biceps_act_sig = activation_signal.ActivationSignal(C1=-0.033, C2=-0.019, A=-0.200, d=0.05, pod=emg.EMGPOD.BICEPS_BRACHII)
triceps_act_sig = activation_signal.ActivationSignal(C1=-0.033, C2=-0.019, A=-0.200, d=0.05, pod=emg.EMGPOD.TRICEPS_BRACHII)

_emg.register_observer(biceps_act_sig)
_emg.register_observer(triceps_act_sig)

biceps = muscle.Muscle(
  biceps_act_sig,
  muscle_utils.MUSCLE_NAME.BICEPS_BRACHII)

triceps = muscle.Muscle(
  biceps_act_sig,
  muscle_type=muscle_utils.MUSCLE_NAME.TRICEPS_BRACHII, # Should be changed to muscle_name
  max_length=402.9,
  optimal_fiber_length=152.4,
  tensor_slack_length=190.5,
  max_force=1000,
  alpha=0.66,
  Spe=10,
  Sse=2.3,
  phi_m=0.5,
  phi_v=1
)

## Plot wtuff we dont care about
fig, ax = plt.subplots(1, 1)
ax.set_aspect('equal')
ax.set_xlim(-0.35, 0.35)
ax.set_ylim(-0.35, 0.35)
ax.hold(True)

plt.ion()
plt.draw()
plt.show(False)

lines, = ax.plot([0,
                 params.l1 * np.sin(x[0, 0]),
                 params.l1 * np.sin(x[0, 0]) + params.l2 * np.sin(x[1, 0])],
                [0,
                 params.l1 * -np.cos(x[0, 0]),
                 params.l1 * -np.cos(x[0, 0]) - params.l2 * np.cos(x[1, 0])],
                'o-', lw=2)

background = fig.canvas.copy_from_bbox(ax.bbox)

fig.canvas.draw()
ax.figure.canvas.draw()

## Connect to myo and add the update function as callback

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
  myo = myo.MyoRaw()
  myo.connect()
  myo.add_emg_handler(update)
  while(1):
    myo.run(1)
