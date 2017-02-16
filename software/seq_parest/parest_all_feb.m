close all; clear all

% 8=====================================D
% GET ALL THE FILES
% 8=====================================D

Ts = 0.01;
joint = 1;
smooth_par = 50;

if joint == 1 % Elbow
	names = {'rs_60_0.1', 'rs_60_0.2', 'rs_60_0.3', 'e_sin_no_0.6', 'e_sin_no_0.7'};
	%names = {'rs_60_0.1'};%, 'rs_60_0.2', 'rs_60_0.3', 'sw_60_0.1', 'sw_60_0.1', 'sw_60_0.1'};
elseif joint == 2 % shoulder
	names = {'rs_60_0.1', 'rs_60_0.3', 'rs_60_0.5', 's_sin_no_1.1', 's_sin_no_1.3', 's_sin_no_1.5'};
end

% 8=====================================D
% LOAD ALL THE DATA
% 8=====================================D

for n = 1:length(names)
	[in(n) m1(n) m2(n)] = getParestData(names{n},joint);
end

% 8=====================================D
% BUILD ALL THE VECTORS
% 8=====================================D

vel  = [];
cur  = [];

for n = 1:length(names)
	vel = cat(1,vel,getSignal(m1(n),'velocity'));
	cur = cat(1,cur,getSignal(m1(n),'current'));
end

acc = diff(vel,1,1)./Ts;
acc = smooth(smooth(acc));

vel = vel(1:end-1);
cur = cur(1:end-1);

time = [Ts:Ts:length(vel)*Ts];

pars;

%par = [cur -vel -sigmoid(vel,sigmoidpar)] \ [Jm*acc];
par = [cur -vel -sigmoid(vel,sigmoidpar) -sigmoid(vel,sigmoidpar).*exp(-abs(vel./vs))] \ [Jm*acc];

kt    = par(1);
b     = par(2);
tau_c = par(3);
tau_s = par(4);

simulate_it;

% 8=====================================D
% PLOT
% 8=====================================D

plot(time,vel,time,x(2,1:end-1));

ylabel('Velocity');
grid on;
legend('Measured', 'Simulated')

disp('MSE:')
disp(immse(x(2,2:end)',vel))
