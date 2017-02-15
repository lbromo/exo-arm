function [par tau_f x] = parest_feb(name, joint)

% if joint == 'shoulder'
%     amps_sq = 0.3;
%     amps_sw = amps_sq;
% elseif joint == 'elbow'
%     amps_sq = [0.1 0.15 0.2 0.3];
%     amps_sw = [0.1 0.2 0.3];
% end

% 8=====================================D
% LOAD DATA
% 8=====================================D

if joint == 1
    jname = 'elbow';
elseif joint == 2
    jname = 'shoulder';
end

fm1 = strcat('logs/',jname,'/motor1_',name,'.log');
fm2 = strcat('logs/',jname,'/motor2_',name,'.log');
fin = strcat('logs/',jname,'/input_',name,'.log');

m1 = importdata(fm1);
m2 = importdata(fm2);
in = importdata(fin);

ang_id = find(~cellfun(@isempty,strfind(m1.colheaders,'angle')));
vel_id = find(~cellfun(@isempty,strfind(m1.colheaders,'velocity')));
cur_id = find(~cellfun(@isempty,strfind(m1.colheaders,'current')));
time_id = find(~cellfun(@isempty,strfind(m1.colheaders,'time')));

vel  = m1.data(:,vel_id);
time = m1.data(1:end-1,time_id);

Ts = time(2)-time(1);
acc = diff(vel,1,1)./Ts;
acc = smooth(smooth(acc));

cur  = m1.data(1:end-1,cur_id);
vel  = vel(1:end-1);

% 8=====================================D
% ESTIMATE
% 8=====================================D


if joint == 2
    JG2 = 0.282e-4;      % [kg*m2] Gear inertia
    JM2 = 1210e-7;       % [kg*m2] Motor inertia (shoulder flex/ext)
    JA2 = 539919.92e-9; %4722727.19e-9; % [kg*m2]
    Jm  = (JG2+JM2) * 50^2 + JA2;%181e-3; 
elseif joint == 1
    JG3 = 0.282e-4;      % [kg*m2] Gear inertia
    JM3 = 181e-7;        % [kg*m2] Motor inertia (elbow flex/ext)
    JA3 = 1562955.32e-9; % [kg*m2]
    Jm = (JG3+JM3)*50^2+JA3;
end

vs = 10;
sigmoidpar = 1;

par = [cur -vel -sigmoid(vel,sigmoidpar) -sigmoid(vel,sigmoidpar).*exp(-abs(vel./vs))] \ [Jm*acc];
%par = [cur -vel -sigmoid(vel,sigmoidpar)] \ [Jm*acc];


kt    = par(1);
b     = par(2);
tau_c = par(3);
tau_s = par(4);

% 8=====================================D
% SIMULATE
% 8=====================================D
N = length(cur);

x0 = [0 vel(1)];
x = zeros(2,N);
tau_f = zeros(1,N);
x(:,1) = x0;


for t = 1:N
    dx1 = x(2,t);
    tau_m = kt * cur(t);
    fv = b * dx1;
    fc = tau_c * sigmoid(dx1,sigmoidpar);
    fs = tau_s * sigmoid(dx1,sigmoidpar)*exp(-abs(dx1/vs));

    tau_f(t) = fv + fc + fs;

    dx2 = 1/Jm * (tau_m - tau_f(t));
    x(:,t+1) = x(:,t) + Ts * [dx1;dx2];
end

% 8=====================================D
% PLOT
% 8=====================================D

plot(time,vel,time,x(2,1:end-1));
ylabel('Velocity');
grid on;
legend('Measured', 'Simulated')

disp('MSE:')
disp(immse(x(2,:)',m1.data(:,vel_id)))
