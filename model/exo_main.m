ParametersScript

x0 = [
      0;
      0;
      0;
      0;
];

u = [
       0;
       4
];

t_span = [
          1;
          3
];
tic
[t,x] = ode113(@exo_dynamic_model, t_span, x0, [], u, params);
