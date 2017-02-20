% 8=====================================D
% PARAMETERS
% 8=====================================D

if joint == 2
    N = 50;
    JG2 = 0.282e-4;      % [kg*m2] Gear inertia
    JM2 = 1210e-7;       % [kg*m2] Motor inertia (shoulder flex/ext)
    JA2 = 539919.92e-9; %4722727.19e-9; % [kg*m2]
    Jm  = (JG2+JM2)*N^2 + JA2;%181e-3; 
elseif joint == 1
    N = 50;
    JG3 = 0.282e-4;      % [kg*m2] Gear inertia
    JM3 = 181e-7;        % [kg*m2] Motor inertia (elbow flex/ext)
    JA3 = 1562955.32e-9; % [kg*m2]
    Jm = (JG3+JM3)*N^2+JA3;
end

vs = 1;
vs2 = 18;
sigmoidpar = 5;
