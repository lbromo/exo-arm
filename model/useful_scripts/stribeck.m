function y = stribeck(x,vs,sigpar)

	y = sigmoid(x,sigpar) .* exp(-abs(x./vs));

end