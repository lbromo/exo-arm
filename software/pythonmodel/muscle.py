#! /usr/bin/env python3
import numpy as np
from enum import Enum

import muscle_len as utils

class Muscle():

  def __init__(self,
               muscle_type='BB',  # MUSCLE_TYPES.Biceps_Brachii,
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
    print(velocity)

    # length - magic constant from utils (ask Morten why)
    return self.__get_force_estimate__(length - 378.06, velocity, activation_level)

  def __get_muscle_length__(self, angles):
    return utils.muscle_len(self.muscle_type, angles)

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

  F = []
  m = Muscle()

  length = []

  for a in range(0,180):
    angs = [0,0,a,0]
    length.append(m.__get_muscle_length__(angs))
    F.append(m.get_force_estimate(angs, 1))

  plt.plot(length, F, 'x')
  plt.show()
