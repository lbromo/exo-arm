close all; clear all;

delete(instrfindall);
s = serialInit('/dev/ttyS01');
fopen(s);
pause(2);

params = ParametersScript();

T_end = 1; % [s]
S = T_end/params.Ts; % Samples total

ref = [0 0 0 0]';

x = []; % States: [theta_s; theta_e; thetadot_s; thetadot_e]
u = [];

% p = 40;
% pd = 5;
% kp = [p 0  pd 0;...
% 	  0  p 0 pd];
k = 1;

while true
	tic
	fwrite(s, '&');

	data = fgets(s);
	data = str2num(data) 
	if isempty(data)
		disp('No data :(')
		break;
	end

	x(:,k) = [data(1) data(2) data(3) data(4)]' * 0.01;

	cpars.ref = ref;

	u(:,k) = c_feedback_lin(x(:,k),params,cpars);

	% e = ref-x(:,k);

	% n(x(:,k),params,1);
	
	% disp('B')
	% disp(B(x(:,k),params))

	% u(:,k) = B(x(:,k),params) * (kp * e) + n(x(:,k),params);

	% % u(:,k)  = (kp * e) + n(x(:,k),params);

	% disp('Ke')
	% disp(kp*e)

	u(:,k) = u(:,k)./([params.kt1 params.kt2]'*params.N);

	instr = sprintf('I%d,%d,E', round(u(1,k)*100), round(u(2,k)*100));
	fwrite(s,instr);
	disp(u(:,k))
	k = k+1;

	if k == 300
		ref = [pi/2 pi*1/2 0 0]'
	end
	if k == 600
		ref = [pi/2 0 0 0]'
	end
	if k == 900
		ref = [pi/2 pi/2 0 0 ]'
	end

	toc

end

fclose(s);
