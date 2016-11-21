#! /usr/bin/env python3
import numpy as np


class Muscle():

  def __init__(self,
               max_length=404.6,
               optimal_fiber_length=130.7,
               tensor_slack_length=229.8,
               max_force=461.76,
               alpha=0.56,
               spe=9,
               phi_m=0.1,
               phi_v=0.5):
    self.Lmax = max_length
    self.Lce0 = optimal_fiber_length
    self.Lts = tensor_slack_length
    self.Fcemax = max_force
    self.alpha = alpha
    self.spe = spe
    self.phi_m = phi_m
    self.phi_v = phi_v

  def get_force_estimate(self, length, velocity, activation_level):
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

  length = np.linspace(-250, 55, 305)
  for l in length:
    F.append(m.get_force_estimate(l, 1, 1))

  plt.plot(length, F)
  plt.show()
