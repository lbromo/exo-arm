import numpy as np
import sympy as sp
import params


class Mech_2_dof_arm():

  def __init__(
      self,
      x0=np.matrix([0,0,0,0]).transpose(),
      I1=params.I1,
      l1=params.l1,
      a1=params.a1,
      m1=params.m1,
      I2=params.I1,
      l2=params.l1,
      a2=params.a2,
      m2=params.m2):
    self.x = x0
    self.I1 = I1
    self.l1 = l1
    self.a1 = a1
    self.m1 = m1
    self.I2 = I2
    self.l2 = l2
    self.a2 = a2
    self.m2 = m2

  def __m_inv__(self):
    pass

  def __generate_m_inv__(self):
    t = sp.Symbol('t')
    g = sp.Symbol('g')
    a1, a2 = sp.symbols("a1 a2")
    l1, l2 = sp.symbols("l1 l2")
    m1, m2 = sp.symbols("m1, m2")
    tau1, tau2 = sp.symbols("tau1 tau2")

    g0 = sp.Matrix([g, 0, 0, 0]).T

    th1 = sp.Function('th1')(t)
    th2 = sp.Function('th2')(t)
    dth1 = sp.Function('dth1')(t)
    dth2 = sp.Function('dth2')(t)
    ddth1 = sp.Function('ddth1')(t)
    ddth2 = sp.Function('ddth2')(t)


    I1_xx, I1_yy, I1_zz = sp.symbols("I1_xx I1_yy I1_zz")
    I2_xx, I2_yy, I2_zz = sp.symbols("I2_xx I2_yy I2_zz")

    # Transformation matrices
    T01 = sp.Matrix([
      [sp.cos(th1), -sp.sin(th1), 0, a1*sp.cos(th1)],
      [sp.sin(th1),  sp.cos(th1), 0, a1*sp.sin(th1)],
      [         0,           0, 1, 0],
      [         0,           0, 0, 1]
    ])

    T12 = sp.Matrix([
      [sp.cos(th2), -sp.sin(th2), 0, a2*sp.cos(th2)],
      [sp.sin(th2),  sp.cos(th2), 0, a2*sp.sin(th2)],
      [         0,           0, 1, 0],
      [         0,           0, 0, 1]
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

    w1 = sp.Matrix([0, 0, sp.diff(th1, t)])
    w2 = sp.Matrix([0, 0, sp.diff(th2, t)])

    # ========= CHANGES TO INERTIA ===================
    w1_0 = w1
    w2_0 = w1_0 + T01[0:3, 0:3]*w2

    I1_0 = I1
    I2_0 = T01[0:3, 0:3] * I2 * T01[0:3, 0:3].T

    k1  = 0.5 * m1 * Vc1.T * Vc1 + 0.5 * w1_0.T * I1_0 * w1_0
    k2  = 0.5 * m2 * Vc2.T * Vc2 + 0.5 * w2_0.T * I2_0 * w2_0

    # The Euler-Lagrange Equation
    L = k1[0]+k2[0] - (u1[0]+u2[0])
    L = L.subs(sp.diff(th1, t), dth1)
    L = L.subs(sp.diff(th2, t), dth2)

    EL1 = sp.diff(sp.diff(L, dth1), t) - sp.diff(L, th1)
    EL2 = sp.diff(sp.diff(L, dth2), t) - sp.diff(L, th2)

    EL1 = EL1.subs(sp.diff(th1, t), dth1)
    EL1 = EL1.subs(sp.diff(th2, t), dth2)
    EL2 = EL2.subs(sp.diff(th1, t), dth1)
    EL2 = EL2.subs(sp.diff(th2, t), dth2)

    EL1 = EL1.subs(sp.diff(dth1, t), ddth1)
    EL1 = EL1.subs(sp.diff(dth2, t), ddth2)
    EL2 = EL2.subs(sp.diff(dth1, t), ddth1)
    EL2 = EL2.subs(sp.diff(dth2, t), ddth2)

    tmp1 = sp.collect(sp.simplify(EL1), [ddth1, ddth2])
    M_1_1 = sp.Add(*[argi for argi in tmp1.args if argi.has(ddth1)])
    M_1_2 = sp.Add(*[argi for argi in tmp1.args if argi.has(ddth2)])

    tmp2 = sp.collect(sp.simplify(EL2), [ddth1, ddth2])
    M_2_1 = sp.Add(*[argi for argi in tmp2.args if argi.has(ddth1)])
    M_2_2 = sp.Add(*[argi for argi in tmp2.args if argi.has(ddth2)])

    M = sp.Matrix([
      [M_1_1, M_1_2],
      [M_2_1, M_2_2]
    ])

    rest = sp.Matrix([
      [(M[0, 0] + M[0, 1]) - EL1],
      [(M[1, 0] + M[1, 1]) - EL2]
    ])


if __name__ == '__main__':
  m = Mech_2_dof_arm()
  m.__generate_m_inv__()
