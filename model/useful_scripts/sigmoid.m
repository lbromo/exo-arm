% function val = sigmoid(arg, par)
function val = sigmoid(x, par)

val = 2./(1+exp(-par * x))-1;

end