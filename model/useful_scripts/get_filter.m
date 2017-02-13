function [a b1 b2] = get_filter(c)


	b1 = c(1)+c(2);
	b2 = c(1)*c(2);
	a = 1-b1-b2;

end