function F = hill_muscle_model(Lm, Vm, a, params)
  %% CE elements - looks fair
  % Real-Time Myoprocessors for a Neural Controlled Powered Exoskeleton Arm
  DLce = Lm;% - params.Lms;% WRONG
  %
  Vcemax = 2*params.Lce0 + 8*params.Lce0 * params.alpha;
  Vce0 = 1/2*(a + 1) * Vcemax;
  %
  fl=exp(-0.5 * (((DLce./params.Lce0) - params.phim) / (params.phiv)).^2);
  fv=0.1433./(0.1074+exp(-1.3*sinh(2.8*(Vm./Vce0)+1.64)));
  %
  Fce=a*fl.*fv*params.Fcemax;

  %% PE elements
  % Real-Time Myoprocessors for a Neural Controlled Powered Exoskeleton Arm
  Fpemax = 0.05 * params.Fcemax;
  DLpemax = params.Lmax - (params.Lce0 + params.Lts);
  DLpe = DLce;

  Fpe=(Fpemax/(exp(params.Spe)-1)) * (exp((params.Spe./DLpemax).*DLpe)-1);

  F = Fce + Fpe;
end
