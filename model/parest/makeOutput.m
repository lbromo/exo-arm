close all; clear all

addpath('../');
ParametersScript

Ts = 0.01;
Tend = 10;
t = Ts:Ts:Tend;
xd = [1.67;0;0;0];
% u = 0.25 * square(t)+0.25;
u = zeros(2,length(t));
%u(1,1:100) = 1;
%u(1,500:600) = -1;
%u(2,1000:1100) = 1;
%u(2,1500:1600) = -1;


for k = 1:length(t)
%	u(1,k) = (1.67 - xd(1,k));
  xd(:,k+1) = xd(:,k) + Ts*f(xd(:,k), u(:,k), params);
end

y = xd(:,2:end);
%ynoise =  0.05 * randn(size(y));
%y = y+ynoise;
u = u';
y = y';
t = t'; 

save measexo t u y
%{
for i = 1:4 
  plot(y(:,i)) 
  hold on
end
%}