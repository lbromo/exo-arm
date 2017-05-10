% clear all; close all;
% clear globals;
function [vel xd] = sim_test(NAME)
global params;
params = ParametersScript;

% NAME = 'march_3';
[in m2 m1] = getParestData(NAME,4);

pwm1 = getSignal(in, 'pwm2');
on1  = getSignal(in, 'on2');
dir1 = getSignal(in, 'dir2');
pwm2 = getSignal(in, 'pwm1');
on2  = getSignal(in, 'on1');
dir2 = getSignal(in, 'dir1');

vel1 = getSignal(m1, 'velocity')./params.N;
ang1 = getSignal(m1, 'angle');
cur1_m = getSignal(m1, 'current');
vel2 = getSignal(m2, 'velocity')./params.N;
ang2 = getSignal(m2, 'angle');
cur2_m = getSignal(m2, 'current');

addpath('verification')

global Ts;
Ts = 0.010 * ones(length(vel1),1);

%% FROM HERE, EVERYTHING THAT NEEDS SWITCHING IS SWITCHED!


global x0;
x0=[ang1(1), ang2(1), vel1(1), vel2(1)];


cur1 = pwm2cur(pwm1, dir1, 1);
cur2 = pwm2cur(pwm2, dir2, 2);

u = zeros(2,length(cur1));
u(1,:) = cur1_m' * params.kt1 * params.N; % Torque
u(2,:) = cur2_m' * params.kt2 * params.N;

% par_to_get=[params.cm params.vm params.sigmoidpar];% params.cm params.vm  params.sigmoidpar params.hast
% ydata=[ang1 ang2 vel1 vel2]'; 
% [X, resnorm] = lsqcurvefit(@parest_forward, par_to_get, u, ydata, [0 0 0 0 0 0]);

% params.cm=X(1:2);
% params.vm=X(3:4);
% params.sigmoidpar=X(5:6);

xd = zeros(4,length(u(:,1)));
xd(:,1) = x0;

for k = 1:length(u(1,:))-1  %forward euler
	[xdot V(:,k) G(:,k) F(:,k)] = f(xd(:,k), u(:,k), params);
	xd(:,k+1) = xd(:,k) + Ts(k)*xdot;
	% xd(1:2,k+1) = [ang1(k+1) ang2(k+1)];
end

vel = [vel1; vel2];

end