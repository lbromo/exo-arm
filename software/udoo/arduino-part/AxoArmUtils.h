#pragma once

#include "Matrix.h"

namespace AxoArm{
  Vector controller(Vector& x, Vector& ref, Matrix& K);
  Vector get_N_vector(Vector& x);
  Matrix get_M_matrix(Vector& x);
}
