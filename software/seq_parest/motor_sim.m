function dx = motor_sim(t,x,ia,kt,f_c,f_v)

	Jm = 181e-3;

	acc = 1/Jm *(kt * ia - f_c * sign(x(2) - f_v * x(2)))

	dx = [x(2) acc];
end