function [exo] = exo_sim(controller, x0)

% 8=====================================D
% INITIALIZE
% 8=====================================D
	ParametersScript;
	mex GCC=/usr/bin/gcc-4.9.3 arduino_feedback_lin.c

	delete(instrfindall);
	s = serialInit('/dev/ttyS01');
	fopen(s);
	pause(2);
	T_end = 15; % [s]
	S = T_end/Ts; % Samples total

	x = zeros(n_s,S); % States: [theta_s; theta_e; thetadot_s; thetadot_e]
	u = zeros(n_i,S);

	x_m(:,1) = x0;
	u(:,1) = [0; 0];
	ardref = u;
	x_m = x;

% 8=====================================D
% REFERENCE
% 8=====================================D
	ref1 = [pi/2 pi*3/4 0 0]' * ones(1,T_end/Ts);
	% ref2 = [0.5  1 0 0]' * ones(1,30/Ts);
	% ref3 = [pi 0.25*pi 0 0]' * ones(1,30/Ts);
	% ref4 = [2  1 0 0]' * ones(1,30/Ts);
	
	ref = [ref1]; % ref2 ref3 ref4];

% 8=====================================D
% SIMULATE
% 8=====================================D
	for k = 2:S-1
		% Get input from controller
		u_tmp = controller(x(:,k),params,u(:,k-1),x(:,k-1),ref(:,k),s);
		u(:,k) = u_tmp(1:2);
		% ardref(:,k) = u_tmp(3:4);

		% Limit input signal to valid current range
		% u(1,k) = saturate(u(1,k),cur2torque(-maxC1,1,params),cur2torque(maxC1,1,params));
		% u(2,k) = saturate(u(2,k),cur2torque(-maxC2,2,params),cur2torque(maxC2,2,params));

		% Forward euler
	 	x(:,k+1) = x(:,k) + Ts*f(x(:,k), u(:,k), params);
	end

	% for k = 2:S-1
	% 	% Get input from controller
	% 	u_m(:,k) = feedback_lin_w_mex(x_m(:,k),params,u_m(:,k-1),x_m(:,k-1),ref(:,k));

	% 	% Limit input signal to valid current range
	% 	u_m(1,k) = saturate(u_m(1,k),cur2torque(-maxC1,1,params),cur2torque(maxC1,1,params));
	% 	u_m(2,k) = saturate(u_m(2,k),cur2torque(-maxC2,2,params),cur2torque(maxC2,2,params));

	% 	% Forward euler
	%  	x_m(:,k+1) = x_m(:,k) + Ts*f(x_m(:,k), u_m(:,k), params);
	% end

% 8=====================================D
% SAVE OUTPUTS
% 8=====================================D
	t = 0:Ts:T_end-Ts;
	exo.t = t;
	exo.x = x;
	exo.u = u;
	exo.ref = ref;
	exo.ardref = ardref;
	% exo.t = t;
	% exo.x_m = x_m;
	% exo.u_m = u_m;

	fclose(s);
end