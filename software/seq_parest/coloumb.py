import serial
import parest as pe
import time
import numpy as np

PORT = '/dev/ttyACM0'
BAUD = 115200

OFFSET = 0.5

if __name__ == '__main__':
  ser = serial.Serial(PORT, BAUD, timeout=0)
  if not ser.isOpen():
    ser.Open()

  time.sleep(2)

  cur = np.array([0.01])

  pwm1 = int(pe.cur_pwm(cur, 2))

  on1 = 1
  dir1 = 1

  on2 = 0
  dir2 = 0
  pwm2 = 0



  time.sleep(2)


  try:
    while True:
      input("Current:" + str(cur + OFFSET) + " A \nPress Enter to continue...")
      pwm1 = int(pe.cur_pwm(cur, 2))
      print(pwm1)
      out = pe.parseMsg(on1, dir1, pwm1, on2, dir2, pwm2)
      ser.write(out)
      cur = cur + 0.1
      dir1 = not dir1
  except:
    out = pe.parseMsg(0, 0, pe.PWM_MIN, 0, 0, pe.PWM_MIN)
    ser.write(out)
    exit()

    # RESULT:
    # 0.55 A