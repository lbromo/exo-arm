m2 = importdata('both/motor1_both_sine.log'); %time,angle,velocity,current
m1 = importdata('both/motor2_both_sine.log'); %time,angle,velocity,current
in = importdata('both/input_both_sine.log'); %on1,dir1,pwm1,on2,dir2,pwm2

Ts = 0.01;

p1 = getSignal(m1, 'angle');
p2 = getSignal(m2, 'angle');
t1 = Ts:Ts:length(p1)*Ts;
t2 = Ts:Ts:length(p2)*Ts;

bits = @(ang) (ang-204)/-0.296;

p1_b10 = bits(p1);
p2_b10 = bits(p2);

p1_5v = p1_b10 * (5/2^10);
p2_5v = p2_b10 * (5/2^10);

p1_muh = p1_5v * 0.5 * 2^12/3.3;
p2_muh = p2_5v * 0.5 * 2^12/3.3;

a1_muh = (1495 - p1_muh) * 2 * pi / 2500;
a2_muh = (1308 - p2_muh) * 2 * pi / 2472;

% a1_us = p1 * 2*pi/360;
% a2_us = p2 * 2*pi/360;

off1 = a1_us(1) - a1_muh(1);
off2 = a2_us(1) - a2_muh(1);

a1_us = (1.2 *2^10/3.3 - p1_b10) * 2* pi / (2^10 * 2/3.3);
a2_us = (1.05*2^10/3.3 - p2_b10) * 2* pi / (2^10 * 2.24/3.3);

subplot(211);
plot(t1,a1_muh,t1,a1_us);
grid on;
subplot(212);
plot(t2,a2_muh,t2,a2_us);
grid on;