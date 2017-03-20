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
    Vector() {};
    Vector(size_t elements);
#if defined (__i386__) || defined (__x86_64__) || defined (__arm__)
    Vector(const Vector& other);
#endif
    ~Vector();

    const size_t& elements = _elements;

#if defined (__i386__) || defined (__x86_64__) || defined (__arm__)
    Vector& operator= (const Vector& other);
#endif
    float& operator[] (const int index) const;

    Vector operator+ (const Vector& other) const;
    Vector operator- (const Vector& other) const;
    float operator* (const Vector& other) const;
    Vector operator* (const int scalar) const;
    Vector operator* (const float scalar) const;

  private:
    float* _values;
    size_t _elements;
  };

  class Matrix{
  public:
    Matrix();
    Matrix(size_t rows, size_t columns);
#if defined (__i386__) || defined (__x86_64__) || defined (__arm__)
    Matrix(const Matrix& other);
#endif
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

#if defined (__i386__) || defined (__x86_64__) || defined (__arm__)
    Matrix& operator=(const Matrix& other);
#endif
    Proxy operator[](const int index) const;

    Matrix operator+ (const Matrix& other) const;
    Matrix operator- (const Matrix& other) const;
    Matrix operator* (const Matrix& other) const;
    Matrix operator* (const int scalar) const;
    Matrix operator* (const float scalar) const;

    Vector operator* (const Vector& v) const;


  private:
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