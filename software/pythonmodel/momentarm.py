import matplotlib.pyplot as plt
import numpy as np

def MA(par,ang):
  l = len(par)
  ma=0
  for i in range(0,l):
    print(i)
    ma=ma+par[i]*ang**i    
  return ma  

def BB(joint, ang):
  print("Biceps Brachii")
  if joint == "elbow":
    c = [14.660,4.5322e-1,1.8047e-3,-2.9883e-5]
    return MA(c, ang)
  elif joint == "shoulder":
    d = [29.21]
    return MA(d,ang)

def TB(joint, ang):
  print("Triceps Brachii")
  if joint == "elbow":
    c = [-23.287,-3.0284e-1,12.886e-3,-19.092e-5, 13.277e-7,-3.5171e-9]
    return MA(c, ang)
  elif joint == "shoulder":
    d = [-25.40]
    return MA(d,ang)


def muscle_ma(name, ang, joint):
  switcher = {
  'BB': BB,
  'TB': TB,
  }
  func = switcher.get(name, lambda:"nothing")
  return func(joint, ang)

if __name__ == '__main__':
  biceps_len = []
  joint ="elbow"
  for a in range(0,140):
    angs = [0,0,a,10]
    biceps_len.append(muscle_ma('TB',a, joint))
  plt.plot(biceps_len)
  plt.show()