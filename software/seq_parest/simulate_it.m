% 8=====================================D
% SIMULATE
% 8=====================================D
N = length(cur);

x0 = [0 vel(1)];
x = zeros(2,N);
tau_f = zeros(1,N);
x(:,1) = x0;


for t = 1:N
    dx1 = x(2,t);
    tau_m = kt * cur(t);
    fv = b * dx1;
    fc = tau_c * sigmoid(dx1,sigmoidpar);
    fs = tau_s * sigmoid(dx1,sigmoidpar)*exp(-abs(dx1/vs));

    tau_f(t) = fv + fc + fs;

    % if (abs(dx1) < 1) && (abs(tau_m) < (abs(fc)+abs(fs)))
    %     tau_f(t) = tau_m;
    % end

    dx2 = 1/Jm * (tau_m - tau_f(t));
    x(:,t+1) = x(:,t) + Ts * [dx1;dx2];
end