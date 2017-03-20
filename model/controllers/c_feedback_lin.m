function u = c_feedback_lin(x,params,cpars)

	p = 12;
	pd = 3.5;
	kp = [p 0  pd 0;...
		  0  p 0 pd];
	

	% x = x + cpars.n;
	
	e = cpars.ref-x;

	u = B(x,params) * (kp * e) + n(x,params);
	u = u./([params.kt1 params.kt2]'*params.N);

end