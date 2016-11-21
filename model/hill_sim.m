
%% From Real-Time Myoprocessors for a Neural Controlled Powered Exoskeleton Arm page 6
params.Lmax = 404.6;
params.Lce0 = 130.7;
params.Lts = 229.8;
params.Fcemax = 461.76;
params.alpha = 0.56;
params.Spe = 9;
params.Sse = 2.8;

%%
params.phim = 0.1;
params.phiv = 0.5;
params.M = 1000;

%%
% Fra lækkerlækkerhill
%params.Fmax = 3913;
%params.Lmopt = 0.0959;
%params.Vmax = 0.5179;
%params.w = 0.643;
%params.Kte = 3022;
%params.Ktl = 31140;
%params.Kt = 635540;
%params.Lts = 0.3185;
%params.Ltc = 0.3185;
%params.Ftc = 200;
%params.Kme = 90.4;
%params.Kml = 487.5;
%params.Km = 6770;
%params.Lms = 0.0959;
%params.Lmc = 0.125;
%params.Fmc = 69.4723;
%params.Bm = 257.1;

% Own
%params.Ltot = 40.46;

ts = 0.1;
t = 1:ts:1000;

x = [0;0];
a = zeros(1,length(t));
a(1:10) = 0.5;

%for k = 1:(t(end) - 1) * 1/ts
%  x(:,k+1) = x(:,k) + ts*hill_muscle_model(0, x(:,k), a(k), params);
%end

Fpemax = 0.05 * params.Fcemax;
DLpemax = params.Lmax - (params.Lce0 + params.Lts)

[Lm Vm] = meshgrid([-250:1:55], [-600:5:200]);

Vcemax = 2*params.Lce0 + 8*params.Lce0 * params.alpha;
Vce0 = 1/2*(1 + 1) * Vcemax;

Fsemax = 1.3 * params.Fcemax;
DLsemax = 0.03 * params.Lts;

fl=exp(-0.5 * (((Lm./params.Lce0) - params.phim) / (params.phiv)).^2);
fv=0.1433 ./ (0.1074+exp(-1.3*sinh(2.8*(Vm./Vce0)+1.64)));

Fce2 =1*fl.*fv*params.Fcemax;

Fpe2 = (Fpemax/(exp(params.Spe)-1)) * (exp((params.Spe./DLpemax).*Lm)-1);

%DLse = Lm;
%
%Fse = (Fsemax/(exp(params.Sse)-1)) * (exp((params.Sse./DLsemax).*DLse)-1);

F = Fce2 + Fpe2;
