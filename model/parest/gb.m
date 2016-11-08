%% Create model

addpath('../')

ParametersScript

opt = nlgreyestOptions('Display', 'on');
m = idnlgrey('gb_sim', [4 2 4], {0.01 0.05}, [0;0;0;0], 0.01)


%% Create data
Ts = 0.01;
Tend = 10;
xd = [0;0;0;0];
u = [1; 0.5];

t = [0:Ts:Tend];
u = [square(t); square(t)];
for k = 1:Tend/Ts
  xd(:,k+1) = xd(:,k) + Ts*f(xd(:,k), u(:,k), params);
end

data = iddata(xd', u', Ts);

%% Estimate
tmp  = nlgreyest(data, m, opt);
