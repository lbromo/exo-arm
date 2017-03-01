function [tau_f x vel time] = test_pars_feb(name,joint, par)

% 8=====================================D
% LOAD DATA
% 8=====================================D

par = [par.kt par.b par.tau_c par.sigmoidpar];

if joint == 1
    jname = 'elbow';
elseif joint == 2
    jname = 'shoulder';     
end

fm1 = strcat('logs/',jname,'/motor1_',name,'.log');

m1 = importdata(fm1);

ang_id = find(~cellfun(@isempty,strfind(m1.colheaders,'angle')));
vel_id = find(~cellfun(@isempty,strfind(m1.colheaders,'velocity')));
cur_id = find(~cellfun(@isempty,strfind(m1.colheaders,'current')));
time_id = find(~cellfun(@isempty,strfind(m1.colheaders,'time')));

vel  = m1.data(:,vel_id);
time = m1.data(1:end-1,time_id);

Ts = 0.01;

cur  = m1.data(1:end-1,cur_id);
vel  = vel(1:end-1);

pars

kt    = par(1);
b     = par(2);
tau_c = par(3);
sigmoidpar = par(4);
%tau_s = par(4);

simulate_it

% 8=====================================D
% PLOT
% 8=====================================D

plot(time,vel,time,x(2,1:end-1));
if joint == 1
	title('Elbow');
elseif joint == 2
	title('Shoulder');
end

ylabel('Velocity');
grid on;
legend('Measured', 'Simulated')

disp('MSE:')
disp(immse(x(2,:)',m1.data(:,vel_id)))

end