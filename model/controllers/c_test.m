function [u] = c_test(x, params, cpars)

	if cpars.k < cpars.t_end;
		u = [0 1];
	else 
		u = [0 0];
	end
end