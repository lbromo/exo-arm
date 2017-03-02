% ----------------------------------------------
%  FORWARD EULER METHOD (Discrete model) 
%  test of method
% -----------------------------------------------
%Ts = 0.01;
%Tend = 20 / Ts;
xd = [0;0;0;0];

Ts = zeros(1, length(time(1:end-10)));
for a = 1:length(time(1:end-10))
    Ts(a)=time(a+1)-time(a);
end
u= zeros(2,length(time(1:end-10)))
%u = zeros(2, Tend);

u(1, 200:400) = 0.1;
u(2, 1:end) = 0;

%xd(:, 1) = [1; 1; 0; 0]

%params.vm = [0.5, 0.55]

%for k = 1:Tend
for k = 1:length(time(1:end-10))
  %if(mod(k,10) == 0)
  %  params.arm.plot(xd(1:2,k)', 'fps', 1/(Ts*10))
  %end

  %if (k > 1/Ts)
  %  u = [0; 0];
  %end
  xd(:,k+1) = xd(:,k) + Ts(k)*f(xd(:,k), u(:,k), params);
end

%time=[0:Ts:20];
subplot(2,1,1)
plot(time(1:end-10),xd(1,1:end-1),'g')
hold on
plot(time(1:end-10),xd(2,1:end-1),'r')
subplot(2,1,2)
plot(time(1:end-10),u(1,:))