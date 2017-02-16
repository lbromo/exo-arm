function [par tau_f x data] = parest_feb(name, joint)

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
    jname = 'elbow/';
elseif joint == 2
    jname = 'shoulder/';
end

fm1 = strcat('logs/',jname,'motor1_',name,'.log');
fm2 = strcat('logs/',jname,'motor2_',name,'.log');
fin = strcat('logs/',jname,'input_',name,'.log');

m1 = importdata(fm1);
m2 = importdata(fm2);
in = importdata(fin);

ang_id = find(~cellfun(@isempty,strfind(m1.colheaders,'angle')));
vel_id = find(~cellfun(@isempty,strfind(m1.colheaders,'velocity')));
cur_id = find(~cellfun(@isempty,strfind(m1.colheaders,'current')));
time_id = find(~cellfun(@isempty,strfind(m1.colheaders,'time')));

vel  = m1.data(:,vel_id);
time = m1.data(1:end-1,time_id);

Ts = time(3)-time(2)
acc = diff(vel,1,1)./Ts;
acc = smooth(smooth(acc));

cur  = m1.data(1:end-1,cur_id);
vel  = vel(1:end-1);

data = [time vel cur];

% 8=====================================D
% ESTIMATE
% 8=====================================D

pars

%par = [cur -vel -sigmoid(vel,sigmoidpar) -sigmoid(vel,sigmoidpar).*exp(-abs(vel./vs)) -sigmoid(vel,sigmoidpar).*exp(-abs(vel./vs2))] \ [Jm*acc];
%par = [cur -vel -sigmoid(vel,sigmoidpar) -sigmoid(vel,sigmoidpar).*exp(-abs(vel./vs))] \ [Jm*acc];
%par = [cur -vel -sigmoid(vel,sigmoidpar)] \ [Jm*acc];


kt    = par(1);
b     = par(2);
tau_c = par(3);
tau_s = par(4);
%tau_s = tau_c * 0.2;

simulate_it

% 8=====================================D
% PLOT
% 8=====================================D

plot(time,vel,time,x(2,1:end-1));

ylabel('Velocity');
grid on;
legend('Measured', 'Simulated')

disp('MSE:')
disp(immse(x(2,:)',m1.data(:,vel_id)))
