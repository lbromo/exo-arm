function [xdot] = exo_dynamic_model(t, x,torque, params)
persistent t_clk;

if isempty(t_clk)
		t_clk = 1;
end

  theta = x(1:2);
  thetadot = x(3:4);

  if t > 5
    torque = [0; 0];
  end


  Minv=minv_matrix(theta, params.l1, params.l2, params.m1, params.m2, params.a1, params.a2, params.I1, params.I2);

  V=v_matrix(theta,thetadot, params.l2, params.m2, params.a1, params.a2);
  G=g_matrix(theta, params.g, params.l1, params.l2, params.m1, params.m2, params.a1 ,params.a2);
  F=f_matrix(thetadot, params.vm, params.cm);

  thetadotdot = Minv*(torque-(V+G+F));

  xdot = [thetadot; thetadotdot];
telaps = t;

if telaps > t_clk
	params.arm.plot(theta');
	t;
	timestr = sprintf('%4.1f sec elapsed', telaps);
	t_clk = t_clk + .001;
	disp(timestr)
end

end
