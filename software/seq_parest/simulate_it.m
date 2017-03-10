% 8=====================================D
% SIMULATE
% 8=====================================D
N = length(cur);

x0 = [0 vel(1)];
x = zeros(2,N);
tau_f = zeros(1,N);
x(:,1) = x0;

for t = 2:N
    dx1 = x(2,t);
    tau_m = kt * cur(t);
    fv = b * dx1;
    % if dx1 == 0
    %     fc = min([tau_m tau_c*(-sign(tau_m))]);
    % else
    %     fc = tau_c * sign(dx1);
    % end
    fc = tau_c * sigmoid(dx1, sigmoidpar);
    tau_f(t) = fv+fc;
    
    dx2 = 1/Jm * (tau_m - tau_f(t));
    x(:,t+1) = x(:,t) + Ts * [dx1;dx2];
end

