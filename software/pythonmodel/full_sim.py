import numpy as np
import mech_arm
import matplotlib
matplotlib.use('GTKAgg')
import muscle
import muscle_utils
import params
import time
import matplotlib.pyplot as plt


if __name__ == '__main__':
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

  plt.show(False)
  plt.draw()

  line, = ax.plot([0,
                   params.l1 * np.sin(x[0, 0]),
                   params.l1 * np.sin(x[0, 0]) + params.l2 * np.sin(x[1, 0])],
                  [0,
                   params.l1 * -np.cos(x[0, 0]),
                   params.l1 * -np.cos(x[0, 0]) - params.l2 * np.cos(x[1, 0])],
                  'o-', lw=2)

  background = fig.canvas.copy_from_bbox(ax.bbox)

  fig.canvas.draw()

  ## Simulate
  for a in activation_levels:
    step_time = time.time()
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

    # sleep untill next sample time
    time.sleep(ts - (time.time() - step_time))
