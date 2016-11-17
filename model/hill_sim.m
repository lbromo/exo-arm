
%% From Real-Time Myoprocessors for a Neural Controlled Powered Exoskeleton Arm page 6
params.Lmax = 0.4046;
params.Lce0 = 0.1307;
params.Lts = 0.2298;
params.Fcemax = 461.76;
params.Sse = 2.8;
params.DLmax = 0.10;
params.alpha = 0.56;

%%
params.phim = 0.1;
params.phiv = 0.8;
params.M = 1;



ts = 0.01;
T = 1:ts:2;

x = [0.001;0];
a = zeros(1,length(T));
%a(1:100) = 0.5;

for k = 1:(T(end) - 1) * 1/ts
  x(:,k+1) = x(:,k) + ts*hill_muscle_model(x(:,k), a(k), params);
end
