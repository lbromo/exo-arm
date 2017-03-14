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

Vector::Vector(const Vector& other){
  if(!(this == &other)){
    /* Free all the "old" buffers */
    this->~Vector();

    /* Allocate new memory*/
    new (this) Vector(other.elements);

    /* Copy the content */
    for(int i = 0; i < this->elements; i++){
      (*this)[i] = other[i];
    }
  }
}

Vector::~Vector(){
  free(this->_values);
}

Vector& Vector::operator= (const Vector& other){
  if (!(this == &other)){
    new (this) Vector(other);
  }
  return *this;
}

float& Vector::operator[] (const int index) const{
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

Matrix::Proxy Matrix::operator[] (const int index) const{
  assert(index >= 0 && index < this->_rows);
  return Proxy(this->_values[index], this->_columns);
}

float& Matrix::Proxy::operator[] (const int index) const{
  assert(index >= 0 && index < this->_columns);
  return _array[index];
}

/**
 * Matrix Math
 */
Matrix Matrix::operator+ (const Matrix& other) const{
  assert(this->rows == other.rows);
  assert(this->columns == other.columns);
  auto m = this->rows;
  auto n = this->columns;
  Matrix C(m, n);

  for(int row = 0; row < m; row++){
    for(int col = 0; col < n; col++){
      C[row][col] = (*this)[row][col] + other[row][col];
    }
  }
  return C;
}


Matrix Matrix::operator- (const Matrix& other) const{
  assert(this->rows == other.rows);
  assert(this->columns == other.columns);
  auto m = this->rows;
  auto n = this->columns;
  Matrix C(m, n);

  for(int row = 0; row < m; row++){
    for(int col = 0; col < n; col++){
      C[row][col] = (*this)[row][col] - other[row][col];
    }
  }
  return C;
}

Matrix Matrix::operator* (const Matrix& other) const{
  assert(this->columns == other.rows);
  auto m = this->rows;
  auto p = this->columns;
  auto n = other.columns;

  Matrix C(m, n);

  for(int row = 0; row < m; row++){
    for(int col = 0; col < n; col++){
      for(int inner = 0; inner < p; inner++){
        C[row][col] += (*this)[row][inner] * other[inner][col];
      }
    }
  }
  return C;
}

Matrix Matrix::operator* (const int scalar) const{
  auto m = this->rows;
  auto n = this->columns;

  Matrix C(m, n);

  for(int row = 0; row < m; row++){
    for(int col = 0; col < n; col++){
      C[row][col] = (*this)[row][col] * scalar;
    }
  }
  return C;
}

Matrix Matrix::operator* (const float scalar) const{
  auto m = this->rows;
  auto n = this->columns;

  Matrix C(m, n);

  for(int row = 0; row < m; row++){
    for(int col = 0; col < n; col++){
      C[row][col] = (*this)[row][col] * scalar;
    }
  }
  return C;
}

/**
 * Matrix Vector product
 */
Vector Matrix::operator* (const Vector& v) const{
  assert(this->columns == v.elements);

  Matrix m2(v.elements, 1);
  Vector res(this->rows);

  for(int i = 0; i < v.elements; i++)
    m2[i][0] = v[i];
  auto C = (*this) * m2;

  for(int i = 0; i < this->rows; i++){
    res[i] = C[i][0];
  }

  return res;
}


/**
 * Vector Math
 */
Vector Vector::operator+ (const Vector& other) const{
  assert(this->elements == other.elements);
  Vector v(this->elements);
  for(int i = 0; i < this->elements; i++){
    v[i] = (*this)[i] + other[i];
  }

  return v;
}

Vector Vector::operator- (const Vector& other) const{
  assert(this->elements == other.elements);
  Vector v(this->elements);
  for(int i = 0; i < this->elements; i++){
    v[i] = (*this)[i] - other[i];
  }
  return v;
}

float Vector::operator* (const Vector& other) const{
  assert(this->elements == other.elements);
  float val = 0;
  for(int i = 0; i < this->elements; i++){
    val += (*this)[i]*other[i];
  }
  return val;
}

Vector Vector::operator* (const int scalar) const{
  Vector v(this->elements);

  for(int i = 0; i < this->elements; i++){
    v[i] = (*this)[i] * scalar;
  }
  return v;
}

Vector Vector::operator* (const float scalar) const{
  Vector v(this->elements);

  for(int i = 0; i < this->elements; i++){
    v[i] = (*this)[i] * scalar;
  }

  return v;
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
