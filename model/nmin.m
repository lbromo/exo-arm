% numerical min fct.
function [minimum I] = nmin(x)
	[m I] = min(abs(x));

	minimum = x(I);

end