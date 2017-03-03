function u = c_feedback_lin(x,params,upre, xpre,ref)

	p = 12;
	pd = 3.5;
	kp = [p 0  pd 0;...
		  0  p 0 pd];

	K = kp.*[params.kt1 params.kt2]'*params.N;

	x = x + 0.1 * rand(4,1);
	
	e = ref-x;

	u = B(x,params) * (K * e) + n(x,params);

end