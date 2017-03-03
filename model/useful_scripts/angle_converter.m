close all; clear all;

m2 = importdata('both/motor1_both_sine.log'); %time,angle,velocity,current
m1 = importdata('both/motor2_both_sine.log'); %time,angle,velocity,current
in = importdata('both/input_both_sine.log'); %on1,dir1,pwm1,on2,dir2,pwm2

Ts = 0.01;

p1 = getSignal(m1, 'angle');
p2 = getSignal(m2, 'angle');
t = Ts:Ts:length(p1)*Ts;

bits = @(ang) (ang-204)./-0.296;

Vto10bit = @(num) num*2^10/3.3;

p_b10 = bits([p1 p2(1:length(p1))]);

p_5v = p_b10 * (5/2^10);

p_muh = p_5v * 2.6/5 * 2^12/3.3;

a1_muh = (1308 - p_muh(:,1)) * 2 * pi ./ 2472;
a2_muh = (1495 - p_muh(:,2)) * 2 * pi ./ 2500;

p_off_1 = 1308 * 3.3/2.6 / 2^2;
p_a1 	= 2472 * 3.3/2.6 / 2^2;

p_off_2 = 1495 * 3.3/2.6 / 2^2;
p_a2	= 2500 * 3.3/2.6 / 2^2;

a_us1 = (p_off_1 - p_b10(:,1)) * 2 * pi ./ p_a1;
a_us2 = (p_off_2 - p_b10(:,2)) * 2 * pi ./ p_a2;

subplot(211);
plot(t,a1_muh,t,a_us1,'-.');
grid on;
subplot(212);
plot(t,a2_muh,t,a_us2,'-.');
grid on;