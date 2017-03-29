clear all;

x = linspace(0,pi,100);
dx = linspace(-6,6,100);

params = ParametersScript()

for m = 1:100
for o = 1:100
	junk = n([x(m) 0 dx(o) 0]', params);
	z(m,o) = junk(1); 
end
end

surf(x,dx,z');

xlabel('x')
ylabel('dx')