#include <iostream>

namespace AxoArm{

  class Vector{
  public:
    Vector(size_t elements);
    ~Vector();
    float& operator[] (const int index);
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

    Proxy operator[](const int index);
    friend std::ostream& operator<< (std::ostream &strm, Matrix& m);

    const size_t& rows = _rows;
    const size_t& columns = _columns;
  private:
    float** _values;
    size_t _rows;
    size_t _columns;
  };

  Vector controller(Vector& x, Vector& ref);
  Vector get_N_vector(Vector& x);
  Matrix get_M_matrix(Vector& x);

  std::ostream& operator<< (std::ostream &strm, Matrix& m);
}
