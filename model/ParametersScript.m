%% Exo Dynamic Model Script

%clear all; clc; close all;

% disp('Run "roblocks" to open RVC Simulink Library')
% warning('off','all') % Suppress annoying character encoding warning when opening the model
%     open('CrustCrawlerDynamicModel.slx')
% warning('on','all')
% addpath(genpath(cd));

disp('Parametersscript')

%% Constants
g   = 9.81;     % [m/s^2] Gravitational acceleration
Ts	= 0.004;	% [s] Sampling period

%% Constants - Link 1:
d1  = 0;        % [m] Distance from {0} to {1} along z0
a1  = 330e-3;        % [m] Distance from {0} to {1} along x0
alpha1 = 0;  % [rad] Rotation of z1 compared to z0
l1  = 224e-3;   % [m] Distance from {1} to CoM of link 1
m1  = 1491.070e-3;	% [kg] Mass of link 1

%% Constants - Link 2:
d2  = 0;        % [m] Distance from {1} to {2} along z1
a2  = 227e-3;    % [m] Distance from {1} to {2} along x1
alpha2 = 0;     % [rad] Rotation of z2 compared to z1
l2  = 89e-3;   % [m] Distance from {2} to CoM of link 2
m2  = 547.77e-3;	% [kg] Mass of link 2


%% Inertias
%[I1, I2] = InertiaCalculations([a1 a2],[m1 m2]);

I1_xx = 17401661.51e-9
I1_yy = 49708861.39e-9
I1_zz = 33589941.15e-9
I1_xy = -9363.03e-9
I1_yz = -40923.12e-9
I1_xz = -10657124.30e-9

I2_xx = 658642.154e-9
I2_yy = 3806398.210e-9
I2_zz = 3444384.466e-9
I2_xy = 3462.100e-9
I2_yz = -4984.582e-9
I2_xz = -443444.240e-9

I1 = [I1_xx, I1_xy, I1_yz
      I1_xy, I1_yy, I1_yz
      I1_xz, I1_xy, I1_zz]

I2 = [I2_xx, I2_xy, I2_yz
      I2_xy, I2_yy, I2_yz
      I2_xz, I2_xy, I2_zz]

Izz1=I1(3,3);Izz2=I2(3,3);


%% Frictions 
cm=[0.01 0.05]; 
vm= [0.00005 0.00055]; 

% %% Save all variables for use in other scripts
% save('ModelParams',...
% 		'm1','m2',...
% 		'a1','a2',...
% 		'l1','l2',...
% 		'I1','I2',...
% 		'g'...
% 		);
global params
params.m1 = m1;
params.m2 = m2;
params.a1 = a1;
params.a2 = a2;
params.l1 = l1;
params.l2 = l2;
params.I1 = I1;
params.I2 = I2;
params.g = g;
params.cm = cm;
params.vm = vm;

%% Robotics Toolbox Implementation
%L(1) = Link('d', d1,	'a', a1,   'alpha', alpha1);
%L(2) = Link('d', d2,	'a', a2,   'alpha', alpha2);
%
%
%plotopt = { 'floorlevel',-0.1, ...
%            'jvec',...
%            'noshadow'};
%
%params.arm = SerialLink(L, 'name', 'Exoskeleton','plotopt',plotopt);
%save('SerialLinkCC','arm');
