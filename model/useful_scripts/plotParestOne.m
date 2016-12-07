function plotParest(name, motor, fid)

	if ~exist('fid')
		fid = 1;
	end

	fm = strcat('logs/motor',sprintf('%d',motor),'_',name,'.log');
	fin = strcat('logs/input_',name,'.log');

	m = importdata(fm);
	in = importdata(fin);

	if ishandle(fid)
		close(fid)
	end

	figure(fid)
	ax(1) = subplot(2,3,1);
	plot(m.data(:,1), in.data(1:length(m.data(:,1)),3))
	grid on;
	legend('Elbow', 'Shoulder')
	title('PWM Input')
%	ylim([0 300])

	ax(2) = subplot(2,3,2);
	plot(m.data(:,1), m.data(:,2))
	grid on;
	legend('Elbow', 'Shoulder')
	title('Angle')
	ylim([0 360])

	ax(3) = subplot(2,3,3);
	plot(m.data(:,1), m.data(:,3))
	grid on;
	legend('Elbow', 'Shoulder')
	title('Velocity')
	% ylim([-2000 2000])

	ax(4) = subplot(2,3,4);
	plot(m.data(:,1), m.data(:,4))
	grid on;
	legend('Elbow', 'Shoulder')
	title('Current')
	% ylim([0 10])

	ax(5) = subplot(2,3,5);
	plot(m.data(:,1), in.data(1:length(m.data(:,1)),2))
	hold on;
	legend('Elbow', 'Shoulder')
	title('Direction')
	ylim([0 2])

	ax(6) = subplot(2,3,6);
	plot(m.data(:,1), in.data(1:length(m.data(:,1)),1))
	grid on;
	legend('Elbow', 'Shoulder')
	title('ON')
	ylim([0 2])

	linkaxes(ax,'x')