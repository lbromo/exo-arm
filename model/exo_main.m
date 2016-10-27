ParametersScript

x0 = [
      2
      0;
      0;
      0;
];

u = [
       0;
       0
];

t_span = [0 10];

% [t,x] = ode113(@exo_dynamic_model, t_span, x0, [], u, params);


%% So we have way to many samples, and no "specific" sampling time..
%% We "create" one by taking unique time samples with a 0.01 spacing
% [C,ia,ic] = uniquetol(t, 0.001);

%theta1 = x(ia,1);
%theta2 = x(ia,2);

%theta = [theta1 theta2];

%params.arm.plot(theta, 'fps', length(theta)/t_span(end), 'loop');

%% Discrete model

Ts = 0.01;
Tend = 10;
xd = [0;0;0;0];
u = [1; 0.5];

for k = 1:Tend/Ts
  if(mod(k,10) == 0)
    params.arm.plot(xd(1:2,k)', 'fps', 1/(Ts*10))
  end

  if (k > 1/Ts)
    u = [0; 0];
  end

  xd(:,k+1) = xd(:,k) + Ts*f(xd(:,k), u, params);
end
