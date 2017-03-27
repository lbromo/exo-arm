function u = c_arduino(x,params,cpars)

	s = cpars.s;
	ref = cpars.ref;

	refmsg = sprintf('R%3.3d,%3.3d,%3.3d,%3.3d,E', round(100*ref(1)),round(100*ref(2)),round(100*ref(3)),round(100*ref(4)));
	fwrite(s,refmsg);

	msg = sprintf('$%3.3d,%3.3d,%3.3d,%3.3d,E', round(100*x(1)),round(100*x(2)),round(100*x(3)),round(100*x(4)));
	fwrite(s,msg);

	inmsg =	fgets(s);
	if isempty(inmsg);
		inmsg = '0,0,0,0';
		disp('Shit..')
	end
	
	u = str2num(inmsg)';

	% u = out * 0.01;



	% u(1) = out(1) * 1/(params.kt1 * params.N);% 
	% u(2) = out(2) * 1/(params.kt2 * params.N);% 

	% u(1) = cur2torque(pwm2cur(out(1), out(3), 1),1,params); % Shoulder
	% u(2) = cur2torque(pwm2cur(out(2), out(4), 2),2,params); % Elbow

end