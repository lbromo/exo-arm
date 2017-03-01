function u = c_feedback_lin(x,params)

	p = 0.1;
	kp = [p 0  0 0;...
		  0  p 0 0];
	% i = 10;
	% ki = [i 0  0 0;...
	% 	 0  i 0 0];

	ref = [pi/4 pi*3/4 0 0]';

	% x = x + 1.*rand(4,1);
	
	e = ref-x;
	% u(:,k) = kp * e + ki * e_int;
	
	%c = [200.1*eye(2); zeros(2,2)]' * e - [199.9*eye(2); zeros(2,2)]' * epre - upre;
	c = [0; 0];

	c(1) = e(1) - x(3);
	c(2) = e(2) - x(4);

	u = B(x,params) * (kp * e) + n(x,params);

end