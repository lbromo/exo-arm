#!/usr/bin/env python

import numpy as np


class PSO(object):
  def __init__(
      self, objective, dimensions,
      particles=100,
      w=0.5, phi_p=0.75, phi_g=1,
      lower_bound=None, upper_bound=None
  ):
    self.objective = objective
    self.particles = particles
    self.dimensions = dimensions
    self.w = 0.5
    self.phi_p = phi_p
    self.phi_g = phi_g
    self.lower = lower_bound
    self.upper = upper_bound

  def add_limits(self, lower_bound, upper_bound):
    self.lower = lower_bound
    self.upper = upper_bound


  def optimize(self, inputs, outputs, rho=1, max_iter=100):
    x, v, p = self.__init_particeles__()
    g = [-1] * self.dimensions

    g_best = np.inf
    p_best = np.ones((self.particles, self.dimensions)) * np.inf

    for i in range(self.particles):
      p_best = self.objective(inputs, outputs, *x[i,:])

      if p_best < g_best:
        g_best = p_best
        g = x[i,:]

    n = 0
    while g_best > rho and max_iter > n:
      for i in range(self.particles):
        for d in range(self.dimensions):
          rp = np.random.rand()
          rg = np.random.rand()
          v[i,d] = self.w * v[i,d] + self.phi_p * rp * (p[i,d] - x[i,d]) + self.phi_g * rg * (g[d] - x[i,d])

        xnew = x[i,:] + v[i,:]
        fitness = self.objective(inputs, outputs, *xnew)
        p_best = self.objective(inputs, outputs, *p[i,:])

        if any(self.lower < xnew) or any(xnew > self.upper):
          fitness = 2*fitness

        if fitness < p_best:
          p[i,:] = xnew
          if fitness < g_best:
            g = xnew
            g_best = fitness

        x[i,:] = xnew

      n = n + 1

    g = tuple(g)
    ret = g + (g_best, x, p)
    return ret


  def __init_particeles__(self):
    if not self.lower:
      self.lower = [-1000] * self.dimensions
    if not self.upper:
      self.upper = [1000] * self.dimensions

    x_max = [u - l for u, l in zip(self.upper, self.lower)]
    v_max = [u + abs(l) if l < 0 else u - l for u, l in zip(self.upper, self.lower)]

    x = self.lower + np.random.rand(self.particles, self.dimensions) * x_max
    v = self.lower + np.random.rand(self.particles, self.dimensions) * v_max
    p = self.lower + np.random.rand(self.particles, self.dimensions) * x_max

    return x, v, p

if __name__ == '__main__':
  import matplotlib.pyplot as plt

  ## Define objective funcion
  objective = lambda x, meas, a, b: (((a*x + b) - meas)**2).mean()

  ## Generate test data
  x = np.linspace(-10,10,20)
  y = 4*x + 42

  ## initialize PSO
  pso = PSO(objective, dimensions=2, particles=50, w=1.8, phi_p=0.75, phi_g=1)
  pso.add_limits([0, 25], [10, 75])

  ## Optimize
  a, b, best_cost, particles, personal_best = pso.optimize(x, y, rho=0.01, max_iter=10000)

  ## Show results
  y_est = a*x + b
  plt.subplot(2,1,1)
  plt.plot(x,y)
  plt.plot(x, y_est, 'x')
  plt.title('Esimated results')
  plt.legend(['"Real" data', 'Estimated'])

  plt.subplot(2,1,2)
  plt.plot(particles[:,0], particles[:,1], 'x')
  plt.plot(personal_best[:,0], personal_best[:,1], 'x')
  plt.plot(a, b, 'o')
  plt.title('Particle Swarn')
  plt.legend(['Latests Locations', 'Personal Best', 'Global Best'])

  plt.show()
