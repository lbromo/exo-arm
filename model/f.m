function [xdot] = f(x, u, params, acc)
  theta = x(1:2);
  thetadot = x(3:4);

  Minv=minv_matrix(theta, params.l1, params.l2, params.m1, params.m2, params.a1, params.a2, params.I1, params.I2, params.In1, params.In2, params.N);
  M=m_matrix(theta, params.l1, params.l2, params.m1, params.m2, params.a1, params.a2, params.I1, params.I2, params.In1, params.In2, params.N);
  V=v_matrix(theta,thetadot, params.l2, params.m2, params.a1, params.a2);
  G=g_matrix(theta, params.g, params.l1, params.l2, params.m1, params.m2, params.a1 ,params.a2);
  F=f_matrix(thetadot, params.vm, params.cm, params.N, params.sigmoidpar);

% if (abs(F(1)) > abs(u(1)-V(1)-G(1)-M(1)*acc(1)))
% 	if (abs(thetadot(1)) < 0.0105)
%  		F(1) = (u(1)-V(1)-G(1)-M(1)*acc(1));
% 	end
% end
% if (abs(F(2)) > abs(u(2)-V(2)-G(2)-M(2)*acc(2)))
% 	if (abs(thetadot(2)) < 0.0105)
%  		F(2) = (u(2)-V(2)-G(2)-M(2)*acc(2));
% 	end
% end

  thetadotdot = Minv*(u-(V+G+F));

  xdot = [thetadot; thetadotdot];
end
