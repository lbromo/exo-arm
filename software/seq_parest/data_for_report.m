clear all; close all;

in_sq = importdata('logs/shoulder/input_rs_60_0.3.log');
m_sq = importdata('logs/shoulder/motor1_rs_60_0.3.log');
t = getSignal(m_sq,'time');
real_cur = getSignal(m_sq,'current');

 
pwm = getSignal(in_sq, 'pwm1');
dir = getSignal(in_sq, 'dir1');
dir = sign(dir-0.5);

pwm = pwm-25;

cur = pwm * 1.29/61 .* dir;

% plot(t,cur, t,real_cur);
% grid on;

T = table(t,cur, 'VariableNames', {'time','current'});
writetable(T,'parest_input_sq.csv');


in_sin = importdata('logs/shoulder/input_s_sin_no_1.3.log');
m_sin = importdata('logs/shoulder/motor1_s_sin_no_1.3.log');
t = getSignal(m_sin,'time');
real_cur = getSignal(m_sin,'current');

 
pwm = getSignal(in_sin, 'pwm1');
dir = getSignal(in_sin, 'dir1');
dir = sign(dir-0.5);

pwm = pwm-25;

cur = pwm * 3/205 .* dir;

% plot(t,cur, t,real_cur);
% grid on;

T = table(t,cur, 'VariableNames', {'time','current'});
writetable(T,'parest_input_sin.csv');