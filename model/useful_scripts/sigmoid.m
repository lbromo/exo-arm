% function val = sigmoid(arg, par)
function val = sigmoid(arg, par)

val = 2./(1+exp(-par * arg))-1;

end