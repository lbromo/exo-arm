%pid
damping =1
wn=5;
n=1;
ki=n*wn^(3)
kp=(1+2*n)*(ki/n)^(2/3)
kv=(n+2)*(ki/n)^(1/3)


sys= tf([1 0],[1 kv kp ki]);
% a = [0,1,0;0,0,1;-ki,-kp,-kv];
% b = [0;0;1];
% c = [1,0,0];
%sys = ss(a,b,c,0);
% [x,t] = step(sys);

s = tf('s');
sys = 1/s^2;

c = ki/s + kp + kv*s;

cl = feedback(sys*c,1)
[x_e, t_e] = step(cl,4);

%bode(sys)
%rlocus(sys)

%pd
% kp=100;
% kv=20;
% sys= tf([1],[1 kv kp])
% step(sys)
% stepinfo(sys)

%pid
damping =1
wn=3;
n=1;
ki=n*wn^(3)
kp=(1+2*n)*(ki/n)^(2/3)
kv=(n+2)*(ki/n)^(1/3)


sys= tf([1 0],[1 kv kp ki]);
% a = [0,1,0;0,0,1;-ki,-kp,-kv];
% b = [0;0;1];
% c = [1,0,0];
%sys = ss(a,b,c,0);
% [x,t] = step(sys);

s = tf('s');
sys = 1/s^2;

c = ki/s + kp + kv*s;

cl = feedback(sys*c,1)
[x_s, t_s] = step(cl,4);

%bode(sys)
%rlocus(sys)

%pd
% kp=100;
% kv=20;
% sys= tf([1],[1 kv kp])
% step(sys)
% stepinfo(sys)