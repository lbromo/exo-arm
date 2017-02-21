close all; clear all

% 8=====================================D
% GET ALL THE FILES
% 8=====================================D

Ts = 0.01;
joint = 1;
smooth_par = 50;

if joint == 1 % Elbow
	names = {'rs_60_0.1', 'rs_60_0.2', 'rs_60_0.3', 'e_sin_no_0.6', 'e_sin_no_0.7'};
	%names = {'e_sin_no_0.5', 'e_sin_no_0.6', 'e_sin_no_0.7'};
elseif joint == 2 % shoulder
	names = {'rs_60_0.1', 'rs_60_0.3', 'rs_60_0.5', };%;'s_sin_no_1.3', 's_sin_no_1.5'};
	%names = {'s_sin_no_1.1', 's_sin_no_1.3', 's_sin_no_1.5', }
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

% acc = diff(vel,1,1)./Ts;
% acc = smooth(smooth(acc));
acc = diff(smooth(vel),1,1)./Ts;

vel = vel(1:end-1);
cur = cur(1:end-1);

time = [Ts:Ts:length(vel)*Ts];

pars;

% 8=====================================D
% ESTIMATE
% 8=====================================D

% MODEL

% load par_e
% par0 = [100 0.5 30];

% xdata = [cur vel sign(vel)];
% ydata = Jm * acc;

% fct = @(par,xdata) par(1) * xdata(:,1) - par(2) * xdata(:,2) - par(3) * xdata(:,3);

% [par, resnorm, ~, exitflag, output] = lsqcurvefit(fct,par0,xdata,ydata,[0 0 0],[300 300 300]);
% x0 = [0; vel(1)];
% e = @(par) sum((vel'-motor_sim(cur, Jm, x0, par(1), par(2), par(3))).^2);

% par = particleswarm(e,3,[0 0 0],[300 300 300]);

par = [cur -vel -sigmoid(vel,sigmoidpar)] \ [Jm*acc];
%par = pinv([cur -vel -sigmoid(vel,sigmoidpar)]) * [Jm * acc];
%par = [cur -vel -sigmoid(vel,sigmoidpar) -sigmoid(vel,sigmoidpar).*exp(-abs(vel./vs))] \ [Jm*acc];

kt    = par(1);
b     = par(2);
tau_c = par(3);
%tau_s = par(4);

simulate_it;

% 8=====================================D
% PLOT
% 8=====================================D

plot(time,vel,time,x(2,1:end-1));

ylabel('Velocity');
grid on;
legend('Measured', 'Simulated')

% figure

% plot(x(2,1:end-1), tau_f, '.');
% xlabel('velocity')
% ylabel('friction torque')
% grid on

disp('MSE:')
disp(immse(x(2,2:end)',vel))

%save par_s kt b tau_c;

% figure

% vel_sin  = [];
% cur_sin  = [];

% for n = 4:length(names)
% 	vel_sin = cat(1,vel_sin,getSignal(m1(n),'velocity'));
% 	cur_sin = cat(1,cur_sin,getSignal(m1(n),'current'));
% end

% t_sin= [Ts:Ts:length(vel_sin)*Ts];

% plot(t_sin, vel_sin, t_sin, 100*cur_sin);
% xlabel('time');
% legend('Velocity', '100 x current');
% grid on

% par