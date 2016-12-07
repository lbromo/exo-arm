function [in m1 m2] = getParestData(name, old)

	if ~exist('old')
		old = 0;
	end

	fm1 = strcat('logs/motor1_',name,'.log');
	fm2 = strcat('logs/motor2_',name,'.log');
	fin = strcat('logs/input_',name,'.log');

	if old == 1
		fm1 = strcat('logs/old_logs/motor1_',name,'.log');
		fm2 = strcat('logs/old_logs/motor2_',name,'.log');
		fin = strcat('logs/old_logs/input_',name,'.log');
	elseif old == 2
		fm1 = strcat('/home/morten/Dropbox/exo-arm/logs/parest_logs/motor1_',name,'.log');
		fm2 = strcat('/home/morten/Dropbox/exo-arm/logs/parest_logs/motor2_',name,'.log');
		fin = strcat('/home/morten/Dropbox/exo-arm/logs/parest_logs/input_',name,'.log');		
	end

	m1 = importdata(fm1);
	m2 = importdata(fm2);
	in = importdata(fin);


end