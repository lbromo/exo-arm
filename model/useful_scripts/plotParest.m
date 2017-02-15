function plotParest(name, joint, fid)

	if ~exist('fid')
		fid = 1;
	end

	if joint == 0
		fm1 = strcat('logs/motor1_',name,'.log');
		fm2 = strcat('logs/motor2_',name,'.log');
		fin = strcat('logs/input_',name,'.log');
	elseif joint == 1
		fm1 = strcat('logs/elbow/motor1_',name,'.log');
		fm2 = strcat('logs/elbow/motor2_',name,'.log');
		fin = strcat('logs/elbow/input_',name,'.log');
	elseif joint == 2		
		fm1 = strcat('logs/shoulder/motor1_',name,'.log');
		fm2 = strcat('logs/shoulder/motor2_',name,'.log');
		fin = strcat('logs/shoulder/input_',name,'.log');
	end

	m1 = importdata(fm1);
	m2 = importdata(fm2);
	in = importdata(fin);

	if ishandle(fid)
		close(fid)
	end

	figure(fid)
	ax(1) = subplot(2,3,1);
	plot(m1.data(:,1), in.data(1:length(m1.data(:,1)),3))
	hold on;
	plot(m2.data(:,1), in.data(1:length(m2.data(:,1)),6))
	grid on;
	legend('Elbow', 'Shoulder')
	title('PWM Input')
	ylim([0 300])

	ax(2) = subplot(2,3,2);
	plot(m1.data(:,1), m1.data(:,2))
	hold on;
	plot(m2.data(:,1), m2.data(:,2))
	grid on;
	legend('Elbow', 'Shoulder')
	title('Angle')
	ylim([0 360])

	ax(3) = subplot(2,3,3);
	plot(m1.data(:,1), m1.data(:,3))
	hold on;
	plot(m2.data(:,1), m2.data(:,3))
	grid on;
	legend('Elbow', 'Shoulder')
	title('Velocity')
	% ylim([-2000 2000])

	ax(4) = subplot(2,3,4);
	plot(m1.data(:,1), m1.data(:,4))
	hold on;
	plot(m2.data(:,1), m2.data(:,4))
	grid on;
	legend('Elbow', 'Shoulder')
	title('Current')
	% ylim([0 10])

	ax(5) = subplot(2,3,5);
	plot(m1.data(:,1), in.data(1:length(m1.data(:,1)),2))
	hold on;
	plot(m1.data(:,1), in.data(1:length(m1.data(:,1)),5))
	grid on;
	legend('Elbow', 'Shoulder')
	title('Direction')
	ylim([0 2])

	ax(6) = subplot(2,3,6);
	plot(m1.data(:,1), in.data(1:length(m1.data(:,1)),1))
	hold on;
	plot(m1.data(:,1), in.data(1:length(m1.data(:,1)),4))
	grid on;
	legend('Elbow', 'Shoulder')
	title('ON')
	ylim([0 2])

	linkaxes(ax,'x')