%% Exo Dynamic Model Script

clear all; clc; close all;

% disp('Run "roblocks" to open RVC Simulink Library')
% warning('off','all') % Suppress annoying character encoding warning when opening the model
%     open('CrustCrawlerDynamicModel.slx')
% warning('on','all')
% addpath(genpath(cd));

%% Constants
g   = 9.81;     % [m/s^2] Gravitational acceleration
Ts	= 0.004;	% [s] Sampling period

%% Constants - Link 1:
d1  = 0;        % [m] Distance from {0} to {1} along z0
a1  = 0.25;        % [m] Distance from {0} to {1} along x0
alpha1 = 0;  % [rad] Rotation of z1 compared to z0
l1  = 3.5e-2;   % [m] Distance from {1} to CoM of link 1
m1  = 0.241;	% [kg] Mass of link 1

%% Constants - Link 2:
d2  = 0;        % [m] Distance from {1} to {2} along z1
a2  = 0.25;    % [m] Distance from {1} to {2} along x1
alpha2 = 0;     % [rad] Rotation of z2 compared to z1
l2  = 0.151;   % [m] Distance from {2} to CoM of link 2
m2  = 0.231;	% [kg] Mass of link 2


%% Inertias
[I1, I2] = InertiaCalculations([a1 a2],[m1 m2]);
Izz1=I1(3,3);Izz2=I2(3,3);


%% Frictions 
cm=[0.1427 0.3032]; 
vm= [0.07933 0.3446]; 

% %% Save all variables for use in other scripts
% save('ModelParams',...
% 		'm1','m2',...
% 		'a1','a2',...
% 		'l1','l2',...
% 		'I1','I2',...
% 		'g'...
% 		);

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
L(1) = Link('d', d1,	'a', a1,   'alpha', alpha1);
L(2) = Link('d', d2,	'a', a2,   'alpha', alpha2);


plotopt = { 'floorlevel',-0.1, ...
            'jvec',...
            'noshadow'};

arm = SerialLink(L, 'name', 'Exoskeleton','plotopt',plotopt);
save('SerialLinkCC','arm');
