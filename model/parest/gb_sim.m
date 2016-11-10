function [dx y] = gb_sim(t, x, u, p1, p2, varargin)
global params

params.cm(1) = p1;
params.cm(2) = p2;

dx = x + 0.01*f(x, u', params);
y = dx;

end
