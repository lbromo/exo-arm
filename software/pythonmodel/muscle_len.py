import matplotlib.pyplot as plt
import numpy as np

def ML(cst,r,s,t,u,angs):
  wRU, wFE, eFE, sFE = angs
  l = cst + r[1] * wRU**2 + r[0] * wRU**1 + \
  s[3] * wFE**4 + s[2] * wFE**3 + s[1] * wFE**2 + s[0] * wFE + \
  t[5] * eFE**6 + t[4] * eFE**5 + t[3] * eFE**4 + t[2] * eFE**3 + t[1] * eFE**2 + t[0] * eFE + \
  u[0] * sFE;
  return l

def BB(angs):
  cst = 378.06
  r = [0, 0]
  s = [0, 0, 0, 0]
  t = [-25.587e-2, -7.9101e-3, -3.1498e-5, 5.2156e-7, 0, 0]
  u = [-5.0981e-1]
  return ML(cst,r,s,t,u,angs)

def TB(angs):
  cst = 260.05
  r = [0, 0]
  s = [0, 0, 0, 0]
  t = [40.644e-2, 5.2856e-3, -22.491e-5, 33.321e-7, -2.3174e-8, 6.1385e-11]
  u = [-4.4331e-1]
  return ML(cst,r,s,t,u,angs)


def muscle_len(name, angs):
  switcher = {
  'BB': BB,
  'TB': TB,
  }
  func = switcher.get(name, lambda x: (_ for _ in ()).throw(Exception("No such muscle")))
  return func(angs)

if __name__ == '__main__':
  biceps_len = []
  for a in range(0,140):
    angs = [0,0,a,10]
    biceps_len.append(muscle_len('BB',angs))
  plt.plot(biceps_len)
  plt.show()
