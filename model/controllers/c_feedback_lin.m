function [u] = c_feedback_lin(x,params,cpars)

persistent err_int epre vpre;

if isempty(err_int) & isempty(epre) & isempty(vpre)
	disp('First Run!');
	err_int = [0; 0];
	epre = [0 0]';
	vpre = [0 0]';
end

if isfield(cpars,'cl')
	clear err_int epre vpre;
	disp('cleared');
	u = 0;
	return;
end


	kp = 1000;
	kd = 2 * sqrt(1000);
	ki = 200;

	k = [kp 0  kd 0  ki 0;...
		   0  kp 0  kd 0  ki];
	
	% x = x + cpars.n;
	

	e = cpars.ref-x;

	e = [e; err_int(1:2)];

	Bm = B(x,params); 
	nv =  n(x,params);

	v = zeros(2,1);

	% Controller corresponding to 15 * (s+1.5)/(s+5);
	% v(1) = 14.74 * e(1) - 14.52 * epre(1) + 0.951 * vpre(1);
	% v(2) = 14.74 * e(2) - 14.52 * epre(2) + 0.951 * vpre(2);

	v = k * e;

	u = Bm * v + nv; % This is a torque

	u = u./([params.kt1 params.kt2]'*params.N); % Convert to current

	% Anti windup
	ei = e(1:2);

	% if abs(v(1)) > params.maxC1;
	% 	ei(1) = 0;
	% 	disp('aw1')
	% end
	% if abs(v(2)) > params.maxC2;
	% 	ei(2) = 0;
	% 	disp('aw2')
	% end

	u(1) = saturate(u(1),-params.maxC1,params.maxC1);
	u(2) = saturate(u(2),-params.maxC2,params.maxC2);

	u(1) = cur2torque(u(1),1,params);
	u(2) = cur2torque(u(2),2,params);

 	% Error integration
	err_int = err_int + params.Ts*ei;

	% FIR
	epre = e(1:2);
	vpre = v;

end
