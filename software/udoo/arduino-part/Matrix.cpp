#include <assert.h>
#include "Matrix.h"

#if defined (__i386__) || defined (__x86_64__)
#include <cstdlib>
#include <iostream>
#endif /*  (__i386__) || (__x86_64__) */

using namespace AxoArm;

/**
 * Vector implementation
 */
Vector::Vector(size_t elements){
  this->_values = (float*) calloc(elements, sizeof(float));
  this->_elements = elements;
}

Vector::~Vector(){
  free(this->_values);
}

float& Vector::operator[] (const int index){
  assert(index >= 0 && index < this->_elements);
  return this->_values[index];
}

/**
 * Matrix implementation
 */
Matrix::Matrix(size_t rows, size_t columns){
  this->_values = (float**) calloc(rows, sizeof(float*));
  for(int i = 0; i < rows; i++){
    this->_values[i] = (float*) calloc(columns, sizeof(float));
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

/**
 * Matrix Math
 */
Matrix AxoArm::operator+ (Matrix& m1, Matrix& m2){
  assert(m1.rows == m2.rows);
  assert(m1.columns == m2.columns);
  auto m = m1.rows;
  auto n = m1.columns;
  Matrix C(m, n);

  for(int row = 0; row < m; row++){
    for(int col = 0; col < n; col++){
      C[row][col] = m1[row][col] + m2[row][col];
    }
  }
  return C;
}

Matrix AxoArm::operator- (Matrix& m1, Matrix& m2){
  assert(m1.rows == m2.rows);
  assert(m1.columns == m2.columns);
  auto m = m1.rows;
  auto n = m1.columns;
  Matrix C(m, n);

  for(int row = 0; row < m; row++){
    for(int col = 0; col < n; col++){
      C[row][col] = m1[row][col] - m2[row][col];
    }
  }
  return C;
}

Matrix AxoArm::operator* (Matrix& m1, Matrix& m2){
  assert(m1.columns == m2.rows);
  auto m = m1.rows;
  auto p = m2.rows;
  auto n = m2.columns;
  Matrix C(m, n);

  for(int row = 0; row < m; row++){
    for(int col = 0; col < n; col++){
      for(int inner = 0; inner < p; inner++){
        C[row][col] += m1[row][inner] * m2[inner][col];
      }
    }
  }
  return C;
}

Matrix operator* (Matrix& m1, int scalar){
  auto m = m1.rows;
  auto n = m1.columns;

  Matrix C(m, n);

  for(int row = 0; row < m; row++){
    for(int col = 0; col < n; col++){
      C[row][col] = m1[row][col] * scalar;
    }
  }
  return C;
}

Matrix operator* (Matrix& m1, double scalar){
  auto m = m1.rows;
  auto n = m1.columns;

  Matrix C(m, n);

  for(int row = 0; row < m; row++){
    for(int col = 0; col < n; col++){
      C[row][col] = m1[row][col] * scalar;
    }
  }
  return C;
}

/**
 * Vector Math
 */
Vector AxoArm::operator+ (Vector& v1, Vector& v2){
  assert(v1.elements == v2.elements);
  Vector v(v1.elements);
  for(int i = 0; i < v1.elements; i++){
    v[i] = v1[i] + v2[i];
  }
  return v;
}

Vector AxoArm::operator- (Vector& v1, Vector& v2){
  assert(v1.elements == v2.elements);
  Vector v(v1.elements);
  for(int i = 0; i < v1.elements; i++){
    v[i] = v1[i] - v2[i];
  }
  return v;
}

float AxoArm::operator* (Vector& v1, Vector& v2){
  assert(v1.elements == v2.elements);
  float val = 0;
  for(int i = 0; i < v1.elements; i++){
    val += v1[i]*v2[i];
  }
  return val;
}

Vector AxoArm::operator* (Vector& v1, int scalar){
  Vector v(v1.elements);
  for(int i = 0; i < v1.elements; i++){
    v[i] = v1[i] * scalar;
  }
  return v;
}

Vector AxoArm::operator* (Vector& v1, double scalar){
  Vector v(v1.elements);
  for(int i = 0; i < v1.elements; i++){
    v[i] = v1[i] * scalar;
  }
  return v;
}


/**
 * Matrix Vector product
 */
Vector AxoArm::operator* (Matrix& m1, Vector& v){
  assert(m1.columns == v.elements);
  Matrix m2(v.elements, 1);
  Vector res(m1.rows);
  for(int i = 0; i < v.elements; i++)
    m2[i][0] = v[i];
  auto C = m1 * m2;

  for(int i = 0; i < m1.rows; i++){
    res[i] = C[i][0];
  }
  return res;
}

#if defined (__i386__) || defined (__x86_64__)

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

std::ostream& AxoArm::operator<< (std::ostream &strm, Vector& v){

  for(int i = 0; i < v.elements; i++){
    strm << "[" << v[i] << "]";
    if(!(i == v.elements - 1))
      strm << "\n";
  }

  return strm;
}
#endif
