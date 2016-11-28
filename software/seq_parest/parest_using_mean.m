clear all; close all;

	name = 'long_vel';

	[in m1 m2] = getParestData(name);

	% Find the data in the structs
	vel_id = find(~cellfun(@isempty,strfind(m1.colheaders,'velocity')));
	cur_id = find(~cellfun(@isempty,strfind(m1.colheaders,'current')));
	time_id = find(~cellfun(@isempty,strfind(m1.colheaders,'time')));

	% Get all the vectors!
	thetadot = m1.data(1000:end,vel_id);
	time = m1.data(1000:end,time_id);
	Ts = time(2)-time(1);
	current = m1.data(1000:end,cur_id);
	current = current - mean(current);

	% Differentiate speed to get acceleration
	thetadotdot = diff(thetadot,1,1)./Ts;

	PERIOD_SAMPLE = 100;
	SEQ_LEN = floor(length(current)/PERIOD_SAMPLE);
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

	
	% Solve for parameters
	Jm  = 181e-3; %kg m^3
	par = [cur_m -sign(vel_m) -vel_m]\(acc_m * Jm)
	kt  = par(1);
	f_c = par(2);
	f_v = par(3);

	% Simulate!
	x0 = [0 thetadot(1)];
	x = zeros(2,length(thetadotdot));
	x(:,1) = x0;

	for t = 1:length(thetadotdot)
		dx1 = x(2,t);
		tau_fc = f_c * sign(x(2,t));
		tau_fv = f_v * x(2,t);
		tau_m = kt * current(t);

		dx2 = 1/Jm * (tau_m - tau_fc - tau_fv);

		x(:,t+1) = x(:,t) + Ts * [dx1;dx2];
	end

	subplot(2,1,1);

	plot(time,thetadot);
	hold on;
	plot(time,x(2,:))
	grid on;
	ylabel('velocity');
	legend('Measured', 'Simulated');

	subplot(2,1,2);
	plot(time,current);
	ylabel('current');
	grid on;

MSE = immse(x(2,:),thetadot')/length(thetadotdot);
