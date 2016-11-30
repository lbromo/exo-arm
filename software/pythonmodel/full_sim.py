import matplotlib
matplotlib.use('QT4Agg')
import mech_arm
import activation_signal
import muscle
import muscle_utils
import params
import time
import matplotlib.pyplot as plt
import sys
sys.path.append("../sensor/pyo")
import myo_raw as myo
import numpy as np

emg = np.genfromtxt("lasse.log", delimiter=',')
emg_max = max(emg[:, 4])
emg_min = min(emg[:, 4])


def update(emg, moving):
  global x
  e = (emg[3] - emg_min)/(emg_max - emg_min)
  #print(e)

  a = activation_signal.act_sig(1, e)
  angles = [0, 0, float(x[0, -1]), float(x[1, -1])]
  tmp = muscle.get_torque_estimate(angles, a, muscle_utils.MUSCLE_JOINT.ELBOW)
  tau.append(tmp)
  u = [0, tmp]
  x_new = np.reshape(arm.step(u), (4,1))
  x = np.append(x, x_new, axis=1)

  ## Plot stuff we dont care about

  line.set_data([0,
                 params.l1 * np.sin(x[0, -1]),
                 params.l1 * np.sin(x[0, -1]) + params.l2 * np.sin(x[1, -1])],
                [0,
                 params.l1 * -np.cos(x[0, -1]),
                 params.l1 * -np.cos(x[0, -1]) - params.l2 * np.cos(x[1, -1])])

  fig.canvas.restore_region(background)
  ax.draw_artist(line)
  fig.canvas.blit(ax.bbox)


ts = 0.01  # sample time
x = np.array([[0], [0], [0], [0]])  # initial conditions

## Prepare
arm = mech_arm.Mech_2_dof_arm(x0=x, ts=ts)
muscle = muscle.Muscle()

## Setup input signals
activation_levels = 0.25 * np.sin(np.linspace(0, 10*np.pi, 30/ts))
activation_levels[activation_levels < 0] = 0
activation_levels = np.append(activation_levels, 0 * np.linspace(0, 1, 10/ts))
tau = []

## Plot wtuff we dont care about
fig, ax = plt.subplots(1, 1)
ax.set_aspect('equal')
ax.set_xlim(-0.35, 0.35)
ax.set_ylim(-0.35, 0.35)
ax.hold(True)

plt.ion()
plt.draw()
plt.show(False)

line, = ax.plot([0,
                 params.l1 * np.sin(x[0, 0]),
                 params.l1 * np.sin(x[0, 0]) + params.l2 * np.sin(x[1, 0])],
                [0,
                 params.l1 * -np.cos(x[0, 0]),
                 params.l1 * -np.cos(x[0, 0]) - params.l2 * np.cos(x[1, 0])],
                'o-', lw=2)

background = fig.canvas.copy_from_bbox(ax.bbox)

fig.canvas.draw()
ax.figure.canvas.draw()

print("1")
time.sleep(1)
print("2")

myo = myo.MyoRaw()
myo.connect()
myo.add_emg_handler(update)

while(1):
  myo.run(1)

