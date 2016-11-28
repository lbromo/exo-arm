#! /usr/bin/env python3
import numpy as np

import muscle_utils

class Muscle():

  def __init__(self,
               muscle_type=muscle_utils.MUSCLE_NAME.BICEPS_BRACHII,
               max_length=404.6,
               optimal_fiber_length=130.7,
               tensor_slack_length=229.8,
               max_force=461.76,
               alpha=0.56,
               spe=9,
               phi_m=0.1,
               phi_v=0.5):
    self.muscle_type = muscle_type
    self.Lmax = max_length
    self.Lce0 = optimal_fiber_length
    self.Lts = tensor_slack_length
    self.Fcemax = max_force
    self.alpha = alpha
    self.spe = spe
    self.phi_m = phi_m
    self.phi_v = phi_v
    self.__prev_len__ = None


  def get_force_estimate(self, angles, activation_level):
    length = self.__get_muscle_length__(angles)
    if self.__prev_len__:
      velocity = length - self.__prev_len__
    else:
      velocity = 0

    self.__prev_len__ = length

    # length - magic constant from utils (ask Morten why)
    return self.__get_force_estimate__(length - 378.06, velocity, activation_level)

  def get_torque_estimate(self, angles, activation_level, joint):
    F = self.get_force_estimate(angles, activation_level)
    moment_arm = muscle_utils.get_muscle_value(self.muscle_type, angles[2], joint) # HACK
    return moment_arm/1000 * F

  def __get_muscle_length__(self, angles):
    return muscle_utils.get_muscle_value(self.muscle_type, angles)

  def __get_force_estimate__(self, length, velocity, activation_level):
    a = activation_level
    # CE Element
    # Real-Time Myoprocessors for a Neural Controlled Powered Exoskeleton Arm
    Vcemax = 2 * self.Lce0 + 8 * self.Lce0 * self.alpha
    Vce0 = 1/2 * (a + 1) * Vcemax

    fl = np.exp(-1/2 * ((length/self.Lce0 - self.phi_m) / self.phi_v) ** 2)
    fv = 0.1433 / (0.1074 + np.exp(-1.3 * np.sinh(2.8 * velocity / Vce0 + 1.64)))
    Fce = a * fl * fv * self.Fcemax

    # PE Element
    # Real-Time Myoprocessors for a Neural Controlled Powered Exoskeleton Arm
    Fpemax = 0.05 * self.Fcemax
    DLpemax = self.Lmax - (self.Lce0 + self.Lts)

    Fpe = Fpemax / (np.exp(self.spe) - 1) * (np.exp(self.spe/DLpemax * length) - 1)

    Ftot = Fce + Fpe

    return Ftot


if __name__ == '__main__':
  import matplotlib.pyplot as plt

  F, tau = ([], [])
  m = Muscle()
  activation_level = 1

  length = []

  for a in range(0,140):
    angs = [0,0,a,0]
    length.append(m.__get_muscle_length__(angs))
    F.append(m.get_force_estimate(angs, activation_level))
    tau.append(m.get_torque_estimate(angs, activation_level, muscle_utils.MUSCLE_JOINT.ELBOW))

  plt.figure(1)

  plt.subplot(2, 1, 1)
  plt.plot(length, F, 'x')
  plt.grid()
  plt.title('Force - Length relationship')
  plt.xlabel('Length [mm]')
  plt.ylabel('Force [N]')

  plt.subplot(2, 1, 2)
  plt.plot(tau, 'x')
  plt.grid()
  plt.title('Torque - Angle relationship')
  plt.xlabel('Angle')
  plt.ylabel('tau [Nm]')

  plt.show()
