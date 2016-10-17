ParametersScript

torque = [0.0004; 0]

theta = [0;0]
thetadot = [0;0]
thetadotdot = [0;0]

for i = 1:10
thetadotdot(:,end+1) = exo_dynamic_model(theta(:,end), thetadot(:,end),torque, params);
thetadot(:,end+1) = trapz(thetadotdot(:,end)');
theta(:,end+1) = trapz(thetadot(:,end)');
end