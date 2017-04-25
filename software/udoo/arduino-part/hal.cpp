#include "hal.h"

float AxoArm::getPos(int joint) {

  // if (joint == SHOULDER) {
  //   return analogRead(pin_pos_shoulder) * -0.001681795 + 3.1331837;
  // }
  // else if (joint == ELBOW) {
  //   return analogRead(pin_pos_elbow) * -0.00165696 + 3.4945247;
  // }
  // else {
  //   return 0;
  // }
  int a_r;
  float ang_rad;
  if (joint == SHOULDER) {
    a_r = analogRead(pin_pos_shoulder);
    if(a_r < MAGIC_VOLTAGE){
      a_r += MAGIC_OFFSET;
    }
    ang_rad = map(a_r, 5808, 3817, MIN_RAD, MAX_RAD);
    // return analogRead(pin_pos_shoulder) * -0.001681795 + 3.1331837;
  }
  else if (joint == ELBOW) {
    return analogRead(pin_pos_elbow) * -0.00165696 + 3.4945247;
  }
  else {
    return 0;
  }

}

float AxoArm::getCur(int joint) {

  int reading;

  if (joint == SHOULDER) {
    // return (analogRead(pin_cur1) * 0.0014652 - 3.1414);
    reading = analogRead(pin_cur_shoulder);
    return ((reading - 2144) * 0.0014652);
  }
  else if (joint == ELBOW) {
    // return (analogRead(pin_cur2) * 0.0004884 - 1.0471);
    reading = analogRead(pin_cur_elbow);
    return ((reading - 2144) * 0.0004884);
  }
  else {
    return -1;
  }
}

float AxoArm::getVel(int joint) {
  int reading;

  if (joint == SHOULDER) {
    // return (analogRead(pin_vel1) * 0.153398 - 328.8852);
    reading = analogRead(pin_vel_shoulder);
    return (((reading - 2144) * 0.153398) * 0.02); // 0.02 is due to gear ratio
  }
  else if (joint == ELBOW) {
    // return (analogRead(pin_vel2) * 0.153398 - 328.8852);
    reading = analogRead(pin_vel_elbow);
    return (((reading - 2144) * 0.153398) * 0.02);
  }
  else {
    return -1;
  }
}

int AxoArm::cur2pwm(int joint, float cur) {

  int pwm = 0;

  if (joint == SHOULDER) {
    pwm = (int)(fabs(cur) * (PWM_MAX - PWM_MIN) / 3.0);
  }
  else if (joint == ELBOW) {
    pwm = (int)(fabs(cur) * (PWM_MAX - PWM_MIN) / 1.0);
  }

  pwm += PWM_MIN;

  if (pwm > PWM_MAX) {
    pwm = PWM_MAX;
  } else if (pwm < PWM_MIN) {
    pwm = PWM_MIN;
  }

  return pwm;

}

int AxoArm::getDir(float u) {

  return (int)(u > 0);
}
