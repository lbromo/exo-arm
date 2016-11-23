import sympy as sp

import numpy as np
import cloudpickle

import params


class Mech_2_dof_arm():

  CLOUDPICKLE_FILE = 'matrices'

  def __init__(
      self,
      x0=np.array([[0], [0], [0], [0]]),
      ts=0.01,
      I1=params.I1,
      l1=params.l1,
      a1=params.a1,
      m1=params.m1,
      I2=params.I1,
      l2=params.l1,
      a2=params.a2,
      m2=params.m2,
      g=params.g
  ):
    self.x = x0
    self.ts = ts

    self.matrice_parameters = {
      'I1_xx': I1[0, 0],
      'I1_yy': I1[1, 1],
      'I1_zz': I1[2, 2],
      'l1': l1,
      'a1': a1,
      'm1': m1,
      'I2_xx': I1[0, 0],
      'I2_yy': I1[1, 1],
      'I2_zz': I1[2, 2],
      'l2': l2,
      'a2': a2,
      'm2': m2,
      'g': g
    }

    symbolic_M_inv, symbolic_G, symbolic_V, symbolic_F = self.__get_symbolic_matrices__()

    # insert constant
    self.M_inv = symbolic_M_inv.subs(self.matrice_parameters)
    self.G = symbolic_G.transpose().subs(self.matrice_parameters)
    self.V = symbolic_V.transpose().subs(self.matrice_parameters)
    self.F = symbolic_F

    ## Convert to functions in the states
    states = sp.symbols('th1 th2 dth1 dth2')

    self.f_M_inv = sp.lambdify(states, self.M_inv)
    self.f_G = sp.lambdify(states, self.G)
    self.f_V = sp.lambdify(states, self.V)
    self.f_F = sp.lambdify(states, self.F)

  def step(self, u=np.array([[0], [0]])):
    th1, th2, dth1, dth2 = float(self.x[0]), float(self.x[1]), float(self.x[2]), float(self.x[3])
    # print('M:')
    # print(self.f_M_inv(th1, th2, dth1, dth2))
    # print('#'*80)

    # print('G:')
    # print(self.f_G(th1, th2, dth1, dth2))
    # print('#'*80)

    # print('V:')
    # print(self.f_V(th1, th2, dth1, dth2))
    # print('#'*80)

    # print('F:')
    # print(self.f_F(th1, th2, dth1, dth2))
    # print('#'*80)

    ddth = self.f_M_inv(th1, th2, dth1, dth2).dot(u - (self.f_V(th1, th2, dth1, dth2) + self.f_G(th1, th2, dth1, dth2) + self.f_F(th1, th2, dth1, dth2)))

    xdot = np.concatenate((self.x[2:], ddth))

    self.x = self.x + self.ts * xdot

    return self.x

  def __get_symbolic_matrices__(self):
    try:
      with open(Mech_2_dof_arm.CLOUDPICKLE_FILE, 'rb') as f:
        M_inv, G, V, F = cloudpickle.load(f)
    except Exception as e:
      print(e)
      M_inv, G, V, F = __generate_symbolic_matrices__()
      with open(Mech_2_dof_arm.CLOUDPICKLE_FILE, 'wb') as f:
        cloudpickle.dump((M_inv, G, V, F), f)


    return M_inv, G, V, F

def __generate_symbolic_matrices__():
  t = sp.Symbol('t')
  g = sp.Symbol('g')
  a1, a2 = sp.symbols("a1 a2")
  l1, l2 = sp.symbols("l1 l2")
  m1, m2 = sp.symbols("m1, m2")
  tau1, tau2 = sp.symbols("tau1 tau2")

  g0 = sp.Matrix([g, 0, 0, 0]).T

  # th1 = sp.Function('th1')(t)
  # th2 = sp.Function('th2')(t)
  # dth1 = sp.Function('dth1')(t)
  # dth2 = sp.Function('dth2')(t)
  # ddth1 = sp.Function('ddth1')(t)
  # ddth2 = sp.Function('ddth2')(t)

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

  I1_0 = I1
  I2_0 = T01[0:3, 0:3] * I2 * T01[0:3, 0:3].T

  k1  = 0.5 * m1 * Vc1.T * Vc1 + 0.5 * w1_0.T * I1_0 * w1_0
  k2  = 0.5 * m2 * Vc2.T * Vc2 + 0.5 * w2_0.T * I2_0 * w2_0

  # The Euler-Lagrange Equation
  L = k1[0]+k2[0] - (u1[0]+u2[0])
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

  tmp1 = sp.collect(sp.simplify(EL1), [ddth1(t), ddth2(t)])
  M_1_1 = sp.Add(*[argi for argi in tmp1.args if argi.has(ddth1(t))])
  M_1_2 = sp.Add(*[argi for argi in tmp1.args if argi.has(ddth2(t))])

  tmp2 = sp.collect(sp.simplify(EL2), [ddth1(t), ddth2(t)])
  M_2_1 = sp.Add(*[argi for argi in tmp2.args if argi.has(ddth1(t))])
  M_2_2 = sp.Add(*[argi for argi in tmp2.args if argi.has(ddth2(t))])

  M = sp.Matrix([
    [M_1_1, M_1_2],
    [M_2_1, M_2_2]
  ])

  rest = sp.Matrix([
    [(M[0, 0] + M[0, 1]) - EL1],
    [(M[1, 0] + M[1, 1]) - EL2]
  ])

  tmp_G_1 = sp.collect(sp.simplify(-rest[0]), g)
  tmp_G_2 = sp.collect(sp.simplify(-rest[1]), g)
  G_1 = sp.Add(*[argi for argi in tmp_G_1.args if argi.has(g)])
  G_2 = sp.Add(*[argi for argi in tmp_G_2.args if argi.has(g)])

  V_1 = sp.simplify(G_1) + rest[0]
  V_2 = G_2 + rest[1]

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

  G = sp.simplify(G).subs(subs)
  V = sp.simplify(V).subs(subs)
  M_inv = sp.simplify(M.inv()).subs(subs)


  ## Friction model
  #vm1, vm2, cm1, cm2 = sp.symbols('vm1 vm2 cm1 cm2')
  cm1, cm2 = 0.01, 0.05
  vm1, vm2 = 0.00005, 0.00055
  F = sp.Matrix([
    [vm1 * dth1 + cm1 * sp.sign(dth1)],
    [vm2 * dth2 + cm2 * sp.sign(dth2)]
  ])


  return M_inv, G, V, F


if __name__ == '__main__':
  import matplotlib.pyplot as plt
  ts = 0.01
  Tend = int(60 / ts)
  x = np.array([[0], [0], [0], [0]])
  u = np.zeros((2, Tend))
  u[:, 1:100] = 1

  m = Mech_2_dof_arm(x0=x, ts=ts)

  for i in range(Tend):
    tmp = m.step(u[:, i:(i+1)])
    x = np.append(x, tmp, axis=1)

  plt.plot(x[0, :])
  plt.show()
