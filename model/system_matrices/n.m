function [n] = n(x,params, viewflag)

  	V=v_matrix(x(1:2),x(3:4), params.l2, params.m2, params.a1, params.a2);
  	G=g_matrix(x(1:2), params.g, params.l1, params.l2, params.m1, params.m2, params.a1 ,params.a2);
  	F=f_matrix(x(3:4), params.vm, params.cm, params.N, params.sigmoidpar);

  	n = G + V + F;

  	if exist('viewflag') && viewflag == 1
  		disp('V:')
  		disp(V)
  		disp('G:')
  		disp(G)
  		disp('F:')
  		disp(F)
  	end

end