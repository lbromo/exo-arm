params = ParametersScript();

torque_seq = zeros(2,1000);
% torque_seq(:,1:100) = [1:100; 1:100];
% torque_seq(:,100:200) = [100:-1:0; 100:-1:0];
% torque_seq(:,200:300) = [0:-1:-100; 0:-1:-100];
% torque_seq(:,300:400) = [-100:1:0; 0:-1:-100];
torque_seq(:,1:50) = 40

x = zeros(4,1)
ref = zeros(6,1)
u = []

% 8=====================================D
% SIMULATE
% 8=====================================D

for k = 1:1000

  ref(:,k) = admittance2(torque_seq(:,k));

  % Get input from controller
	cpars.ref = ref(1:4,k);
	cpars.k = k;
	cpars.n = 0;

  [u(:,k) e] = c_feedback_lin(x(:,k),params,cpars);

  % Forward euler
	x(:,k+1) = x(:,k) + params.Ts*f(x(:,k), u(:,k), params);
end


% 8=====================================D
% SAVE OUTPUTS
% 8=====================================D
exo.x = x;
exo.u = u;
exo.ref = ref;
