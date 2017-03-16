function u = c_admittance(x,params,upre, xpre,uref,s,cl)

persistent thref;

if isempty(thref)
	disp('First Run!');
	thref = 0;
end

if exist('cl')
	clear thref;
	disp('thref cleared');
	u = 0;
	return;
end

tau = upre;

b = 0.3;
ref = zeros(4,1);

ref(4) = tau * b;

thref = thref+ ref(4) * params.Ts;

ref(2) = thref;


p = 50;
pd = 10;
kp = [p 0  pd 0;...
	  0  p 0 pd];


% x = x + 0.1 * rand(4,1);

e = ref-x;

u = (B(x,params) * (kp * e) + n(x,params));
u = u./([params.kt1 params.kt2]'*params.N);



end