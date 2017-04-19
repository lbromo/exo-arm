function [in m1 m2] = getParestData(name, where)

	if ~exist('old')
		old = 0;
	end

	fm1 = strcat('logs/motor1_',name,'.log');
	fm2 = strcat('logs/motor2_',name,'.log');
	fin = strcat('logs/input_',name,'.log');

	if where == 1
		fm1 = strcat('logs/elbow/motor1_',name,'.log');
		fm2 = strcat('logs/elbow/motor2_',name,'.log');
		fin = strcat('logs/elbow/input_',name,'.log');
	elseif where == 2
		fm1 = strcat('logs/shoulder/motor1_',name,'.log');
		fm2 = strcat('logs/shoulder/motor2_',name,'.log');
		fin = strcat('logs/shoulder/input_',name,'.log');
	elseif where == 3
		fm1 = strcat('logs/both/motor1_',name,'.log');
		fm2 = strcat('logs/both/motor2_',name,'.log');
		fin = strcat('logs/both/input_',name,'.log');
	elseif where == 4
		fm1 = strcat('both/motor1_both_',name,'.log');
		fm2 = strcat('both/motor2_both_',name,'.log');
		fin = strcat('both/input_both_',name,'.log');
	end
	m1 = importdata(fm1);
	m2 = importdata(fm2);
	in = importdata(fin);


end