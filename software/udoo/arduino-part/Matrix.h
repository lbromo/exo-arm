#pragma once

#if defined (__i386__) || defined (__x86_64__)
#include <iostream>
#endif /*  (__i386__) || (__x86_64__) */

namespace AxoArm{

  class Vector{
  public:
    Vector() {};
    Vector(size_t elements);
    ~Vector();
    float& operator[] (const int index);

    const size_t& elements = _elements;

  private:
    float* _values;
    size_t _elements;
  };

  class Matrix{
  public:
    Matrix(size_t rows, size_t columns);
    ~Matrix();

    class Proxy{
    public:
      Proxy (float* array, size_t columns) : _array(array), _columns(columns) { }
      float& operator[](const int index);
    private:
      float* _array;
      size_t _columns;
    };

    const size_t& rows = _rows;
    const size_t& columns = _columns;

    Matrix& operator=(const Matrix& m) = default;
    Proxy operator[](const int index);

  private:
    float** _values;
    size_t _rows;
    size_t _columns;
  };

  Matrix operator+ (Matrix& m1, Matrix& m2);
  Matrix operator- (Matrix& m1, Matrix& m2);
  Matrix operator* (Matrix& m1, Matrix& m2);
  Matrix operator* (Matrix& m1, int& scalar);
  Matrix operator* (Matrix& m1, float& scalar);

  Vector operator+ (Vector& v1, Vector& v2);
  Vector operator- (Vector& v1, Vector& v2);
  float operator* (Vector& v1, Vector& v2);
  Vector operator* (Vector& v1, int& scalar);
  Vector operator* (Vector& v1, float& scalar);


  Vector operator* (Matrix& m1, Vector& v);



#if defined (__i386__) || defined (__x86_64__)
  std::ostream& operator<< (std::ostream &strm, Matrix& m);
  std::ostream& operator<< (std::ostream &strm, Vector& v);
#endif /*  (__i386__) || (__x86_64__) */
}
