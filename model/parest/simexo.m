function y = simexo(u, t, par)

%% Constants
g   = 9.81;     % [m/s^2] Gravitational acceleration
Ts	= 0.004;	% [s] Sampling period

%% Constants - Link 1:
d1  = 0;        % [m] Distance from {0} to {1} along z0
a1  = 0.25;        % [m] Distance from {0} to {1} along x0
alpha1 = 0;  % [rad] Rotation of z1 compared to z0
l1  = 3.5e-2;   % [m] Distance from {1} to CoM of link 1
m1  = 0.241;	% [kg] Mass of link 1

%% Constants - Link 2:
d2  = 0;        % [m] Distance from {1} to {2} along z1
a2  = 0.25;    % [m] Distance from {1} to {2} along x1
alpha2 = 0;     % [rad] Rotation of z2 compared to z1
l2  = 0.151;   % [m] Distance from {2} to CoM of link 2
m2  = 0.231;	% [kg] Mass of link 2

%% Frictions 
cm=[0.01 0.05]; 
vm=[0.00005 0.00055]; 

% Estimation Parameters
cm(1) = par(1);
vm(1) = par(2);

%% Inertias
[I1, I2] = InertiaCalculations([a1 a2],[m1 m2]);

%I1(2,2) = par(1);
%I1(3,3) = par(2);

params.m1 = m1;
params.m2 = m2;
params.a1 = a1;
params.a2 = a2;
params.l1 = l1;
params.l2 = l2;
params.I1 = I1;
params.I2 = I2;
params.g = g;
params.cm = cm;
params.vm = vm;

xd = [0;0;0;0];

Ts = t(2)-t(1);



for k = 1:length(t)
  xd(:,k+1) = xd(:,k) + Ts*f(xd(:,k), u(k,:)', params);
end

y = xd(:,2:end)';

end