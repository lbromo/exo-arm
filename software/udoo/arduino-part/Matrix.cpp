#include <assert.h>
#include "Matrix.h"

#ifdef __arm__
#include <new>
#endif /*  (__i386__) || (__x86_64__) */

using namespace AxoArm;

/**
 * Allocate memory the vector
 */

void Vector::_allocate(size_t elements){
  this->_values = (float*) calloc(elements, sizeof(float));
  this->_elements = elements;
}

void Vector::_copy(const Vector& other){
  for(int i = 0; i < this->elements; i++){
    (*this)[i] = other[i];
  }
}


Vector::Vector(size_t elements){
  this->_allocate(elements);
}

/**
 * Copy constructor
 * Copies all the data from "other" into a new vector
 */
Vector::Vector(const Vector& other){
  if(!(this == &other)){
    /* Allocate new memory*/
    /* New syntax -- doesn't work with AVR-GCC */
    //new (this) Vector(other.elements);
    this->_allocate(other.elements);

    /* Copy the content */
    this->_copy(other);

  }
}

/**
 * Free the memory on destruction
 */
Vector::~Vector(){
  if(elements){
    free(this->_values);
  }
}

/**
 * The assignment operator invokes the copy constructor and returns a reference to the copied vector
 */
Vector& Vector::operator= (const Vector& other){
  if (!(this == &other)){
    this->~Vector();

    this->_allocate(other.elements);
    this->_copy(other);

  }
  return *this;
}

/**
 * We want to be able to index with v[0], v[i] ... v[v.elements - 1]
 */
float& Vector::operator[] (const int index) const{
  assert(index >= 0 && index < this->_elements);
  return this->_values[index];
}

/**
 * Vector addition
 */
Vector Vector::operator+ (const Vector& other) const{
  assert(this->elements == other.elements);
  Vector v(this->elements);
  for(int i = 0; i < this->elements; i++){
    v[i] = (*this)[i] + other[i];
  }

  return v;
}

/**
 * Vector subtraction
 */
Vector Vector::operator- (const Vector& other) const{
  assert(this->elements == other.elements);
  Vector v(this->elements);
  for(int i = 0; i < this->elements; i++){
    v[i] = (*this)[i] - other[i];
  }
  return v;
}

/**
 * dot product
 */
float Vector::operator* (const Vector& other) const{
  assert(this->elements == other.elements);
  float val = 0;
  for(int i = 0; i < this->elements; i++){
    val += (*this)[i]*other[i];
  }
  return val;
}

/**
 * Vector scalar multiplication
 * If needed it could be templated
 */
Vector Vector::operator* (const int scalar) const{
  Vector v(this->elements);

  for(int i = 0; i < this->elements; i++){
    v[i] = (*this)[i] * scalar;
  }
  return v;
}

/**
 * Vector scalar multiplication
 * If needed it could be templated
 */
Vector Vector::operator* (const float scalar) const{
  Vector v(this->elements);

  for(int i = 0; i < this->elements; i++){
    v[i] = (*this)[i] * scalar;
  }

  return v;
}

/**
 * Allocate the memory needed for the matrix
 */
void Matrix::_allocate(size_t rows, size_t columns){
  this->_values = (float**) calloc(rows, sizeof(float*));
  for(int i = 0; i < rows; i++){
    this->_values[i] = (float*) calloc(columns, sizeof(float));
  }

  this->_rows = rows;
  this->_columns = columns;
}

void Matrix::_copy(const Matrix& other){
  for(int row = 0; row < this->rows; row++){
    for(int col = 0; col < this->columns; col++){
      (*this)[row][col] = other[row][col];
    }
  }
}

Matrix::Matrix(size_t rows, size_t columns){
  this->_allocate(rows, columns);
}


/**
 * Copy constructor
 * Copies all the data from "other" into a new vector
 */
Matrix::Matrix(const Matrix& other){
  if(!(this == &other)){
    /* Allocate new memory*/
    this->_allocate(other.rows, other.columns);

    /* Copy the content */
    this->_copy(other);

    }
}

/**
 * Free the memory on destruction
 */
Matrix::~Matrix(){
  for(int i = 0; i < this->_rows; i++){
    free(this->_values[i]);
  }
  /*
   * If we haven't any rows, we have nothing to free
   */
  if (_rows){
    free(this->_values);
  }
}

/**
 * The assignment operator invokes the copy constructor and returns a reference to the copied vector
 */
Matrix& Matrix::operator= (const Matrix& other){
  if (!(this == &other)){
    this->~Matrix();
    this->_allocate(other.rows, other.columns);
    this->_copy(other);
  }
  return *this;
}

/**
 * We want to be able to index with m[0][0], m[i][i] ... m[m.rows - 1][m.columns - 1]
 * The "Proxy" maps the first index (the row) to the array containing the column elements,
 * So in practice we got m[i] -> proxy --> proxy[j] -> values of m[i][j]
 */
Matrix::Proxy Matrix::operator[] (const int index) const{
  assert(index >= 0 && index < this->_rows);
  return Proxy(this->_values[index], this->_columns);
}
float& Matrix::Proxy::operator[] (const int index) const{
  assert(index >= 0 && index < this->_columns);
  return _array[index];
}

/*
 * Matrix addition
 * out[i][j] = m1[i][j] + m2[i][j]
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

/*
 * Matrix subtraction
 * out[i][j] = m1[i][j] - m2[i][j]
 */
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

/**
 * Matrix multiplication
 * See https://msdn.microsoft.com/en-us/library/hh873134.aspx
 */
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

/**
 * Matrix scalar multiplication
 * If needed it could be templated 
 */
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

/**
 * Matrix scalar multiplication
 * If needed it could be templated 
 */
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
 * Maps the vector to a (row) matrix with 1 column.
 * Compute the matrix multiplication with the row matrix
 * Copy the result into the output vector
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

#if defined (__i386__) || defined (__x86_64__)

/**
 * Pretty print matrix
 */
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

/**
 * Pretty print vector
 */
std::ostream& AxoArm::operator<< (std::ostream &strm, Vector& v){
  for(int i = 0; i < v.elements; i++){
    strm << "[" << v[i] << "]" << std::endl;
  }

  return strm;
}
#endif
