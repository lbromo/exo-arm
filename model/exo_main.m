% -----------------------------------------
% DYNAMIC MECHANICAL MODEL 
% -----------------------------------------
% choose  abe = 1 to run ODE SOLVER
%         abe = 2 to run FORWARD EULER METHOD - test of method 
%         abe = 3 to run FORWARD EULER METHOD - for verification of model 

clear all;
clc;
abe = 3;
% -----------------------------------------
% LOAD DATA AND PARAMETERS
% -----------------------------------------
ParametersScript 

m2 = importdata('both/motor1_both_sine2.log'); %time,angle,velocity,current
m1 = importdata('both/motor2_both_sine2.log'); %time,angle,velocity,current
in = importdata('both/input_both_sine2.log'); %on1,dir1,pwm1,on2,dir2,pwm2

%m1 and m2
time_id = find(~cellfun(@isempty,strfind(m1.colheaders,'time')));
ang_id = find(~cellfun(@isempty,strfind(m1.colheaders,'angle')));
vel_id = find(~cellfun(@isempty,strfind(m1.colheaders,'velocity')));
cur_id = find(~cellfun(@isempty,strfind(m1.colheaders,'current')));

time = (m1.data(:,time_id)- m1.data(1,time_id))./1000; %to start from 0 and in ms
angle_m1  = (m1.data(:,ang_id)).*0.01745329252; %from angle to rad
vel_m1  = (m1.data(:,vel_id))/N; %from before to after gear
cur_m1 = m1.data(:,cur_id).*params.kt1*N; %to get torque input and after gears
angle_m2  = (m2.data(:,ang_id)).*0.01745329252; %from angle to rad 
vel_m2  = (m2.data(:,vel_id))/N; %from before to after gear
cur_m2 = m2.data(:,cur_id).*params.kt2*N; %to get torque input and after gears

%in  
on1_id = find(~cellfun(@isempty,strfind(in.colheaders,'on1')));
dir1_id = find(~cellfun(@isempty,strfind(in.colheaders,'dir1')));
pwm1_id = find(~cellfun(@isempty,strfind(in.colheaders,'pwm1')));
on2_id = find(~cellfun(@isempty,strfind(in.colheaders,'on2')));
dir2_id = find(~cellfun(@isempty,strfind(in.colheaders,'dir2')));
pwm2_id = find(~cellfun(@isempty,strfind(in.colheaders,'pwm2')));

% Switch because morten is dumb
on_m2 = in.data(:,on1_id);
dir_m2  = in.data(:,dir1_id);
pwm_m2  = in.data(:,pwm1_id);
on_m1 = in.data(:,on2_id);
dir_m1  = in.data(:,dir2_id);
pwm_m1  = in.data(:,pwm2_id);

%% 
% ----------------------------------------------
%  ODE SOLVER
% -----------------------------------------------

if abe == 1
x0 = [
      1
      1;
      0;
      0;
];

u = [
       0;
       0
];

t_span = [0 5];

 [t,x] = ode113(@exo_dynamic_model, t_span, x0, [], u, params);


%So we have way to many samples, and no "specific" sampling time..
%We "create" one by taking unique time samples with a 0.01 spacing
[C,ia,ic] = uniquetol(t, 0.001);

theta1 = x(ia,1);
theta2 = x(ia,2);

theta = [theta1 theta2];

params.arm.plot(theta, 'fps', length(theta)/t_span(end), 'loop');

end

%% 
% ----------------------------------------------
%  FORWARD EULER METHOD (Discrete model) 
%  test of method
% -----------------------------------------------
if abe == 2
%Ts = 0.01;
%Tend = 20 / Ts;
xd = [0;0;0;0];

Ts = zeros(1, length(time(1:end-10)));
for a = 1:length(time(1:end-10))
    Ts(a)=time(a+1)-time(a);
end
u= zeros(2,length(time(1:end-10)))
%u = zeros(2, Tend);

u(1, 200:400) = 0.1;
u(2, 1:end) = 0;

%xd(:, 1) = [1; 1; 0; 0]

%params.vm = [0.5, 0.55]

%for k = 1:Tend
for k = 1:length(time(1:end-10))
  %if(mod(k,10) == 0)
  %  params.arm.plot(xd(1:2,k)', 'fps', 1/(Ts*10))
  %end

  %if (k > 1/Ts)
  %  u = [0; 0];
  %end
  xd(:,k+1) = xd(:,k) + Ts(k)*f(xd(:,k), u(:,k), params);
end

%time=[0:Ts:20];
subplot(2,1,1)
plot(time(1:end-10),xd(1,1:end-1),'g')
hold on
plot(time(1:end-10),xd(2,1:end-1),'r')
subplot(2,1,2)
plot(time(1:end-10),u(1,:))
end
%% 
% ----------------------------------------------
%  FORWARD EULER METHOD (Discrete model) 
%  for verification of model
% -----------------------------------------------
if abe == 3

xd = [angle_m1(1);angle_m2(1);vel_m1(1);vel_m2(1)]; %angle start
acc=zeros(2, length(time(1:end-10)));
u = zeros(2, length(time(1:end-10))); %to be sure that the lengths of the vectors are the same "length(time(1:end-10))" are used everywhere
u(1, 1:end) = cur_m1(1:length(time(1:end-10)));
u(2, 1:end) = cur_m2(1:length(time(1:end-10)));

Ts = zeros(1, length(time(1:end-10)));
for a = 1:length(time(1:end-10))
    Ts(a)=time(a+1)-time(a);
end

for k = 1:length(time(1:end-10))
  xd(:,k+1) = xd(:,k) + Ts(k)*f(xd(:,k), u(:,k), params, acc(:,k));
  acc(:,k+1)=(xd(3:4,k+1) - xd(3:4,k))/Ts(k);
end

 
%simulated
subplot(3,2,1)
plot(time(1:end-10),xd(1,1:end-1),'g') %angle plot m1
hold on
plot(time(1:end-10),xd(2,1:end-1),'r') %angle plot m2
title('simulated rad')  
grid on;

subplot(3,2,3)
plot(time(1:end-10),xd(3,1:end-1),'g') %vel plot m1
hold on
plot(time(1:end-10),xd(4,1:end-1),'r') %vel plot m2
title('simulated rad/s')
ylim([-3 3])
grid on;

subplot(3,2,5)
plot(time(1:end-10),u(1,:),'g') %in plot m1
hold on
plot(time(1:end-10),u(2,:),'r') %in plot m2
title('inputs')
grid on;

%measured
subplot(3,2,2)
plot(time(1:end-10),angle_m1(1:length(time(1:end-10))),'g') %angle plot m1
hold on
plot(time(1:end-10),angle_m2(1:length(time(1:end-10))),'r') %angle plot m2
title('measured rad')
grid on;

subplot(3,2,4)
plot(time(1:end-10),vel_m1(1:length(time(1:end-10))),'g') %vel plot m1
hold on
plot(time(1:end-10),vel_m2(1:length(time(1:end-10))),'r') %vel plot m2
title('measured rad/s')
ylim([-3 3])
grid on;

end




