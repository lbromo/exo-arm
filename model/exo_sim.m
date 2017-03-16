function [exo] = exo_sim(controller, x0, ref)

% 8=====================================D
% INITIALIZE
% 8=====================================D
	if ~exist('x0')
		x0 = [0 0 0 0]';
	end

	params = ParametersScript();
	addpath controllers;

	T_end = 15; % [s]
	S = T_end/params.Ts; % Samples total
	t = 0:params.Ts:T_end-params.Ts;

	x = zeros(params.n_s,S); % States: [theta_s; theta_e; thetadot_s; thetadot_e]
	u = zeros(params.n_i,S);

	x(:,1) = x0;
	u(:,1) = [0; 0];

	if isequal(controller, @c_mex)
		mex -I../software/udoo/arduino-part/ GCC=/usr/bin/gcc-4.9.3 controllers/controller_mex.cpp ../software/udoo/arduino-part/AxoArmUtils.cpp ../software/udoo/arduino-part/Matrix.cpp
	end

	s = [];
	if isequal(controller, @c_arduino)
		delete(instrfindall);
		s = serialInit('/dev/ttyS01');
		fopen(s);
		pause(2);
	end


	if isequal(controller, @c_admittance)
		tau = sin(t);
	end

% 8=====================================D
% REFERENCE
% 8=====================================D
	if ~exist('ref')
		ref1 = [pi/2 pi*3/4 0 0]' * ones(1,T_end/params.Ts);
		% ref2 = [0.5  1 0 0]' * ones(1,30/Ts);
		% ref3 = [pi 0.25*pi 0 0]' * ones(1,30/Ts);
		% ref4 = [2  1 0 0]' * ones(1,30/Ts);
		
		ref = [ref1]; % ref2 ref3 ref4];
	else
		ref = ref' * ones(1,T_end/params.Ts);
	end


% 8=====================================D
% SIMULATE
% 8=====================================D
	for k = 2:S-1
		% Get input from controller
		u(:,k) = controller(x(:,k),params,tau(:,k),x(:,k-1),ref(:,k),s);

		% Limit input signal to valid current range
		u(1,k) = saturate(u(1,k),cur2torque(-params.maxC1,1,params),cur2torque(params.maxC1,1,params));
		u(2,k) = saturate(u(2,k),cur2torque(-params.maxC2,2,params),cur2torque(params.maxC2,2,params));

		% Forward euler
	 	x(:,k+1) = x(:,k) + params.Ts*f(x(:,k), u(:,k), params);
	end


% 8=====================================D
% SAVE OUTPUTS
% 8=====================================D
	exo.t = t;
	exo.x = x;
	exo.u = u;
	exo.ref = ref;

	if isequal(controller, @c_arduino)
		fclose(s);
	end

	if isequal(controller, @c_admittance)
		controller([],[],[],[],[],[],1);
	end
end