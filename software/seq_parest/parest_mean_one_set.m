clear all; close all;

	names = [2:6];

	SAMPLE_F = 100; % Hz
	PULSE_PERIOD = 20; % s
	PERIOD_SAMPLE = SAMPLE_F*PULSE_PERIOD;

for i = 1:length(names)

%	name = sprintf('long_step%d%d.0',names(i),names(i));
%	name = sprintf('step_test_2_%d',names(i));
	name = sprintf('step_test_2_%d',names(i));

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

		cur_m{i} = mean(cur,2);
		vel_m{i} = mean(vel,2);
		acc_m{i} = mean(acc,2);
	
	else

		cur_m{i} = current(1:end-1)';
		vel_m{i} = thetadot(1:end-1)';
		acc_m{i} = thetadotdot(1:end-1)';
	end

	cur_sig{i} = current_shortened;
	vel_sig{i} = thetadot_shortened;
	time_sig{i} = time_shortened;
end

cur = reshape(cell2mat(cur_m),1,i*PERIOD_SAMPLE)';
vel = reshape(cell2mat(vel_m),1,i*PERIOD_SAMPLE)';
acc = reshape(cell2mat(acc_m),1,i*PERIOD_SAMPLE)';
cur_orig = reshape(cell2mat(cur_sig),1,i*PERIOD_SAMPLE*SEQ_LEN)';
vel_orig = reshape(cell2mat(vel_sig),1,i*PERIOD_SAMPLE*SEQ_LEN)';

for idx = 2:i
	time_sig{idx}(:) = time_sig{idx}(:) - (time_sig{idx}(1) - time_sig{idx-1}(end));
end

time = reshape(cell2mat(time_sig),1,i*PERIOD_SAMPLE*SEQ_LEN)';

N = length(cur_orig);

	Jm  = 181e-3; %kg m^3
% Extra nasty directional viscous friction!
	par = [cur -(sign(vel)+1).*vel -sign(vel).*vel -sign(vel)]\[Jm * acc];;
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

		tau_m = kt * cur_orig(t);
		tau_f = ((sign(dx1)+1)*b + sign(dx1)*b_ad)*dx1 + sign(dx1) * tau_e;
		dx2 = 1/Jm * (tau_m - tau_f);

		x(:,t+1) = x(:,t) + Ts * [dx1;dx2];
	end

	plot(time,vel_orig,'b');
	hold on;
	grid on;
	plot(time,x(2,2:end),'r'); 
	hold on;
	grid on;
	ylabel('velocity');
	legend('Measured', 'Simulated')

	MSE = immse(x(2,2:end),vel_orig');
