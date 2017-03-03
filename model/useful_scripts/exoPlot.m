function exoPlot(exo,fid)

	if ~exist('fid')
		fid =1;
	end

	t = exo.t;
	x = exo.x;
	u = exo.u;

	figure(fid);
	ax(1) = subplot(311); 
	plot(t,x(1,:),t,x(2,:)); grid on;
	title('Joint Angles')
	legend('Shoulder','Elbow','Location','bestoutside');

	ax(2) = subplot(312); 
	plot(t,x(3,:),t,x(4,:)); grid on;
	title('Joint Velocities')
	legend('Shoulder','Elbow','Location','bestoutside');

	ax(3) = subplot(313); 
	plot(t,u(1,:),t,u(2,:)); grid on
	title('Input Torque')
	legend('Shoulder','Elbow','Location','bestoutside');

	linkaxes(ax, 'x');

end