clear all; close all; 

% 8=====================================D
% GET ALL THE FILES
% 8=====================================D

ELBOW = 1;
SHOULDER = 2;

Ts = 0.01;
joint = ELBOW;


if joint == ELBOW % Elbow
	% names = {'rs_60_0.1', 'rs_60_0.2', 'rs_60_0.3', 'e_sin_no_0.6', 'e_sin_no_0.7'};
	names = {'new_elbow0.5', 'new_elbow0.6', 'new_elbow0.7', 'new_elbow_sw0.6', 'new_elbow_sw0.7'}; 
elseif joint == SHOULDER % shoulder
	names = {'rs_60_0.1', 'rs_60_0.3', 'rs_60_0.5', 's_sin_no_1.3', 's_sin_no_1.5'};
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
pos  = [];
offset = 0;

for n = 1:length(names)
	vel = cat(1,vel,getSignal(m1(n),'velocity'));
	cur = cat(1,cur,getSignal(m1(n),'current'));
	pos = cat(1,pos,getSignal(m1(n),'angle'));
	
	if n == 3
		sq_end = length(vel);
	end
end

acc = diff(smooth(vel),1,1)./Ts;

vel = vel(1:end-1);
cur = cur(1:end-1);
pos = pos(1:end-1); % [deg] on the output of gear
pos = pos * (2*pi)/360 * 50; % [rad] on gear input

time = [Ts:Ts:length(vel)*Ts];

% 8=====================================D
% FIND ACC == 0
% 8=====================================D

idx = find(abs(acc)==0);

v = vel(idx);
c = cur(idx);

% 8=====================================D
% ESTIMATE FRICTION
% 8=====================================D

par0 = [1 1 1];

fct = @(par,xdata) par(1) * xdata + par(2) * sigmoid(xdata,par(3));

[par,resnorm,residual,exitflag,output] = lsqcurvefit(fct,par0,v,c,[0 0 0]);


% 8=====================================D
% ESTIMATE Kt
% 8=====================================D

cur_f = fct(par,vel);

pars;

% p = [cur -cur_f] \ [Jm*acc];

f2 = @(par,xdata) par(1) * xdata(:,1) - par(2) * xdata(:,2);
%f2 = @(par,xdata) par * (xdata(:,1) -  xdata(:,2));

ydata = Jm * acc;
xdata = [cur, cur_f];

[p,resnorm,residual,exitflag,output] = lsqcurvefit(f2,[1 1],xdata,ydata,[0 0]);

kf = p(2);
b 	  = par(1) * kf;
tau_c = par(2) * kf;
sigmoidpar = par(3);
kt = p(1);


simulate_it

% 8=====================================D
% PLOT THAT SHIT
% 8=====================================D

ax(1) = subplot(311);

t = min(v):0.1:max(v);
tauf = fct([b tau_c sigmoidpar],t);
plot(v,c*kf,'.',t,tauf);
xlabel('Velocity');
ylabel('Friction Torque');
grid on;
legend('Measured', 'Simulated','Location','southeast')

ax(2) = subplot(312);

plot(time,vel,time,x(2,1:end-1));
xlabel('Time');
ylabel('Velocity');
grid on;
legend('Measured', 'Simulated','Location','southeast')

ax(3) = subplot(313);

plot(time,pos,time,x(1,1:end-1));
xlabel('Times');
ylabel('Angle');
grid on;
legend('Measured', 'Simulated','Location','northeast')


linkaxes(ax(2:3),'x')

if 		joint == 1
	title(ax(1),'Elbow');
elseif 	joint == 2
	title(ax(1),'Shoulder');
end

disp('N*MSE:')
%disp(exo_mse(x(2,2:end),vel))
disp(goodnessOfFit(x(2,2:end)',vel,'NMSE'));

% param.kt = kt;
% param.b =b;
% param.tau_c = tau_c;
% param.sigmoidpar = sigmoidpar;

% if joint == 1
% 	elbow = param
% 	save param_e elbow
% elseif joint == 2
% 	shoulder = param
% 	save param_s shoulder
% end
