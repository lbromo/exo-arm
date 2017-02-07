ParametersScript

x0 = [
      0
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

Ts = 0.0001;
Tend = 60 / Ts;
xd = [0;1;0;0];
u = zeros(2, Tend);

u(1, 1:100) = 0;
u(2, 1:end) = 0;

%xd(:, 1) = [1; 1; 0; 0]

%params.vm = [0.5, 0.55]

for k = 1:Tend
  %if(mod(k,10) == 0)
  %  params.arm.plot(xd(1:2,k)', 'fps', 1/(Ts*10))
  %end

  %if (k > 1/Ts)
  %  u = [0; 0];
  %end
  xd(:,k+1) = xd(:,k) + Ts*f(xd(:,k), u(:,k), params);
end

subplot(3,1,1)
plot(xd(1,:))
subplot(3,1,2)
plot(xd(2,:))
