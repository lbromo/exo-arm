function u = c_admittance(x,params,cpars)

persistent thref;

if isempty(thref)
	disp('First Run!');
	thref = 0;
end

if isfield(cpars,'cl')
	clear thref;
	disp('thref cleared');
	u = 0;
	return;
end

b = 0.3;
ref = cpars.ref;

ref(4) = cpars.tau(cpars.k) * b + ref(4);

thref = thref + ref(4) * params.Ts;

ref(2) = thref + cpars.ref(2);


p = 50;
d = 10;
kp = [p 0  d 0;...
	  0  p 0 d];


% x = x + 0.1 * rand(4,1);

e = ref-x;

u = (B(x,params) * (kp * e) + n(x,params));
u = u./([params.kt1 params.kt2]'*params.N);

end