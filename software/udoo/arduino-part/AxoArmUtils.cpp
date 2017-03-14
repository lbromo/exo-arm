#if defined (__i386__) || defined (__x86_64__)
#include <cmath>
#elif defined (ARDUINO)
#include <math.h>
#endif

#include "Matrix.h"
#include "AxoArmUtils.h"

using namespace AxoArm;

Vector AxoArm::get_N_vector(Vector& x){
  Vector n(2);

  n[0]= x[2]*4.86725E-1+sin(x[1]+x[0])*1.591091295955199E-1+sin(x[0])*2.173806515142+4.82E2/(exp(x[2]*(-1.9E1/4.0E2))+1.0)-x[3]*sin(x[1])*(x[3]+x[2]*2.0)*5.35229487936E-3-2.41E2;
  n[1] = x[3]*1.101175E-1+sin(x[1]+x[0])*1.5910912959552E-1+(x[2]*x[2])*sin(x[1])*5.35229487936E-3+3.6E1/(exp(x[3]*(-1.299E-1))+1.0)-1.8E1;

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
  auto n = get_N_vector(x);
  auto M = get_M_matrix(x);

  auto e = ref - x;
  auto K_tmp = K * e;
  auto M_tmp = M * K_tmp;
  auto u = M_tmp + n;

  u[0] = u[0] * 0.282485875706215;
  u[1] = u[1] * 0.261780104712042;

  return u;
}


#if defined (__i386__) || defined (__x86_64__)
int main(){
  Vector x(4);
  Vector r(4);
  Matrix K(2,4);

  r[0] = 1.67;
  r[1] = 2.36;

  K[0][0] = 12;
  K[0][2] = 3.5;
  K[1][1] = 12;
  K[1][3] = 3.5;

  auto u = controller(x, r, K);
  std::cout << u << std::endl;

}
#endif
