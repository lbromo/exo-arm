%% 
% ----------------------------------------------
%  ODE SOLVER
% -----------------------------------------------
x0 = [
      1
      1;
      0;
      0;
];

u = [
       0;
       0
];

t_span = [0 5];

 [t,x] = ode113(@exo_dynamic_model, t_span, x0, [], u, params);


%So we have way to many samples, and no "specific" sampling time..
%We "create" one by taking unique time samples with a 0.01 spacing
[C,ia,ic] = uniquetol(t, 0.001);

theta1 = x(ia,1);
theta2 = x(ia,2);

theta = [theta1 theta2];

params.arm.plot(theta, 'fps', length(theta)/t_span(end), 'loop');
