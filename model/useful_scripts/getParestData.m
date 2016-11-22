function [in m1 m2] = getParestData(name)

	fm1 = strcat('logs/motor1_',name,'.log');
	fm2 = strcat('logs/motor2_',name,'.log');
	fin = strcat('logs/input_',name,'.log');

	m1 = importdata(fm1);
	m2 = importdata(fm2);
	in = importdata(fin);


end