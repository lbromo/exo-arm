function mse = exo_mse(x, y)

if length(x) ~= length(y)
	disp('Vectors need to be the same length!')
	mse = NaN;
	return;
end


mse = sum((x(:)-y(:)).^2)/length(x);

end