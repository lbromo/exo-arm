function [tau_f x] = test_pars_feb(name,joint, par)

% 8=====================================D
% LOAD DATA
% 8=====================================D

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

Ts = time(2)-time(1);
acc = diff(vel,1,1)./Ts;
acc = smooth(smooth(acc));

cur  = m1.data(1:end-1,cur_id);
vel  = vel(1:end-1);

if joint == 2
    N = 50;
    JG2 = 0.282e-4;      % [kg*m2] Gear inertia
    JM2 = 1210e-7;       % [kg*m2] Motor inertia (shoulder flex/ext)
    JA2 = 539919.92e-9; %4722727.19e-9; % [kg*m2]
    Jm  = (JG2+JM2)*N^2 + JA2;%181e-3; 
elseif joint == 1
    N = 50;
    JG3 = 0.282e-4;      % [kg*m2] Gear inertia
    JM3 = 181e-7;        % [kg*m2] Motor inertia (elbow flex/ext)
    JA3 = 1562955.32e-9; % [kg*m2]
    Jm = (JG3+JM3)*N^2+JA3;
end

kt    = par(1);
b     = par(2);
tau_c = par(3);
%tau_s = par(4);

vs = 1;
vs2 = 18;
sigmoidpar = 1;

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

end