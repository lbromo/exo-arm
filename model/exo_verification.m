% -----------------------------------------
% DYNAMIC MECHANICAL MODEL verification
% -----------------------------------------
% choose  abe = 1 to run ODE SOLVER (does  not work rigth now)
%         abe = 2 to run FORWARD EULER METHOD - test of method 
%         abe = 3 to run FORWARD EULER METHOD - for verification of model 
%                       - monkey1 = 1 or 0    parameter estimate or not
%                       - monkey2 = 1 or 0    save data in csv file or not
clear all;
close all;
abe = 3;
monkey1=0; 
monkey2 =1;
addpath('useful_scripts')
addpath('old_scripts')
addpath('system_matrices')
addpath('verification')
ParametersScript  %model parameters
load_data   %data for verification
%% 
% ----------------------------------------------
%  ODE SOLVER
% -----------------------------------------------
if abe == 1
ode_solver_mech_model
end

%% 
% ----------------------------------------------
%  FORWARD EULER METHOD (Discrete model) 
%  test of method
% -----------------------------------------------
if abe == 2
forward_euler_test
end
%% 
% ----------------------------------------------
%  FORWARD EULER METHOD (Discrete model) 
%  for verification of model
% -----------------------------------------------
if abe == 3
global x0;
xd = [angle_m1(1);angle_m2(1);vel_m1(1);vel_m2(1)]; %angle and vel init
x0=xd;
u = zeros(2, length(time)); %to be sure that the lengths of the vectors are the same "length(time(1:end-10))" are used everywhere
u(1, 1:end) = cur_in_m1;%(1:length(time(1:end-10)));
u(2, 1:end) = cur_in_m2;%(1:length(time(1:end-10)));
%--------------------------------------------------------------------
%parameter estimate or not
if monkey1 == 1
 par_to_get=[params.hast];% params.cm params.vm  params.sigmoidpar params.hast
 ydata=[vel_m1 vel_m2]'; 
 [X, resnorm] = lsqcurvefit(@parest_forward, par_to_get, u, ydata, [0 0])
 %params.cm=X(1:2);
 %params.vm=X(3:4);
%params.sigmoidpar=X(5:6);
params.hast=X(1:2);
end
%--------------------------------------------------------------------
for k = 1:length(time(1:end-1))  %forward euler
  xd(:,k+1) = xd(:,k) + Ts(k)*f(xd(:,k), u(:,k), params);
end

residual_error=sum(([xd(3,:) xd(4,:)] -[vel_m1; vel_m2]').^2) %squared 2 norm error
mse = goodnessOfFit([xd(3,:) xd(4,:)]', [vel_m1; vel_m2], 'NRMSE')
figure(1)
subplot(3,1,1)
plot(time,xd(1,:),'--g') %angle plot m1 sim
hold on
plot(time,xd(2,:),'--r') %angle plot m2 sim
plot(time,angle_m1,'g') %angle plot m1 meas
plot(time,angle_m2,'r') %angle plot m2 meas
title('simulated and measured rad')  
%ylim([0.6, 1.4])
grid on;
xlabel('time');
ylabel('rad');
%xlim([0, 2])

subplot(3,1,2)
plot(time,xd(3,:),'--g') %vel plot m1 sim
hold on
plot(time,xd(4,:),'--r') %vel plot m2 sim
plot(time,vel_m1,'g') %vel plot m1 meas 
plot(time,vel_m2,'r') %vel plot m2 meas
title('simulated and measured rad/s')
%ylim([0.6, 1.4])
grid on;
xlabel('time');
ylabel('rad/s'); 
%xlim([0, 2])

subplot(3,1,3)
plot(time,u(1,:),'g') %in plot m1
hold on
plot(time,u(2,:),'r') %in plot m2
title('inputs')
grid on;
xlabel('time');
ylabel('Nm');
%xlim([0, 2])
%ylim([0.6, 1.4])
figure(2)
subplot(1,2,1)
plot(time,pwm_m1)
hold on 
plot(time,pwm_m2)
subplot(1,2,2)
plot(time,cur_in_m1)
hold on 
plot(time,cur_in_m2)
ylim([0.6, 1.4])
% ----------------------------------------------
%  Save data in csv file or not
% ----------------------------------------------
if monkey2 == 1
    T=table(time, u(1,:)',u(2,:)', xd(1,:)', xd(2,:)', xd(3,:)', xd(4,:)', angle_m1, angle_m2, vel_m1, vel_m2, cur_m1, cur_m2, 'VariableNames',{'time','in_m1','in_m2','si_angm1','si_angm2','si_velm1','si_velm2','me_angm1','me_angm2','me_velm1','me_velm2','me_torm1','me_torm2'});
    writetable(T,'/home/bjarkenrp/Documents/exo-rapport/contents/mech_verification/figs/sim_and_meas_mechmodel_sin4.csv');
end
end