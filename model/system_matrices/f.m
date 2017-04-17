function [xdot V G F] = f(x, u, params)
  theta = x(1:2);
  thetadot = x(3:4);
                                          
  Minv=minv_matrix(theta, params.l1, params.l2, params.m1, params.m2, params.a1, params.a2, params.I1, params.I2, params.In1, params.In2, params.N);
  %M=m_matrix(theta, params.l1, params.l2, params.m1, params.m2, params.a1, params.a2, params.I1, params.I2, params.In1, params.In2, params.N);
  V=v_matrix(theta,thetadot, params.l2, params.m2, params.a1, params.a2);
  G=g_matrix(theta, params.g, params.l1, params.l2, params.m1, params.m2, params.a1 ,params.a2);
  F=f_matrix(thetadot, params.vm, params.cm, params.N, params.sigmoidpar);

% torquesum=u-G-V;  %when vel=0 M=0 and V=0
  
% if (thetadot(1) == 0)
%   F(1) = nmin([torquesum(1), -sign(torques(1))*params.cm(1)]);
% end
% if (thetadot(2) == 0)
%   F(2) = nmin([torquesum(2), -sign(torques(2))*params.cm(2)]);
% end

% if (abs(F(1)) > abs(torquesum(1))) 
% 	F(1) = (torquesum(1));
% end
% if (abs(F(2)) > abs(torquesum(2)))
% 	F(2) = (torquesum(2));
% end
% 
% if (abs(F(1)) < abs(torquesum(1))) 
% 	if (abs(thetadot(1)) <  0.0155) 
%  		F(1) = (params.cm(1) + params.hast(1))*sign(torquesum(1));
% 	end
% end
% if (abs(F(2)) < abs(torquesum(2)))
% 	if (abs(thetadot(2)) <  0.0155)
%  		F(2) = (params.cm(2) + params.hast(2))*sign(torquesum(2));
% 	end
% end

  thetadotdot = Minv*(u-(V+G+F));

  xdot = [thetadot; thetadotdot];
end
