function u = feedback_lin_w_mex(x,params,upre, xpre,ref,s)

	p = 12;
	pd = 3.5;
	kp = [p 0  pd 0;...
		  0  p 0 pd];
	

	x = x + 0.1 * rand(4,1);
	
	e = ref-x;

	B_m = arduino_feedback_lin(x, 'B');

	B_m = reshape(B_m,2,2);

	n_v = arduino_feedback_lin(x, 'n');

	u = (B_m * (kp * e)+ n_v);
	u = u./([params.kt1 params.kt2]'*params.N);

end