function [xd] = parest_forward(c_est, u)
%UNTITLED2 Summary of this function goes here
%   Detailed explanation goes here
global Ts params x0;
tmp_pars = params;
tmp_pars.cm = c_est(1:2);
 tmp_pars.vm=c_est(3:4);
tmp_pars.sigmoidpar=c_est(5:6);
 tmp_pars.hast=c_est(7:8);
xd(:,1)=x0;
for k = 1:length(Ts)
%    disp(size(f(xd(:,k), u(:,k), tmp_pars, 0)))
  xd(:,k+1) = xd(:,k) + Ts(k)*f(xd(:,k), u(:,k), tmp_pars);
 % acc(:,k+1)=(xd(3:4,k+1) - xd(3:4,k))/Ts(k);
end
xd=xd(3:4,:);
end

