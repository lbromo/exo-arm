#! /usr/bin/env python2
from __future__ import division
import numpy as np
import scipy.optimize

import muscle_utils

class Muscle():

  def __init__(self,
               activation_signal,
               muscle_type=muscle_utils.MUSCLE_NAME.BICEPS_BRACHII,
               max_length=404.6,
               optimal_fiber_length=130.7,
               tensor_slack_length=229.8,
               max_force=461.76,
               alpha=0.56,
               Spe=9,
               Sse=2.8,
               phi_m=0.1,
               phi_v=0.5,
               ts=0.01
  ):
    self._activation_signal = activation_signal
    self.muscle_type = muscle_type
    self.Lmax = max_length
    self.Lce0 = optimal_fiber_length
    self.Lts = tensor_slack_length
    self.Fcemax = max_force
    self.alpha = alpha
    self.Spe = Spe
    self.Sse = Sse
    self.phi_m = phi_m
    self.phi_v = phi_v
    self.ts = ts
    self.__prev_dLce__ = None


  def get_force_estimate(self, angles):
    length = self.__get_muscle_length__(angles)
    activation_level = self._activation_signal.get_activation_level()

    return self.__get_force_estimate__(length, activation_level)

  def get_torque_estimate(self, angles, joint):
    F = self.get_force_estimate(angles)

    moment_arm = muscle_utils.get_muscle_value(self.muscle_type, angles, joint)

    return (moment_arm/1000) * F  # /1000 to convert from mm to m

  def __get_muscle_length__(self, angles):
    return muscle_utils.get_muscle_value(self.muscle_type, angles)

  def __get_force_estimate__(self, dLpe, activation_level):
    a = activation_level
    error = False

    bisect_func = lambda dLce, dLpe, a, self: self.__Fse__(dLce, dLpe, a) - self.__Fce__(dLce, dLpe, a)
    try:
      dLce = scipy.optimize.bisect(bisect_func, -2*self.Lmax, 2*self.Lmax, args=(dLpe, a, self), xtol=1e-1) # 0.1 mm tolerence is more then enougth
    except:
      print('Bisection error with length:', self.Lmax)
      error = True

    Ftot = self.__Fpe__(dLpe) + self.__Fce__(dLce, dLpe, a)

    if error:
      print('#'*10)
      print('dLce:', dLce)
      print('a:', a)
      print('Fpe:', self.__Fpe__(dLpe))
      print('Fce:', self.__Fce__(dLce, dLpe, a))

    return Ftot


  def __Fpe__(self, dLpe):
    # PE Element
    # Real-Time Myoprocessors for a Neural Controlled Powered Exoskeleton Arm
    Fpemax = 0.05 * self.Fcemax
    DLpemax = self.Lmax - (self.Lce0 + self.Lts)

    Fpe = Fpemax / (np.exp(self.Spe) - 1) * (np.exp(self.Spe/DLpemax * dLpe) - 1)

    return Fpe

  def __Fse__(self, dLce, dLpe, a):
    dLse = dLpe - dLce

    # SE Element
    # Real-Time Myoprocessors for a Neural Controlled Powered Exoskeleton Arm
    Fsemax = 1.3 * self.Fcemax
    DLsemax = 0.03 * self.Lts

    Fse = Fsemax / (np.exp(self.Sse) - 1) * (np.exp(self.Sse/DLsemax * dLse) - 1)

    return Fse

  def __Fce__(self, dLce, dLpe, a):
    if self.__prev_dLce__ is not None:
      Vce = self.ts * (dLce - self.__prev_dLce__)
    else:
      Vce = 0

    # CE Element
    # Real-Time Myoprocessors for a Neural Controlled Powered Exoskeleton Arm
    Vcemax = 2 * self.Lce0 + 8 * self.Lce0 * self.alpha
    Vce0 = 1/2 * (a + 1) * Vcemax

    fl = np.exp(-1/2 * ((dLce/self.Lce0 - self.phi_m) / self.phi_v) ** 2)
    fv = 0.1433 / (0.1074 + np.exp(-1.3 * np.sinh(2.8 * Vce / Vce0 + 1.64)))
    Fce = a * fl * fv * self.Fcemax

    return Fce


if __name__ == '__main__':
  import matplotlib.pyplot as plt
  from activation_signal import MockActicationSignal

  activation_level = 1
  activation_signal = MockActicationSignal(activation_level)

  m = Muscle(activation_signal)

  F, tau, length = [], [], []
  for a in range(0,140):
    angs = [a,0]
    length.append(m.__get_muscle_length__(angs))
    F.append(m.get_force_estimate(angs))
    tau.append(m.get_torque_estimate(angs, muscle_utils.MUSCLE_JOINT.ELBOW))

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
