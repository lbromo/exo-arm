#include "Matrix"

namepsace AxoArm{
  Vector controller(Vector& x, Vector& ref, Matrix& K);
  Vector get_N_vector(Vector& x);
  Matrix get_M_matrix(Vector& x);
}
