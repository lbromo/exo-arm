clear all; close all;

	names = [3:8];

	SAMPLE_F = 100; % Hz
	PULSE_PERIOD = 10; % s
	PERIOD_SAMPLE = SAMPLE_F*PULSE_PERIOD;

	for i = 1:length(names)

%	name = sprintf('long_step%d%d.0',names(i),names(i));
	name = sprintf('step_test_3_%d',names(i));

	[in m1 m2] = getParestData(name);

	% Find the data in the structs
	vel_id = find(~cellfun(@isempty,strfind(m1.colheaders,'velocity')));
	cur_id = find(~cellfun(@isempty,strfind(m1.colheaders,'current')));
	time_id = find(~cellfun(@isempty,strfind(m1.colheaders,'time')));

	% Get all the vectors!
	thetadot = m1.data(:,vel_id);
	time = m1.data(:,time_id);
	Ts = time(2)-time(1);
	current = m1.data(:,cur_id);
	current = current;% - mean(current);

	% Differentiate speed to get acceleration
	thetadotdot = diff(thetadot,1,1)./Ts;


	N = length(thetadotdot);
	SEQ_LEN = floor(length(thetadotdot)/PERIOD_SAMPLE);

	if SEQ_LEN > 0

		current_shortened = current(1:PERIOD_SAMPLE*SEQ_LEN);
		time_shortened = time(1:PERIOD_SAMPLE*SEQ_LEN);
		thetadot_shortened = thetadot(1:PERIOD_SAMPLE*SEQ_LEN);
		thetadotdot_shortened = thetadotdot(1:PERIOD_SAMPLE*SEQ_LEN);

		cur = reshape(current_shortened, PERIOD_SAMPLE, SEQ_LEN);
		vel = reshape(thetadot_shortened, PERIOD_SAMPLE, SEQ_LEN);
		acc = reshape(thetadotdot_shortened, PERIOD_SAMPLE, SEQ_LEN);
		t_v = time(1:PERIOD_SAMPLE);

		cur_m = mean(cur,2);
		vel_m = mean(vel,2);
		acc_m = mean(acc,2);
	
	else

		cur_m = current(1:end-1)';
		vel_m = thetadot(1:end-1)';
		acc_m = thetadotdot(1:end-1)';
	end
			

	Jm  = 181e-3; %kg m^3
%	par = [cur_m -vel_m -sign(vel_m)]\[Jm * acc_m];
%	kt    = par(1);
%	b     = par(2);
%	tau_e = par(3);

% Extra nasty directional viscous friction!
	par = [cur_m -(sign(vel_m)+1).*vel_m -sign(vel_m).*vel_m -sign(vel_m)]\[Jm * acc_m];;
	kt    = par(1);
	b     = par(2);
	b_ad  = par(3);
	tau_e = par(4);


	
	% Simulate!
	x0 = [0 thetadot(1)];
	x = zeros(2,N);
	x(:,1) = x0;

	for t = 1:N
		dx1 = x(2,t);

		tau_m = kt * current(t);
		tau_f = ((sign(dx1)+1)*b + sign(dx1)*b_ad)*dx1 + sign(dx1) * tau_e;
		%tau_f = b * dx1 + sign(dx1) * tau_e;
		dx2 = 1/Jm * (tau_m - tau_f);

		x(:,t+1) = x(:,t) + Ts * [dx1;dx2];
	end

	M = length(names);	
	n = 2;
	m = ceil(M/n);
	ax(1) = subplot(m,n,i);
	time = time - time(1);

	
	plot(time,thetadot,'b');
	hold on;
	grid on;
	plot(time,x(2,:),'r'); 
	hold on;
	grid on;
	ylabel('velocity');
	legend('Measured', 'Simulated')

%	ax(2) = subplot(212);
%	plot(time,current);
%	ylabel('current');
%	hold on;
%	grid on;

	linkaxes(ax,'x');

	MSE(i) = immse(x(2,:),thetadot');

	pars{i} = par;

end

parmat = cell2mat(pars);
final_pars = mean(parmat(:,2:end),2);

figure(2);
bar(parmat);
%
MSE = sum(MSE);
save par.mat final_pars


