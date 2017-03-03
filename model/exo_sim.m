function [exo] = exo_sim(controller, x0)

% 8=====================================D
% INITIALIZE
% 8=====================================D
	ParametersScript;
	T_end = 120; % [s]
	S = T_end/Ts; % Samples total

	x = zeros(n_s,S); % States: [theta_s; theta_e; thetadot_s; thetadot_e]
	u = zeros(n_i,S);

	x(:,1) = x0;
	u(:,1) = [0; 0];

% 8=====================================D
% REFERENCE
% 8=====================================D
	ref1 = [pi/2 pi*3/4 0 0]' * ones(1,30/Ts);
	ref2 = [0.5  1 0 0]' * ones(1,30/Ts);
	ref3 = [pi 0.25*pi 0 0]' * ones(1,30/Ts);
	ref4 = [2  1 0 0]' * ones(1,30/Ts);
	
	ref = [ref1 ref2 ref3 ref4];

% 8=====================================D
% SIMULATE
% 8=====================================D
	for k = 2:S-1
		% Get input from controller
		u(:,k) = controller(x(:,k),params,u(:,k-1),x(:,k-1),ref(:,k));

		% Limit input signal to valid current range
		u(1,k) = saturate(u(1,k),cur2torque(-maxC1,1,params),cur2torque(maxC1,1,params));
		u(2,k) = saturate(u(2,k),cur2torque(-maxC2,2,params),cur2torque(maxC2,2,params));

		% Forward euler
	 	x(:,k+1) = x(:,k) + Ts*f(x(:,k), u(:,k), params);
	end

% 8=====================================D
% SAVE OUTPUTS
% 8=====================================D
	t = 0:Ts:T_end-Ts;
	exo.t = t;
	exo.x = x;
	exo.u = u;

end