#ifndef _MATRIX_h_
#define _MATRIX_h_

#if defined (__i386__) || defined (__x86_64__) || defined (__arm__)
  #include <cstdlib>
  #ifndef __arm__ 
    #include <iostream> /* Altså kun på rigtige computere... Hvis nogen skulle være i tvivl*/
  #endif
#else
  #include <stdint.h>
  #define size_t uint8_t
#endif /*  (__i386__) || (__x86_64__) */

namespace AxoArm{

  class Vector{
  public:
    Vector() : _elements(0) {};
    Vector(size_t elements);
    Vector(const Vector& other);
    ~Vector();

    const size_t& elements = _elements;

    Vector& operator= (const Vector& other);
    float& operator[] (const int index) const;

    Vector operator+ (const Vector& other) const;
    Vector operator- (const Vector& other) const;
    float operator* (const Vector& other) const;
    Vector operator* (const int scalar) const;
    Vector operator* (const float scalar) const;

  private:
    void _allocate(size_t elements);
    void _copy(const Vector& other);
    float* _values;
    size_t _elements;
  };

  class Matrix{
  public:
  Matrix() : _rows(0), _columns(0) {};
    Matrix(size_t rows, size_t columns);
    Matrix(const Matrix& other);
    ~Matrix();

    class Proxy{
    public:
      Proxy (float* array, size_t columns) : _array(array), _columns(columns) { }
      float& operator[](const int index) const;
    private:
      float* _array;
      size_t _columns;
    };

    const size_t& rows = _rows;
    const size_t& columns = _columns;

    Matrix& operator=(const Matrix& other);
    Proxy operator[](const int index) const;

    Matrix operator+ (const Matrix& other) const;
    Matrix operator- (const Matrix& other) const;
    Matrix operator* (const Matrix& other) const;
    Matrix operator* (const int scalar) const;
    Matrix operator* (const float scalar) const;

    Vector operator* (const Vector& v) const;


  private:
    void _allocate(size_t rows, size_t cols);
    void _copy(const Matrix& other);
    float** _values;
    size_t _rows;
    size_t _columns;
  };

#if defined (__i386__) || defined (__x86_64__)
  std::ostream& operator<< (std::ostream &strm, Matrix& m);
  std::ostream& operator<< (std::ostream &strm, Vector& v);
#endif /*  (__i386__) || (__x86_64__) */
}

#endif /* _MATRIX_h_ */
