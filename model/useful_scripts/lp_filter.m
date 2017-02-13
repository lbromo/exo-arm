function out = lp_filter(in, par) 

	in = abs(in);
	out = zeros(length(in),1);

	for i = length(par):length(in)
		out(i) = par(1) * in(i) - par(2) * out(i-1) - par(3) * out(i-2);
	end


end