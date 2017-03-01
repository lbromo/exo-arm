function [B] = B(x, params)

  B = m_matrix(x(1:2), params.l1, params.l2, params.m1, params.m2, params.a1, params.a2, params.I1, params.I2, params.In1, params.In2, params.N);

end