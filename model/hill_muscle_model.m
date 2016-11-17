function [xdot] = hill_muscle_model(x, a, params)
  length = x(1);
  velocity = x(2);

  %% CE elements
  DLce = length;% - params.Lce0;

  Vcemax = 2*params.Lce0 + 8*params.Lce0 * params.alpha;
  Vce0 = 1/2*(a + 1) * Vcemax;

  fl=exp(-0.5 * (((DLce/params.Lce0) - params.phim) / (params.phiv))^2)
  fv=0.1433/(0.1074+exp(-1.3*sinh(2.8*(velocity/Vce0)+1.64)))

  Fce=a*fl*fv*params.Fcemax;

  % SE elements
  Fsemax = 1.3 * params.Fcemax;
  DLsemax = 0.03 * params.Lts;
  DLse = DLce;

  Fpe=(Fsemax/(exp(params.Sse)-1))*(exp((params.Sse/DLsemax)*DLse)-1);


  acceleration = (1/params.M)*(Fce+Fpe);

  xdot = [velocity; acceleration];
end
