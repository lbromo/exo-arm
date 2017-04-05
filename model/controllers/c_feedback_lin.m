function [u ei] = c_feedback_lin(x,params,cpars)

persistent err_int;

if isempty(err_int)
	disp('First Run!');
	err_int = [0; 0];
end

if isfield(cpars,'cl')
	clear err_int;
	disp('err_int cleared');
	u = 0;
	e = 0;
	return;
end


	kp = 12;
	kd = 6;
	ki = 3;
	k = [kp 0  kd 0  ki 0;...
		   0  kp 0  kd 0  ki];
	
	% x = x + cpars.n;
	
	e = cpars.ref-x;

	e = [e; err_int(1:2)];

	Bm = B(x,params); 
	nv =  n(x,params);

	u =  Bm * (k * e) + nv; % This is a torque

	u = u./([params.kt1 params.kt2]'*params.N); % Convert to current

	ei = e(1:2);

	if abs(u(1)) > params.maxC1;
		ei(1) = 0;
		disp('aw1')
	end
	if abs(u(2)) > params.maxC2;
		ei(2) = 0;
		disp('aw2')
	end

	u(1) = saturate(u(1),-params.maxC1,params.maxC1);
	u(2) = saturate(u(2),-params.maxC2,params.maxC2);

	u(1) = cur2torque(u(1),1,params);
	u(2) = cur2torque(u(2),2,params);

 	% Error integration
	err_int = err_int + params.Ts*ei;


end
