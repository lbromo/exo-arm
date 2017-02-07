import sympy as sp

import numpy as np
import cloudpickle
import time

import params


class Mech_2_dof_arm():

  CLOUDPICKLE_FILE = 'matrices'

  def __init__(
      self,
      x0=np.array([[0], [0], [0], [0]]),
      ts=0.01,
  ):
    self.x = x0
    self.ts = ts

    self.matrice_parameters = {
      'I1_xx': params.I1[0, 0],
      'I1_yy': params.I1[1, 1],
      'I1_zz': params.I1[2, 2],
      'l1': params.l1,
      'a1': params.a1,
      'm1': params.m1,
      'I2_xx': params.I2[0, 0],
      'I2_yy': params.I2[1, 1],
      'I2_zz': params.I2[2, 2],
      'l2': params.l2,
      'a2': params.a2,
      'm2': params.m2,
      'g': params.g,
      'vm1': params.vm1,
      'vm2': params.vm2,
      'vm1_scale': params.vm1_scale,
      'vm2_scale': params.vm2_scale,
      'cm1': params.cm1,
      'cm2': params.cm2,
      'N': params.N,
      'Im_s': params.Im_shoulder,
      'Im_e': params.Im_elbow

    }

    symbolic_M, symbolic_G, symbolic_V, symbolic_F = self.__get_symbolic_matrices__()
    N = self.matrice_parameters['N']

    Im_s, Im_e = sp.symbols('Im_s Im_e')

    Im = sp.Matrix([
      [Im_s,    0],
      [   0, Im_e]
    ]).subs(self.matrice_parameters)

    # insert constant
    M = symbolic_M.subs(self.matrice_parameters)
    G = symbolic_G.transpose().subs(self.matrice_parameters)
    V = symbolic_V.transpose().subs(self.matrice_parameters)
    F = symbolic_F.subs(self.matrice_parameters)

    ## Convert to functions in the states
    states = sp.symbols('th1 th2 dth1 dth2')

    self.f_M_inv = sp.lambdify(states, (Im * N**2 + M).inv())
    self.f_G = sp.lambdify(states, G, 'numpy')
    self.f_V = sp.lambdify(states, V, 'numpy')
    self.f_F = sp.lambdify(states, F * N**2, 'numpy')

    self.vm1_scale = self.matrice_parameters['vm1_scale']
    self.vm2_scale = self.matrice_parameters['vm2_scale']

  def step(self, u=np.array([0, 0])):
    th1, th2, dth1, dth2 = float(self.x[0]), float(self.x[1]), float(self.x[2]), float(self.x[3])
    dth = np.array([[dth1, dth2]])
    u = np.array([[u[0]], [u[1]]])

    M = self.f_M_inv(th1, th2, dth1, dth2)
    V = self.f_V(th1, th2, dth1, dth2)
    G = self.f_G(th1, th2, dth1, dth2)
    F = self.f_F(th1, th2, dth1, dth2)

    # if dth1 > 0:
    #   F[0] = (1 + self.vm1_scale) * F[0]  # Should maybe be 1 - scale
    # else:
    #   F[0] = (1 - self.vm1_scale) * F[0]  # Should maybe be 1 + scale

    # if dth2 > 0:
    #   F[1] = (1 + self.vm2_scale) * F[1]  # Should maybe be 1 - scale
    # else:
    #   F[1] = (1 - self.vm2_scale) * F[1]  # Should maybe be 1 + scale

    # print(F)

    ddth = M.dot(u - (V + G + F))

    xdot = np.concatenate([dth.flatten(), ddth.flatten()])

    self.x = self.x.flatten() + self.ts * xdot

    return self.x

  def __get_symbolic_matrices__(self):
    try:
      with open(Mech_2_dof_arm.CLOUDPICKLE_FILE, 'rb') as f:
        M, G, V, F = cloudpickle.load(f)
    except Exception as e:
      print(e)
      M, G, V, F = __generate_symbolic_matrices__()
      with open(Mech_2_dof_arm.CLOUDPICKLE_FILE, 'wb') as f:
        cloudpickle.dump((M, G, V, F), f)


    return M, G, V, F

