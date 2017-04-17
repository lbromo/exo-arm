#if defined (__i386__) || defined (__x86_64__) || defined (__arm__)
#include <cmath>
#elif defined (ARDUINO)
#include <math.h>
#endif

#include "Matrix.h"
#include "AxoArmUtils.h"

using namespace AxoArm;

Vector AxoArm::get_N_vector(Vector& x){
  Vector n(2);

  // n[0]= x[2]*4.86725E-1+sin(x[1]+x[0])*1.591091295955199E-1+sin(x[0])*2.173806515142+4.82E2/(exp(x[2]*(-1.9E1/4.0E2))+1.0)-x[3]*sin(x[1])*(x[3]+x[2]*2.0)*5.35229487936E-3-2.41E2;
  // n[1] = x[3]*1.101175E-1+sin(x[1]+x[0])*1.5910912959552E-1+(x[2]*x[2])*sin(x[1])*5.35229487936E-3+3.6E1/(exp(x[3]*(-1.299E-1))+1.0)-1.8E1;

  // NEW n VECTOR!
  n[0] = x[2]*4.86725E-1+sin(x[0]+x[1])*1.591091295955199E-1+sin(x[0])*2.173806515142+(2.41E2/2.5E1)/(exp(x[2]*(-1.9E1/8.0))+1.0)-x[3]*sin(x[1])*(x[2]*2.0+x[3])*5.35229487936E-3-2.41E2/5.0E1;
  n[1] = x[3]*1.101175E-1+sin(x[0]+x[1])*1.5910912959552E-1+(x[2]*x[2])*sin(x[1])*5.35229487936E-3+(1.8E1/2.5E1)/(exp(x[3]*(-6.495))+1.0)-9.0/2.5E1;

  return n;
}



Matrix AxoArm::get_M_matrix(Vector& x){
  Matrix M(2, 2);

  M[0][0] = cos(x[1])*1.070458975872E-2+4.395832773706053E-1;
  M[0][1] = cos(x[1])*5.352294879359999E-3+1.974569836531137E-3;
  M[1][0] = cos(x[1])*5.352294879359999E-3+1.974569836531137E-3;
  M[1][1] = 1.177245698365311E-1;

  return M;
}

Vector AxoArm::controller(Vector& x, Vector& ref, Matrix& K){
  Vector u; /* Output vector */
  
  auto n = get_N_vector(x);
  auto M = get_M_matrix(x);

  auto e = ref - x;
  auto tmp1 = K * e;
  auto tmp2 = M * tmp1;
  u = tmp2 + n;

/*  u = M * K * e + n; */
  
  return u;
}


float AxoArm::getPos(int joint) {

  if (joint == SHOULDER) {
    return analogRead(pin_pos_shoulder) * -0.001681795 + 3.1331837;
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

#if defined (__i386__) || defined (__x86_64__)
int main(){
  Vector x(4);
  Vector r(4);
  Matrix K(2,4);

  Matrix M(4,4);
  M[0][0] = 2;
  M[1][1] = 2;
  M[2][2] = 2;
  M[3][3] = 2;

  r[0] = 1.67;
  r[1] = 2.36;

  K[0][0] = 12;
  K[0][2] = 3.5;
  K[1][1] = 12;
  K[1][3] = 3.5;

  auto u = controller(x, r, K);
  std::cout << u << std::endl;

  u = controller(x, r, K);
  std::cout << u << std::endl;

  std::cout << M << std::endl;

  M = (M * M) * M - M * (float)0.33;

  std::cout << M << std::endl;
  
}
#endif
