#include <cstdlib>
#include <cmath>
#include <assert.h>
#include "controller.h"

#if defined (__i386__) || defined (__x86_64__)
#include <iostream>
#endif

using namespace AxoArm;

Vector::Vector(size_t elements){
  this->_values = (float*) malloc(sizeof(float) * elements);
  this->_elements = elements;
}

Vector::~Vector(){
  free(this->_values);
}

float& Vector::operator[] (const int index){
  assert(index >= 0 && index < this->_elements);
  return this->_values[index];
}

Matrix::Matrix(size_t rows, size_t columns){
  this->_values = (float**) malloc(sizeof(float*) * rows);
  for(int i = 0; i < rows; i++){
    this->_values[i] = (float*) malloc(sizeof(float) * columns);
  }

  this->_rows = rows;
  this->_columns = columns;
}

Matrix::~Matrix(){
  for(int i = 0; i < this->_rows; i++){
    free(this->_values[i]);
  }
  free(this->_values);
}

Matrix::Proxy Matrix::operator[] (const int index){
  assert(index >= 0 && index < this->_rows);
  return Proxy(this->_values[index], this->_columns);
}

float& Matrix::Proxy::operator[] (const int index){
  assert(index >= 0 && index < this->_columns);
  return _array[index];
}

std::ostream& AxoArm::operator<< (std::ostream &strm, Matrix& m){
  strm << "[";
  for(int i = 0; i < m.rows; ++i){
    for(int j = 0; j < m.columns; ++j){
      strm << m[i][j];
      if(!(j == m.columns-1)){
        strm << ",";
      }
    }
    strm << "]\n";
    if(!(i == m.rows-1)){
      strm << "[";
    }
  }
  return strm;
}

Vector AxoArm::get_N_vector(Vector& x){
  Vector n(2);

  n[0]= x[2]*4.86725E-1+sin(x[1]+x[0])*1.591091295955199E-1+sin(x[0])*2.173806515142+4.82E2/(exp(x[2]*(-1.9E1/4.0E2))+1.0)-x[3]*sin(x[1])*(x[3]+x[2]*2.0)*5.35229487936E-3-2.41E2;
  n[1] = x[3]*1.101175E-1+sin(x[1]+x[0])*1.5910912959552E-1+(x[2]*x[2])*sin(x[1])*5.35229487936E-3+3.6E1/(exp(x[3]*(-1.299E-1))+1.0)-1.8E1;

  return n;
}

Matrix AxoArm::get_M_matrix(Vector& x){
  Matrix M(2, 2);

  float ths = x[0];
  float the = x[1];
  float dths = x[2];
  float dthe = x[3];

  M[0][0] = cos(x[1])*1.070458975872E-2+4.395832773706053E-1;
  M[0][1] = cos(x[1])*5.352294879359999E-3+1.974569836531137E-3;
  M[1][0] = cos(x[1])*5.352294879359999E-3+1.974569836531137E-3;
  M[1][1] = 1.177245698365311E-1;

  return M;
}

#if defined (__i386__) || defined (__x86_64__)
int main(){
  Vector vect(4);
  Matrix mat(2,2);

  vect[0] = 1;
  vect[1] = 1;

  auto n = get_N_vector(vect);
  auto m = get_M_matrix(vect);
  auto m2 = get_M_matrix(vect);

  std::cout << m << std::endl;

}
#endif
