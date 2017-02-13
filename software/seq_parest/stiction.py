import serial
import parest as pe
import time

PORT = '/dev/ttyACM0'
BAUD = 115200

OFFSET = 1

if __name__ == '__main__':
  ser = serial.Serial(PORT, BAUD, timeout=0)
  if not ser.isOpen():
    ser.Open()

  time.sleep(2)

  pwm1 = pe.PWM_MIN

  on1 = 1
  dir1 = 1

  on2 = 0
  dir2 = 0
  pwm2 = 0



  time.sleep(2)


  try:
    while True:

      out = pe.parseMsg(on1, dir1, pwm1, on2, dir2, pwm2)
      print(pwm1)
      ser.write(out)

      input("Current:" + str(((pwm1-pe.PWM_MIN) * 0.0043) + OFFSET ) + " A \nPress Enter to continue...")
      pwm1 = pwm1 + 5
  except:
    out = pe.parseMsg(0, 0, pe.PWM_MIN, 0, 0, pe.PWM_MIN)
    ser.write(out)
    exit()

    # RESULT:
    # 0.55 A