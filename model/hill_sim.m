
%% From Real-Time Myoprocessors for a Neural Controlled Powered Exoskeleton Arm page 6
params.Lmax = 40.46;
params.Lce0 = 13.07;
params.Lts = 22.98;
params.Fcemax = 461.76;
params.alpha = 0.56;
params.Spe = 9;
params.Sse = 28;

%%
params.phim = 0.1;
params.phiv = 0.8;
params.M = 1000;

%%
% Fra lækkerlækkerhill
params.Fmax = 3913;
params.Lmopt = 0.0959;
params.Vmax = 0.5179;
params.w = 0.643;
params.Kte = 3022;
params.Ktl = 31140;
params.Kt = 635540;
params.Lts = 0.3185;
params.Ltc = 0.3185;
params.Ftc = 200;
params.Kme = 90.4;
params.Kml = 487.5;
params.Km = 6770;
params.Lms = 0.0959;
params.Lmc = 0.125;
params.Fmc = 69.4723;
params.Bm = 257.1;

% Own
params.Ltot = 0.25;

ts = 0.01;
T = 1:ts:100;

x = [0.15;0];
a = zeros(1,length(T));

for k = 1:(T(end) - 1) * 1/ts
  x(:,k+1) = x(:,k) + ts*hill_muscle_model(0, x(:,k), a(k), params);
end
