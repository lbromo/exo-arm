clear all; close all;

[in m2 m1] = getParestData('new_1',4);

pwm1 = getSignal(in, 'pwm2');
on1  = getSignal(in, 'on2');
dir1 = getSignal(in, 'dir2');
pwm2 = getSignal(in, 'pwm1');
on2  = getSignal(in, 'on1');
dir2 = getSignal(in, 'dir1');

vel1 = getSignal(m1, 'velocity');
ang1 = getSignal(m1, 'angle');
vel2 = getSignal(m2, 'velocity');
ang2 = getSignal(m2, 'angle');

%% FROM HERE, EVERYTHING THAT NEEDS SWITCHING IS SWITCHED!

cur1 = pwm2cur(pwm1, dir1, 1);

cur2 = pwm2cur(pwm2, dir2, 2);

params = ParametersScript;

u = zeros(2,length(cur1));
u(1,:) = cur1' * params.kt1 * params.N;
u(2,:) = cur2' * params.kt2 * params.N;

xd = zeros(4,length(u(:,1)));
xd(:,1) = [ang1(1), ang2(1), vel1(1)/params.N, vel2(1)/params.N];

Ts = 0.01;

for k = 1:length(u(1,:))-2  %forward euler
	[xdot V(:,k) G(:,k) F(:,k)] = f(xd(:,k), u(:,k), params);
	xd(:,k+1) = xd(:,k) + Ts*xdot;
	xd(1:2,k+1) = [ang1(k+1) ang2(k+1)];
end