def __generate_symbolic_matrices__():
  t = sp.Symbol('t')
  g = sp.Symbol('g')
  a1, a2 = sp.symbols("a1 a2")
  l1, l2 = sp.symbols("l1 l2")
  m1, m2 = sp.symbols("m1, m2")
  tau1, tau2 = sp.symbols("tau1 tau2")

  g0 = sp.Matrix([g, 0, 0, 0]).T

  th1 = sp.Symbol('th1')
  th2 = sp.Symbol('th2')
  dth1 = sp.Symbol('dth1')
  dth2 = sp.Symbol('dth2')
  ddth1 = sp.Symbol('ddth1')
  ddth2 = sp.Symbol('ddth2')


  I1_xx, I1_yy, I1_zz = sp.symbols("I1_xx I1_yy I1_zz")
  I2_xx, I2_yy, I2_zz = sp.symbols("I2_xx I2_yy I2_zz")

  # Transformation matrices
  T01 = sp.Matrix([
    [sp.cos(th1(t)), -sp.sin(th1(t)), 0, a1*sp.cos(th1(t))],
    [sp.sin(th1(t)),  sp.cos(th1(t)), 0, a1*sp.sin(th1(t))],
    [             0,               0, 1, 0],
    [             0,               0, 0, 1]
  ])

  T12 = sp.Matrix([
    [sp.cos(th2(t)), -sp.sin(th2(t)), 0, a2*sp.cos(th2(t))],
    [sp.sin(th2(t)),  sp.cos(th2(t)), 0, a2*sp.sin(th2(t))],
    [             0,               0, 1, 0],
    [             0    ,           0, 0, 1]
  ])

  # Projections of centres of mass to the 0-frame, {0}
  P1c1 = sp.Matrix([-l1, 0, 0, 1])
  P0c1 = T01*P1c1

  P2c2 = sp.Matrix([-l2, 0, 0, 1])
  P0c2 = T01*T12*P2c2

  # Potential energies
  u1 = -m1*g0*P0c1
  u2 = -m2*g0*P0c2

  # Kinetic energies
  Vc1 = sp.diff(P0c1, t)
  Vc2 = sp.diff(P0c2, t)

  # Beginning of inertia
  I1 = sp.diag(I1_xx, I1_yy, I1_zz)
  I2 = sp.diag(I2_xx, I2_yy, I2_zz)

  w1 = sp.Matrix([0, 0, sp.diff(th1(t), t)])
  w2 = sp.Matrix([0, 0, sp.diff(th2(t), t)])

  # ========= CHANGES TO INERTIA ===================
  w1_0 = w1
  w2_0 = w1_0 + T01[0:3, 0:3]*w2

  I1_0 = T01[0:3, 0:3] * I1 * T01[0:3, 0:3].T
  I2_0 = T01[0:3, 0:3] * T12[0:3, 0:3] * I2 * (T01[0:3, 0:3] * T12[0:3, 0:3]).T

  k1  = 0.5 * m1 * Vc1.T * Vc1 + 0.5 * w1_0.T * I1_0 * w1_0
  k2  = 0.5 * m2 * Vc2.T * Vc2 + 0.5 * w2_0.T * I2_0 * w2_0

  # The Euler-Lagrange Equation
  L = k1+k2 - (u1+u2)
  L = L[0]
  L = L.subs(sp.diff(th1(t), t), dth1(t))
  L = L.subs(sp.diff(th2(t), t), dth2(t))

  EL1 = sp.diff(sp.diff(L, dth1(t)), t) - sp.diff(L, th1(t))
  EL2 = sp.diff(sp.diff(L, dth2(t)), t) - sp.diff(L, th2(t))

  EL1 = EL1.subs(sp.diff(th1(t), t), dth1(t))
  EL1 = EL1.subs(sp.diff(th2(t), t), dth2(t))
  EL2 = EL2.subs(sp.diff(th1(t), t), dth1(t))
  EL2 = EL2.subs(sp.diff(th2(t), t), dth2(t))

  EL1 = EL1.subs(sp.diff(dth1(t), t), ddth1(t))
  EL1 = EL1.subs(sp.diff(dth2(t), t), ddth2(t))
  EL2 = EL2.subs(sp.diff(dth1(t), t), ddth1(t))
  EL2 = EL2.subs(sp.diff(dth2(t), t), ddth2(t))

  EL1 = sp.expand(EL1)
  M_1_1 = sp.Add(*[argi for argi in EL1.args if argi.has(ddth1(t))])
  M_1_2 = sp.Add(*[argi for argi in EL1.args if argi.has(ddth2(t))])

  EL2 = sp.expand(EL2)
  M_2_1 = sp.Add(*[argi for argi in EL2.args if argi.has(ddth1(t))])
  M_2_2 = sp.Add(*[argi for argi in EL2.args if argi.has(ddth2(t))])

  M = sp.Matrix([
    [M_1_1, M_1_2],
    [M_2_1, M_2_2]
  ])

  M = sp.simplify(M)

  G_1 = sp.Add(*[argi for argi in EL1.args if argi.has(g)])
  G_2 = sp.Add(*[argi for argi in EL2.args if argi.has(g)])

  V_1 = sp.Add(*[argi for argi in EL1.args if not argi.has(g) and not argi.has(ddth1(t)) and not argi.has(ddth2(t))]) #G_1 - rest[0]
  V_2 = sp.Add(*[argi for argi in EL2.args if not argi.has(g) and not argi.has(ddth1(t)) and not argi.has(ddth2(t))]) #G_2 - rest[1]

  G = sp.Matrix([G_1, G_2]).T
  V = sp.Matrix([V_1, V_2]).T

  subs = {
    th1(t): th1,
    th2(t): th2,
    dth2(t): dth2,
    dth1(t): dth1,
    ddth1(t): 1,
    ddth2(t): 1,
  }

  G = G.subs(subs)
  V = V.subs(subs)
  M = M.subs(subs)

  ## Friction model
  #vm1, vm2, cm1, cm2 = sp.symbols('vm1 vm2 cm1 cm2')
  cm1, cm2 = sp.symbols('cm1 cm2')  # 0.01, 0.05
  vm1, vm2 = sp.symbols('vm1 vm2')  # 0.00005, 0.00055
  F = sp.Matrix([
    [vm1 * dth1],  # + cm1 * sp.sign(dth1)],
    [vm2 * dth2]   # + cm2 * sp.sign(dth2)]
  ])

  return M, G, V, F


