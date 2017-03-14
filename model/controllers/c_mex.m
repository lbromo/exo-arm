% Simulation using mex file;
function u = c_controller_mex(x,params,upre, xpre,ref,s)

	u = controller_mex(x, ref);

end