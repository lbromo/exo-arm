#if defined (__i386__) || defined (__x86_64__)
#include <iostream>
#endif /*  (__i386__) || (__x86_64__) */

namespace AxoArm{

  class Vector{
    friend class Matrix;
  public:
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

    Proxy operator[](const int index);

  private:
    float** _values;
    size_t _rows;
    size_t _columns;
  };

  Vector controller(Vector& x, Vector& ref);
  Vector get_N_vector(Vector& x);
  Matrix get_M_matrix(Vector& x);

  Matrix operator* (Matrix& m1, Matrix& m2){
    assert(m1.columns == m2.rows);
    auto m = m1.rows;
    auto p = m1.columns;
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

  Vector operator* (Matrix& m1, Vector& v){
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
  std::ostream& operator<< (std::ostream &strm, Matrix& m);
  std::ostream& operator<< (std::ostream &strm, Vector& v);
#endif /*  (__i386__) || (__x86_64__) */
}
