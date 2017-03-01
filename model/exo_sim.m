function [exo] = exo_sim(controller, x0)

	ParametersScript;
	T_end = 30; % [s]
	S = T_end/Ts; % Samples total

	x = zeros(n_s,S); % States: [theta_s; theta_e; thetadot_s; thetadot_e]
	u = zeros(n_i,S);

	x(:,1) = x0;
	u(:,1) = [0; 0];
	e_int = zeros(4,1);
	tau = u;


	for k = 1:S-1
		
		u(:,k) = controller(x(:,k),params);

		u(1,k) = saturate(u(1,k),-3,3);
		u(2,k) = saturate(u(2,k),-1,1);

		tau(:,k) = u(:,k).*[params.kt1 params.kt2]'*N;

	 	x(:,k+1) = x(:,k) + Ts*f(x(:,k), tau(:,k), params);

	end

	t = 0:Ts:T_end-Ts;

	exo.t = t;
	exo.x = x;
	exo.u = u;
	exo.tau = tau;

end