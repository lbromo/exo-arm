function [xdot] = f(x, u, params)
  theta = x(1:2,end);
  thetadot = x(3:4,end);

  Minv=minv_matrix(theta, params.l1, params.l2, params.m1, params.m2, params.a1, params.a2, params.I1, params.I2);

  V=v_matrix(theta,thetadot, params.l2, params.m2, params.a1, params.a2);
  G=g_matrix(theta, params.g, params.l1, params.l2, params.m1, params.m2, params.a1 ,params.a2);
  F=f_matrix(thetadot, params.vm, params.cm);

if (abs(F) > abs(u-V-G))
	if (abs(thetadot) < 0.01)
% 		F = (u-V-G);
	end
end

  thetadotdot = Minv*(u-(V+G+F));

  xdot = [thetadot; thetadotdot];
end
