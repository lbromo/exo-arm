#ifndef _AXO_ARM_UTILS_h_
#define _AXO_ARM_UTILS_h_
#include "Matrix.h"

namespace AxoArm{
  Vector controller(Vector& x, Vector& ref, Matrix& K);
  Vector get_N_vector(Vector& x);
  Matrix get_M_matrix(Vector& x);
}

#endif /* _AXO_ARM_UTILS_h_ */
