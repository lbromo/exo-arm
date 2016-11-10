%% Create model

addpath('../')

ParametersScript

m = idnlgrey('gb_sim', [4 2 4], [0.1 0.5], [0;0;0;0], 0.01)


%% Create data
Ts = 0.01;
Tend = 10;
x = [0;0;0;0];
u = [1; 0.5];

t = [0:Ts:Tend];
u = [square(t); square(t)];
for k = 1:Tend/Ts
  x(:,k+1) = x(:,k) + Ts*f(x(:,k), u(:,k), params);
end

data = iddata(x', u', Ts);

%% Estimate
opt = nlgreyestOptions;
opt.Display = 'off';
opt.SearchMethod = 'gn';
opt.SearchOption.MaxIter = 10000;
opt.GradientOptions.GradientType = 'Refined';

%m.Parameters(1).Fixed = true
%m.Parameters(2).Fixed = true

tmp  = nlgreyest(data, m, opt)
compare(data,tmp)

%gb_x = [0;0;0;0];
%for k = 1:Tend/Ts
%  gb_x(:,k+1) = gb_x(:,k) + gb_sim(0, gb_x(:,k), u(:,k)', 0.01, 0.05);
%end
