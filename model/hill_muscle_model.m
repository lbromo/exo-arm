function [xdot] = hill_muscle_model(t, x, a, params)
  %% Fra lækkerlækkerhill:
  % x = [Lm; Vm]
  % xdot(1) = x(2);
  % xdot(2) = 1/M * Ftot
  % Ftot = Fse - (Fce + Fpe)

  Lm = x(1);
  Vm = x(2);

  % Fce = Fmax * a * f(Lm) * g(Vm):
  % g(Vm):
  g = (1 - Vm / params.Vmax) / (1 + 4*Vm / params.Vmax);
  % f(Lm):
  f = ((Lm/params.Lmopt - 1) / params.w)^2;

  Fce = a*g*f*params.Fmax;

  % Fpe = Fp(Lm) + Fd(Vm):
  % Fp(Lm):
  if(Lm < params.Lms)
    Fp = 0;
  elseif(params.Lms <= Lm && Lm <= params.Lmc)
    Fp = params.Kml/params.Kme * (exp(params.Kme*(Lm - params.Lms))-1);
  else
    Fp = params.Fmc + params.Km*(Lm - params.Lmc);
  end
  % Fd(Vm):
  Fd = params.Bm * Vm;

  Fpe = Fp + Fd;

  % Fse(Lt):
  % Lt = const - Lm
  Lt = params.Ltot - Lm;

  if(Lt < params.Lts)
    Fse = 0;
  elseif(params.Lts <= Lt && Lt <= params.Ltc)
    Fse = params.Ktl / params.Kte * (exp(params.Kte*(Lt - params.Lts))-1);
  else
    Fse = params.Ftc + params.Kt * (Lt - params.Lts);
  end

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

  %% SE elements
  %
  Fsemax = 1.3 * params.Fcemax;
  DLsemax = 0.03 * params.Lts;
  DLse = params.Lmax + Lm;
  Fse = (Fsemax/(exp(params.Sse)-1)) * (exp((params.Sse./DLsemax).*DLse)-1)

  Fse = 0;
  acc = Fse - (Fce+Fpe) / params.M;

  xdot = [Vm; acc];

end
