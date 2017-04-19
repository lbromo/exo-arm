function [exo] = exo_sim(controller, x0, ref)

% 8=====================================D
% INITIALIZE
% 8=====================================D
	if ~exist('x0')
		x0 = [0 0 0 0]';
	end

	params = ParametersScript();
	addpath controllers;

	T_end = 30; % [s]
	S = T_end/params.Ts; % Samples total
	t = 0:params.Ts:T_end-params.Ts;

	x = zeros(params.n_s,S); % States: [theta_s; theta_e; thetadot_s; thetadot_e]
	u = zeros(params.n_i,S);
	c = zeros(params.n_i,S);

	x(:,1) = x0;
	u(:,1) = [0; 0];
	cpars.ei = [0 0]';

	if isequal(controller, @c_mex)
		mex -I../software/udoo/arduino-part/ GCC=/usr/bin/gcc-4.9.3 controllers/controller_mex.cpp ../software/udoo/arduino-part/AxoArmUtils.cpp ../software/udoo/arduino-part/Matrix.cpp
	end

	if isequal(controller, @c_arduino)
		delete(instrfindall);
		s = serialInit('/dev/ttyS01');
		fopen(s);
		pause(2);
		cpars.s = s;
		out = zeros(4,S);
	end


	if isequal(controller, @c_admittance)
		cpars.tau = sin(t);
	end

	if isequal(controller, @c_test)
		cpars.t_end = 100;
	end

% 8=====================================D
% REFERENCE
% 8=====================================D
	if ~exist('ref')
		ref1 = [pi/2 pi*3/4 0 0]' * ones(1,30/params.Ts);
		ref2 = [0.5  1 0 0]' * ones(1,30/params.Ts);
		ref3 = [pi 0.25*pi 0 0]' * ones(1,30/params.Ts);
		ref4 = [2  1 0 0]' * ones(1,30/params.Ts);

		ref5 = [1 1 0 0]' * ones(1,30/params.Ts);

		
		ref = [ref5]; % ref2 ref3 ref4];
	else
		ref = ref' * ones(1,T_end/params.Ts);
	end

	n = [0.1 0.1 1 1]' .* randn(params.n_s,S);

% 8=====================================D
% SIMULATE
% 8=====================================D
	for k = 1:S-1
		% Get input from controller
		cpars.ref = ref(:,k); 
		cpars.k = k;
		cpars.n = n(:,k);

		u(:,k) = controller(x(:,k),params,cpars);

		% Forward euler
	 	x(:,k+1) = x(:,k) + params.Ts*f(x(:,k), u(:,k), params);
	end


% 8=====================================D
% SAVE OUTPUTS
% 8=====================================D
	exo.t = t;
	exo.x = x;
	exo.u = u;
	exo.c = c;
	exo.ref = ref;

	if isequal(controller, @c_arduino)
		exo.epwm = out(1,:);
		exo.spwm = out(2,:);
		fclose(s);
	end

	if isequal(controller, @c_admittance)
		cpars.cl = 1;
		controller([],[],cpars);
	end

	if isequal(controller, @c_feedback_lin)
		cpars.cl = 1;
		controller([],[],cpars);
	end


end