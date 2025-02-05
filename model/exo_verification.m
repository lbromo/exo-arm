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
monkey1=1; 
monkey2 =0;
addpath('useful_scripts')
addpath('old_scripts')
addpath('system_matrices')
addpath('verification')
clear globals;
global params;
params = ParametersScript;  %model parameters
load_data;   %data for verification
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
	x0 = [angle_m1(1);angle_m2(1);vel_m1(1);vel_m2(1)]; %angle and vel init
	xd=x0;
	u = zeros(2, length(time)); %to be sure that the lengths of the vectors are the same "length(time(1:end-10))" are used everywhere
	u(1, 1:end) = cur_in_m1;%(1:length(time(1:end-10)));
	u(2, 1:end) = cur_in_m2;%(1:length(time(1:end-10)));
	%--------------------------------------------------------------------
	%parameter estimate or not
	if monkey1 == 1
	 par_to_get=[params.cm params.vm  params.sigmoidpar];% params.cm params.vm  params.sigmoidpar params.hast
	 ydata=[vel_m1 vel_m2]'; %' angle_m1 angle_m2]'; 
	 [X, resnorm] = lsqcurvefit(@parest_forward, par_to_get, u, ydata, [0 0 0 0 0 0]);
	 params.cm=X(1:2);
	 params.vm=X(3:4);
	 params.sigmoidpar=X(5:6);
	% params.hast=X(1:2);
	end
	%--------------------------------------------------------------------
	for k = 1:length(time(1:end-1))  %forward euler
	  xd(:,k+1) = xd(:,k) + Ts(k)*f(xd(:,k), u(:,k), params);
	end

	residual_error=sum(([xd(3,:) xd(4,:)] -[vel_m1; vel_m2]').^2) %squared 2 norm error
	nmse = goodnessOfFit([xd(3,:) xd(4,:)]', [vel_m1; vel_m2], 'NMSE')

	figure(1)
	ax(1) = subplot(3,2,1);
	plot(time,xd(1,:)) %angle plot m1 sim
	hold on
	plot(time,angle_m1) %angle plot m1 meas
	title('simulated and measured rad')  
	%ylim([0.6, 1.4])
	grid on;
	xlabel('time');
	ylabel('rad');

	ax(2) = subplot(3,2,2);
	plot(time,xd(2,:)) %angle plot m2 sim
	hold on;
	plot(time,angle_m2) %angle plot m2 meas
	%xlim([0, 2])
	title('simulated and measured rad')  
	%ylim([0.6, 1.4])
	grid on;
	xlabel('time');
	ylabel('rad');

	ax(3) = subplot(3,2,3);
	plot(time,xd(3,:)) %vel plot m1 sim
	hold on
	plot(time,vel_m1) %vel plot m1 meas 
	title('simulated and measured rad/s')
	grid on;
	xlabel('time');
	ylabel('rad/s'); 

	ax(4) = subplot(3,2,4);
	plot(time,xd(4,:)) %vel plot m2 sim
	hold on
	plot(time,vel_m2) %vel plot m2 meas
	title('simulated and measured rad/s')
	legend('Sim','meas')
	%ylim([0.6, 1.4])
	grid on;
	xlabel('time');
	ylabel('rad/s'); 
	%xlim([0, 2])

	ax(5) = subplot(3,2,5);
	plot(time,u(1,:),'g') %in plot m1
	title('input')
	grid on;
	xlabel('time');
	ylabel('Nm');

	ax(6) = subplot(3,2,6);
	plot(time,u(2,:),'r') %in plot m2
	title('input')
	grid on;
	xlabel('time');
	ylabel('Nm');

	linkaxes(ax, 'x');

	%xlim([0, 2])
	%ylim([0.6, 1.4])
	% figure(2)
	% subplot(1,2,1)
	% plot(time,pwm_m1)
	% hold on 
	% plot(time,pwm_m2)
	% subplot(1,2,2)
	% plot(time,cur_in_m1)
	% hold on 
	% plot(time,cur_in_m2)
	% ylim([0.6, 1.4])

	% ----------------------------------------------
	%  Save data in csv file or not
	% ----------------------------------------------
	if monkey2 == 1
	    T=table(time, u(1,:)',u(2,:)', xd(1,:)', xd(2,:)', xd(3,:)', xd(4,:)', angle_m1, angle_m2, vel_m1, vel_m2, cur_m1, cur_m2, 'VariableNames',{'time','in_m1','in_m2','si_angm1','si_angm2','si_velm1','si_velm2','me_angm1','me_angm2','me_velm1','me_velm2','me_torm1','me_torm2'});
	    %writetable(T,'/home/morten/Documents/exo-rapport/contents/mech_verification/figs/sin_ver_w_unfitted_data.csv');
	end
end