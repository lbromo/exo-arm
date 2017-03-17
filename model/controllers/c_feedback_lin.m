function u = c_feedback_lin(x,params,cpars)

	p = 50;
	pd = 10;
	kp = [p 0  pd 0;...
		  0  p 0 pd];
	

	% x = x + 0.1 * rand(4,1);
	
	e = cpars.ref-x;

	u = (B(x,params) * (kp * e) + n(x,params));
	u = u./([params.kt1 params.kt2]'*params.N);

end