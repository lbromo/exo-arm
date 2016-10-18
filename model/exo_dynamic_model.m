function [xdot] = exo_dynamic_model(x,torque, params)

  theta = x(:,1:2);
  thetadot = x(:,2:4)

%
% initheta=[0 0];
% inithetad=[0 0];
% inithetadd=[0 0];

  V=v_matrix(theta,thetadot, params.l2, params.m2, params.a1, params.a2)
  Minv=minv_matrix(theta, params.l1, params.l2, params.m1, params.m2, params.a1, params.a2, params.I1, params.I2)
  G=g_matrix(theta, params.g, params.l1, params.l2, params.m1, params.m2, params.a1 ,params.a2)
  F=f_matrix(thetadot, params.vm, params.cm)


  thetadotdot = Minv*(torque-V-G-F);

  xdot = [thetadot; thetadotdot]

end
