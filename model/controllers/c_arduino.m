function u = c_arduino(x,params,cpars)

	s = cpars.s;
	ref = cpars.ref;

	refmsg = sprintf('R%3.3d,%3.3d,%3.3d,%3.3d,E', round(100*ref(1)),round(100*ref(2)),round(100*ref(3)),round(100*ref(4)));
	fwrite(s,refmsg);

	msg = sprintf('$%3.3d,%3.3d,%3.3d,%3.3d,E', round(100*x(1)),round(100*x(2)),round(100*x(3)),round(100*x(4)));
	fwrite(s,msg);

	inmsg =	fgets(s);
	if isempty(inmsg);
		inmsg = '0,0';
		disp('Shit..')
	end
	
	u = str2num(inmsg)'.*0.01;

end