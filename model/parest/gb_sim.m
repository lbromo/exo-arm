function [xd y] = gb_sim(t, x, u, p1, p2, tmp)
global params

params.cm(1) = p1;
params.cm(2) = p2;

xd = 0.01*f(x, u', params);
y = xd;

end
