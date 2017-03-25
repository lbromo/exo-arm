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
