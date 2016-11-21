import matplotlib.pyplot as plt
import numpy as np

from enum import Enum

class MUSCLE_NAME(Enum):
  TRICEPS_BRACHII = 1
  BICEPS_BRACHII = 2

class MUSCLE_JOINT(Enum):
  ELBOW = 1
  SHOULDER = 2


def __raise__(msg):
  raise Exception(msg)

def __calculate_muscle_length__(cst, r, s, t, u, angs):
  wRU, wFE, eFE, sFE = angs
  l = cst + r[1] * wRU**2 + r[0] * wRU**1 + \
  s[3] * wFE**4 + s[2] * wFE**3 + s[1] * wFE**2 + s[0] * wFE + \
  t[5] * eFE**6 + t[4] * eFE**5 + t[3] * eFE**4 + t[2] * eFE**3 + t[1] * eFE**2 + t[0] * eFE + \
  u[0] * sFE;
  return l

def __biceps_brachii_length__(angs):
  cst = 378.06
  r = [0, 0]
  s = [0, 0, 0, 0]
  t = [-25.587e-2, -7.9101e-3, -3.1498e-5, 5.2156e-7, 0, 0]
  u = [-5.0981e-1]
  return __calculate_muscle_length__(cst, r, s, t, u, angs)

def __triceps_brachii_length__(angs):
  cst = 260.05
  r = [0, 0]
  s = [0, 0, 0, 0]
  t = [40.644e-2, 5.2856e-3, -22.491e-5, 33.321e-7, -2.3174e-8, 6.1385e-11]
  u = [-4.4331e-1]
  return __calculate_muscle_length__(cst, r, s, t, u, angs)

# Only takes a single angle?
def __moment_arm__(par, q):
  ma=0
  for x, n in zip(par, range(len(par))):
    ma = ma + x * q**n

  return ma

def __biceps_brachii_moment_arm__(joint, ang):
  if joint == MUSCLE_JOINT.ELBOW:
    c = [14.660,4.5322e-1,1.8047e-3,-2.9883e-5]
    return __moment_arm__(c, ang)
  elif joint == MUSCLE_JOINT.SHOULDER:
    d = [29.21]
    return __moment_arm__(d,ang)


def __triceps_brachii_moment_arm__(joint, ang):
  if joint == MUSCLE_JOINT.ELBOW:
    c = [-23.287, -3.0284e-1, 12.886e-3, -19.092e-5, 13.277e-7, -3.5171e-9]
    return __moment_arm__(c, ang)
  elif joint == MUSCLE_JOINT.SHOULDER:
    d = [-25.40]
    return __moment_arm__(d, ang)


def get_muscle_value(muscle, joint_angles, joint=None):
  switcher = {
    MUSCLE_NAME.BICEPS_BRACHII: {
      MUSCLE_JOINT.ELBOW: __biceps_brachii_moment_arm__,
      MUSCLE_JOINT.SHOULDER: __biceps_brachii_moment_arm__,
      None: __biceps_brachii_length__
    },
    MUSCLE_NAME.TRICEPS_BRACHII: {
      MUSCLE_JOINT.ELBOW: __triceps_brachii_moment_arm__,
      MUSCLE_JOINT.SHOULDER: __triceps_brachii_moment_arm__,
      None: __triceps_brachii_length__
    }
  }

  func = switcher.get(
    muscle,
    lambda x: __raise__("No such muscle")).get(
      joint,
      lambda x: __raise__("No such joint")
    )

  if(joint):
    return func(joint, joint_angles)
  else:
    return func(joint_angles)

if __name__ == '__main__':
  biceps_len, biceps_ma_elbow, biceps_ma_shoulder = ([], [], [])
  triceps_len, triceps_ma_elbow, triceps_ma_shoulder = ([], [], [])

  ## biceps
  for a in range(0,140):
    angs = [0,0,a,10]
    biceps_len.append(get_muscle_value(MUSCLE_NAME.BICEPS_BRACHII, angs))
    biceps_ma_elbow.append(get_muscle_value(MUSCLE_NAME.BICEPS_BRACHII, a, MUSCLE_JOINT.ELBOW))
    #biceps_ma_shoulder.append(get_muscle_value(MUSCLE_NAME.BICEPS_BRACHII, 1, MUSCLE_JOINT.SHOULDER))

    triceps_len.append(get_muscle_value(MUSCLE_NAME.TRICEPS_BRACHII, angs))
    triceps_ma_elbow.append(get_muscle_value(MUSCLE_NAME.TRICEPS_BRACHII, a, MUSCLE_JOINT.ELBOW))
    #triceps_ma_shoulder.append(get_muscle_value(MUSCLE_NAME.TRICEPS_BRACHII, a, MUSCLE_JOINT.SHOULDER))

  plt.figure(1)
  plt.subplot(3, 1, 1)
  plt.plot(biceps_len)

  plt.subplot(3, 1, 2)
  plt.plot(biceps_ma_elbow)

  plt.subplot(3, 1, 3)
  plt.plot(biceps_ma_shoulder)

  plt.figure(2)
  plt.subplot(3, 1, 1)
  plt.plot(triceps_len)

  plt.subplot(3, 1, 2)
  plt.plot(triceps_ma_elbow)

  plt.subplot(3, 1, 3)
  plt.plot(triceps_ma_shoulder)

  plt.show()
