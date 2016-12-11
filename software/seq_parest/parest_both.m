% function [par MSE sq_vel sin_vel] = parest_both(sq_name, sq_amps, sin_name, sin_amps, per, old)
function [par MSE sq_vel sin_vel] = parest_both(sq_name, sq_amps, sin_name, sin_amps, per, old, elbow)

ang_sig = [];
cur_sig = [];
vel_sig = [];
time_sig = [];

t_old = 0; % For use with elbow measurements that were made one at a time

% 8=====================================D
% Generation of file names + main loop
% 8=====================================D
nm_len = length([sq_amps sin_amps]);

sq_nm = {};
for i = 1:length(sq_amps)
	sq_nm{i} = [sq_name num2str(sq_amps(i))];
end

sin_nm = {};
for i = 1:length(sin_amps)
	sin_nm{i} = [sin_name num2str(sin_amps(i))];
end

if ~exist('old')
	old = 0;
end

NAMES = [sq_nm sin_nm];

for i = 1:nm_len

% 8=====================================D
% Signal properties
% 8=====================================D
	SAMPLE_F = 100; % Hz
	PULSE_PERIOD = per; % s
	PERIOD_SAMPLE = SAMPLE_F*PULSE_PERIOD;

% 8=====================================D
% LOAD DATA
% 8=====================================D
	[in m1 m2] = getParestData(NAMES{i},old);

	% Find the data in the structs
	ang_id = find(~cellfun(@isempty,strfind(m1.colheaders,'angle')));
	vel_id = find(~cellfun(@isempty,strfind(m1.colheaders,'velocity')));
	cur_id = find(~cellfun(@isempty,strfind(m1.colheaders,'current')));
	time_id = find(~cellfun(@isempty,strfind(m1.colheaders,'time')));

	% Get all the vectors!
	angle = m1.data(:,ang_id);
	thetadot = m1.data(:,vel_id);
	current = m1.data(:,cur_id);
	if elbow == 1
		time = m1.data(:,time_id) + t_old;
		t_old = time(end);
	else
		time = m1.data(:,time_id);
	end

	% Differentiate speed to get acceleration
	Ts = time(2)-time(1);
	thetadotdot = diff(thetadot,1,1)./Ts;

	%Figure out how many periods of the signal are available
	SEQ_LEN = floor(length(thetadotdot)/PERIOD_SAMPLE);


	if SEQ_LEN > 0

		angle_shortened = angle(1:PERIOD_SAMPLE*SEQ_LEN);
		current_shortened = current(1:PERIOD_SAMPLE*SEQ_LEN);
		time_shortened = time(1:PERIOD_SAMPLE*SEQ_LEN);
		thetadot_shortened = thetadot(1:PERIOD_SAMPLE*SEQ_LEN);
		thetadotdot_shortened = thetadotdot(1:PERIOD_SAMPLE*SEQ_LEN);

		ang = reshape(angle_shortened, PERIOD_SAMPLE, SEQ_LEN);
		cur = reshape(current_shortened, PERIOD_SAMPLE, SEQ_LEN);
		vel = reshape(thetadot_shortened, PERIOD_SAMPLE, SEQ_LEN);
		acc = reshape(thetadotdot_shortened, PERIOD_SAMPLE, SEQ_LEN);
		t_v = time(1:PERIOD_SAMPLE);

		ang_mean{i} = mean(ang,2); 
		cur_mean{i} = mean(cur,2);
		vel_mean{i} = mean(vel,2);
		acc_mean{i} = mean(acc,2);
	
	else
		ang_mean{i} = ang(1:end-2)';
		cur_mean{i} = current(1:end-2)';
		vel_mean{i} = thetadot(1:end-2)';
		acc_mean{i} = thetadotdot(1:end-1)';

	end

	ang_sig = [ang_sig angle'];
	cur_sig = [cur_sig current'];
	vel_sig = [vel_sig thetadot'];
	time_sig = [time_sig time'];

	if i == length(sq_amps)
		t_hack = time_sig(end);
		l_hack = length(time_sig);
	end


end

time_sig(l_hack+1:end) = time_sig(l_hack+1:end)+t_hack;

ang_total = reshape(cell2mat(ang_mean),1,i*length(ang_mean{i}))';
cur_total = reshape(cell2mat(cur_mean),1,i*length(cur_mean{i}))';
vel_total = reshape(cell2mat(vel_mean),1,i*length(vel_mean{i}))';
acc_total = reshape(cell2mat(acc_mean),1,i*length(acc_mean{i}))';

% 8=====================================D
% Estimate parameters
% 8=====================================D

	if elbow == 0
		JG2 = 0.282e-4;      % [kg*m2] Gear inertia
		JM2 = 1210e-7;       % [kg*m2] Motor inertia (shoulder flex/ext)
		JA2 = 4722727.19e-9; % [kg*m2]
		Jm  = JG2+JM2+JA2;%181e-3; 
	else
		JG3 = 0.282e-4;      % [kg*m2] Gear inertia
		JM3 = 181e-7;        % [kg*m2] Motor inertia (elbow flex/ext)
		JA3 = 1562955.32e-9; % [kg*m2]
		Jm = JG3+JM3+JA3;
	end
% Extra nasty directional viscous friction!
	par = [cur_total -(sign(vel_total)+1).*vel_total -sign(vel_total).*vel_total -sign(vel_total)]\[Jm * acc_total];
%	par = [cur_total -vel_total -sign(vel_total)]\[Jm * acc_total];

	kt    = par(1);
%	b     = par(2)*.45;
%	b_ad  = par(3)*.45;
%	tau_e = par(4)*1.25;
	b     = par(2);
	b_ad  = par(3);
	tau_e = par(4);
% 8=====================================D
% SIMULATE
% 8=====================================D
	N = length(cur_sig);

	x0 = [0 vel_sig(1)];
	x = zeros(2,N);
	x(:,1) = x0;

	for t = 1:N
		dx1 = x(2,t);

		tau_m = kt * cur_sig(t);
		tau_f = ((sign(dx1)+1)*b + sign(dx1)*b_ad)*dx1 + sign(dx1) * tau_e;
%		tau_f = dx1*b + sign(dx1) * tau_e;
		dx2 = 1/Jm * (tau_m - tau_f);

		x(:,t+1) = x(:,t) + Ts * [dx1;dx2];
	end

% 8=====================================D
% PLOT
% 8=====================================D
	figure;
	ax(1) = subplot(211);

	if elbow == 0
		offset = 12;
	else
		offset = 0;
	end

	plot(time_sig(1:l_hack+offset),vel_sig(1:l_hack+offset),'b');
	hold on;
	grid on;
	plot(time_sig(1:l_hack+offset),x(2,1:l_hack+offset),'r'); 
	hold on;
	grid on;
	ylabel('Velocity');
	legend('Measured', 'Simulated')

	ax(2) = subplot(212);
	plot(time_sig(l_hack+offset:end),vel_sig(l_hack+offset:end),'b');
	hold on;
	grid on;
	plot(time_sig(l_hack+offset:end),x(2,(l_hack+offset:end-1)),'r'); 
	hold on;
	grid on;
	ylabel('Velocity');
	legend('Measured', 'Simulated')

	linkaxes(ax, 'x');

	sq_vel{1} = time_sig(1:l_hack+offset);
	sq_vel{2} = vel_sig(1:l_hack+offset);
	sq_vel{3} = x(2,1:l_hack+offset);

	sin_vel{1} = time_sig(l_hack+offset:end);
	sin_vel{2} = vel_sig(l_hack+offset:end);
	sin_vel{3} = x(2,(l_hack+offset:end-1));

	MSE = immse(x(2,2:end),vel_sig);

end
