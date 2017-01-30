close all; 
clear all;

format long

sq_name = 'SHOULDER_100_STEP_T2_';
sin_name = 'SHOULDER_260_SINE_T2_';
sq_amps = linspace(20,80,7);
sin_amps = linspace(10,100,10);
[par MSE sq sin] = parest_both(sq_name, sq_amps, sin_name, sin_amps, 2, 0, 0);

disp('Shoulder Pars')
par_s = par
MSE

Tsq = table(sq{1}', sq{2}', sq{3}', 'VariableNames', {'time'; 'meas'; 'sim'});
fnsq = 'shoulder_dir_tuned_sq.csv';
%writetable(Tsq, fnsq);

Tsin = table(sin{1}', sin{2}', sin{3}', 'VariableNames', {'time'; 'meas'; 'sim'});
fnsin = 'shoulder_dir_tuned_sin.csv';
%writetable(Tsin, fnsin);

figure;

sq_name = 'ELBOW_1260_STEP_T2_';
sin_name = 'ELBOW_260_SINE_T2_';
sq_amps = linspace(10,40,4);
sin_amps = linspace(10,50,5);
[par MSE sq sin] = parest_both(sq_name, sq_amps, sin_name, sin_amps, 2, 0, 1);

disp('Elbow Pars')
par_e = par
MSE


sin{1} = sin{1}(3:end);
sin{2} = sin{2}(3:end);
sin{3} = sin{3}(3:end);

Tsq = table(sq{1}', sq{2}', sq{3}', 'VariableNames', {'time'; 'meas'; 'sim'});
fnsq = 'elbow_dir_tuned_sq.csv';
%writetable(Tsq, fnsq);

Tsin = table(sin{1}', sin{2}', sin{3}', 'VariableNames', {'time'; 'meas'; 'sim'});
fnsin = 'elbow_dir_tuned_sin.csv';
%writetable(Tsin, fnsin);

%close all
