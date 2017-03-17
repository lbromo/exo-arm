% Simulation using mex file;
function u = c_mex(x,params,cpars)

	u = controller_mex(x, cpars.ref);

end