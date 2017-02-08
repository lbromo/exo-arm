import matplotlib.pyplot as plt
import numpy as np

from enum import Enum

class MUSCLE_NAME(Enum):
  TRICEPS_BRACHII = 1
  BICEPS_BRACHII = 2
  BRACHIALIS = 3
  BRACHIORADIALIS = 4 

class MUSCLE_JOINT(Enum):
  ELBOW = 1
  SHOULDER = 2


def __raise__(msg):
  raise Exception(msg)

def __calculate_muscle_length__(cst, t, u, angs):   # + r[1] * wRU**2 + r[0] * wRU**1 + s[3] * wFE**4 + s[2] * wFE**3 + s[1] * wFE**2 + s[0] * wFE + \
  eFE, sFE = angs
  l = cst + \
  t[5] * eFE**6 + t[4] * eFE**5 + t[3] * eFE**4 + t[2] * eFE**3 + t[1] * eFE**2 + t[0] * eFE + \
  u[0] * sFE;
  return l - cst

def __brachialis_length__(angs):
  cst = 137.48
  t = [-9.6852e-2, -4.0282e-3, -4.0884e-5, 3.5832e-7, 0, 0]
  u = [0]
  return __calculate_muscle_length__(cst, t, u, angs)

def __brachioradialis_length__(angs):
  cst = 276.13
  t = [-34.017e-2, -2.9114e-3, -17.6e-5, 11.374e-7, 0, 0]
  u = [0]
  return __calculate_muscle_length__(cst, t, u, angs)

def __biceps_brachii_length__(angs):
  cst = 378.06
  t = [-25.587e-2, -7.9101e-3, -3.1498e-5, 5.2156e-7, 0, 0]
  u = [-5.0981e-1]
  return __calculate_muscle_length__(cst, t, u, angs)

def __triceps_brachii_length__(angs):
  cst = 260.05
  t = [40.644e-2, 5.2856e-3, -22.491e-5, 33.321e-7, -2.3174e-8, 6.1385e-11]
  u = [-4.4331e-1]
  return __calculate_muscle_length__(cst, t, u, angs)

# Only takes a single angle? yes the shoulder or elbow angle
def __moment_arm__(par, q):
  ma=0
  for x, n in zip(par, range(len(par))):
    ma = ma + x * q**n

  return ma

def __brachialis_moment_arm__(joint, angs):
  eFE, sFE = angs
  if joint == MUSCLE_JOINT.ELBOW:
    c = [5.5492,2.3080e-1,2.3425e-3,-2.0530e-5]
    return __moment_arm__(c, eFE)
  elif joint == MUSCLE_JOINT.SHOULDER:
    d = [0]
    return __moment_arm__(d,sFE)

def __brachioradialis_moment_arm__(joint, angs):
  eFE, sFE = angs
  if joint == MUSCLE_JOINT.ELBOW:
    c = [19.490,1.6681e-1,10.084e-3,-6.5171e-5]
    return __moment_arm__(c, eFE)
  elif joint == MUSCLE_JOINT.SHOULDER:
    d = [0]
    return __moment_arm__(d,sFE)

def __biceps_brachii_moment_arm__(joint, angs):
  eFE, sFE = angs
  if joint == MUSCLE_JOINT.ELBOW:
    c = [14.660,4.5322e-1,1.8047e-3,-2.9883e-5]
    return __moment_arm__(c, eFE)
  elif joint == MUSCLE_JOINT.SHOULDER:
    d = [29.21]
    return __moment_arm__(d,sFE)

def __triceps_brachii_moment_arm__(joint, angs):
  eFE, sFE = angs
  if joint == MUSCLE_JOINT.ELBOW:
    c = [-23.287, -3.0284e-1, 12.886e-3, -19.092e-5, 13.277e-7, -3.5171e-9]
    return __moment_arm__(c, eFE)
  elif joint == MUSCLE_JOINT.SHOULDER:
    d = [-25.40]
    return __moment_arm__(d, sFE)


def get_muscle_value(muscle, joint_angles, joint=None): #som default er joint=none
  switcher = {
    MUSCLE_NAME.BRACHIALIS: {
      MUSCLE_JOINT.ELBOW: __brachialis_moment_arm__,
      None: __brachialis_length__
    },
    MUSCLE_NAME.BRACHIORADIALIS: {
      MUSCLE_JOINT.ELBOW: __brachioradialis_moment_arm__,
      None: __brachioradialis_length__
    },  
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
      lambda x,y: __raise__("No such joint")
    )

  if joint:
    return func(joint, joint_angles)
  else:
    return func(joint_angles)

if __name__ == '__main__':
  brachialis_len, brachialis_ma_elbow = ([], [])
  brachioradialis_len, brachioradialis_ma_elbow = ([], [])
  biceps_len, biceps_ma_elbow, biceps_ma_shoulder = ([], [], [])
  triceps_len, triceps_ma_elbow, triceps_ma_shoulder = ([], [], [])

  ## biceps
  for a in range(0,140):
    angs = [a,10] # [elbowang, shoulderang] 
    
    brachialis_len.append(get_muscle_value(MUSCLE_NAME.BRACHIALIS, angs))
    brachialis_ma_elbow.append(get_muscle_value(MUSCLE_NAME.BRACHIALIS, angs, MUSCLE_JOINT.ELBOW))
    
    brachioradialis_len.append(get_muscle_value(MUSCLE_NAME.BRACHIORADIALIS, angs))
    brachioradialis_ma_elbow.append(get_muscle_value(MUSCLE_NAME.BRACHIORADIALIS, angs, MUSCLE_JOINT.ELBOW))

    biceps_len.append(get_muscle_value(MUSCLE_NAME.BICEPS_BRACHII, angs))
    biceps_ma_elbow.append(get_muscle_value(MUSCLE_NAME.BICEPS_BRACHII, angs, MUSCLE_JOINT.ELBOW))
    biceps_ma_shoulder.append(get_muscle_value(MUSCLE_NAME.BICEPS_BRACHII, angs, MUSCLE_JOINT.SHOULDER))

    triceps_len.append(get_muscle_value(MUSCLE_NAME.TRICEPS_BRACHII, angs))
    triceps_ma_elbow.append(get_muscle_value(MUSCLE_NAME.TRICEPS_BRACHII, angs, MUSCLE_JOINT.ELBOW))
    triceps_ma_shoulder.append(get_muscle_value(MUSCLE_NAME.TRICEPS_BRACHII, angs, MUSCLE_JOINT.SHOULDER))

  plt.figure(1)
  plt.subplot(3, 1, 1)
  plt.plot(biceps_len)

 # len_file_h = open("bb-len.csv", 'w')
 # len_file_h.write("elbow_angle, len\n")
 # a = range(0,140)
 # for i in range(0, len(biceps_len)):
 #   len_file_h.write(str(a[i]) + ',' + str(biceps_len[i]) + '\n');


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

  plt.figure(3)
  plt.subplot(2, 1, 1)
  plt.plot(brachialis_len)

  plt.subplot(2, 1, 2)
  plt.plot(brachialis_ma_elbow)  

  plt.figure(4)
  plt.subplot(2, 1, 1)
  plt.plot(brachioradialis_len)

  plt.subplot(2, 1, 2)
  plt.plot(brachioradialis_ma_elbow) 
  plt.show()
