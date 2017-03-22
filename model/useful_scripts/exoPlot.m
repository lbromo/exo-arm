function exoPlot(exo,fid)

	if ~exist('fid')
		fid =1;
	end

	t = exo.t;
	x = exo.x;
	u = exo.u;
	% x_m = exo.x_m;
	% u_m = exo.u_m;

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

	% figure(fid+1);
	% ax(1) = subplot(311); 
	% plot(t,x_m(1,:),t,x_m(2,:)); grid on;
	% title('Joint Angles - Mex Feedback Lin')
	% legend('Shoulder','Elbow','Location','bestoutside');

	% ax(2) = subplot(312); 
	% plot(t,x_m(3,:),t,x_m(4,:)); grid on;
	% title('Joint Velocities')
	% legend('Shoulder','Elbow','Location','bestoutside');

	% ax(3) = subplot(313); 
	% plot(t,u_m(1,:),t,u_m(2,:)); grid on
	% title('Input Torque')
	% legend('Shoulder','Elbow','Location','bestoutside');

	% linkaxes(ax, 'x');

end