if __name__ == '__main__':
  import matplotlib
  matplotlib.use('GTKAgg')
  import matplotlib.pyplot as plt

# Prepare for simluation
  ts = 0.001
  Tend = int(60 / ts)
  x = np.zeros((4, Tend))
  u = np.zeros((2, Tend))
  u[1, 0:500] = 2

  m = Mech_2_dof_arm(ts=ts)

  fig, ax = plt.subplots(1, 1)
  ax.set_aspect('equal')
  ax.set_xlim(-0.6, 0.6)
  ax.set_ylim(-0.6, 0.6)
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
 
  print(time.time())
  for i in range(Tend-1):
    x[:, i+1] = m.step(u[:, i])
    if i % 20 == 0:
      step_time = time.time()
      line.set_data([0,
                     params.a1 * np.sin(x[0, i+1]),
                     params.a1 * np.sin(x[0, i+1]) + params.a2 * np.sin(x[0, i+1] + x[1, i+1])],
                    [0,
                     -params.a1 * np.cos(x[0, i+1]),
                     -params.a1 * np.cos(x[0, i+1]) - params.a2 * np.cos(x[0, i+1] + x[1, i+1])])
      #fig.canvas.draw()

      fig.canvas.restore_region(background)
      ax.draw_artist(line)
      fig.canvas.blit(ax.bbox)

      time.sleep(20*ts - (time.time() - step_time))

  print(time.time())
  plt.close(fig)

  plt.subplot(3, 1, 1)
  plt.plot(x[0,:])

  plt.subplot(3, 1, 2)
  plt.plot(x[1,:])

  plt.subplot(3, 1, 3)
  plt.plot(u[0,:])
  plt.plot(u[1,:])

  plt.show()
