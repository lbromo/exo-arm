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

	% Solve for parameters
	Jm  = 181e-3; %kg m^3
	par = [current(1:end-1) -sign(thetadot(1:end-1)) -thetadot(1:end-1)]\(thetadotdot * Jm)
	kt  = par(1);
	f_c = par(2);
	f_v = par(3);

	%{ Estimate Jm in stead of kt
	kt = 0.0369;
	par = [thetadot(1:end-1) sign(thetadot(1:end-1)) -thetadotdot] \ (kt*current(1:end-1));
	Jm = -par(3);
	f_c = par(2);
	f_v = par(1);
	%}

	% Simulate!
	x0 = [0 thetadot(1)];
	x = zeros(2,length(thetadotdot));
	x(:,1) = x0;
	%current = linspace(-.02,.02,length(thetadotdot))

	for t = 1:length(thetadotdot)
		dx1 = x(2,t);
		tau_fc = f_c * sign(x(2,t));
		tau_fv = f_v * x(2,t);
		tau_m = kt * current(t);

%		if abs(tau_m) < abs(tau_fc)
%			tau_fc = tau_m - tau_fv;
%		else 
%			tau_fc = 0;
%		end
		dx2 = 1/Jm * (tau_m - tau_fc - tau_fv);

		x(:,t+1) = x(:,t) + Ts * [dx1;dx2];
	end


	subplot(2,1,1);
	plot(time,thetadot);
	hold on;
	plot(time,x(2,:))
%	plot(time,current*10000);
	grid on;
	ylabel('velocity');
	legend('Measured', 'Simulated');

	subplot(2,1,2);
	plot(time,current);
	ylabel('current');
	grid on;

	%{ Estimate Jm in stead of kt
	kt = 0.0369;
	par = [thetadot(1:end-1) sign(thetadot(1:end-1)) -thetadotdot] \ (kt*current(1:end-1));
	Jm = -par(3);
	f_c = par(2);
	f_v = par(1);
	%}

MSE = immse(x(2,:),thetadot')/length(thetadotdot);
