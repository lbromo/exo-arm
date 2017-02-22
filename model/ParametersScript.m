%% Exo Dynamic Model Script

%clear all; clc; close all;

% disp('Run "roblocks" to open RVC Simulink Library')
% warning('off','all') % Suppress annoying character encoding warning when opening the model
%     open('CrustCrawlerDynamicModel.slx')
% warning('on','all')
% addpath(genpath(cd));

disp('Parametersscript')


%% Gear Ratio

N=50;
%% Constants
g   = 9.81;     % [m/s^2] Gravitational acceleration
Ts	= 0.004;	% [s] Sampling period
kt1  = 0.0708;%176.9956/N;%101.961/N;%247.4564/N; %300/N; %187.6525/N;     % motor constant shoulder/m1
kt2  = 0.0764; %190.8920/N;%135.4855/N;%242.2123/N;  %279.4054/N; %193.5055/N;     % motor constant elbow/m2
%% Constants - Link 1:
d1  = 0;        % [m] Distance from {0} to {1} along z0
a1  = 330e-3;        % [m] Distance from {0} to {1} along x0
alpha1 = 0;  % [rad] Rotation of z1 compared to z0
l1  = 244.9300e-3;   % [m] Distance from {1} to CoM of link 1
m1  = 1412.26e-3;	% [kg] Mass of link 1

%% Constants - Link 2:
d2  = 0;        % [m] Distance from {1} to {2} along z1
a2  = 227e-3;    % [m] Distance from {1} to {2} along x1
alpha2 = 0;     % [rad] Rotation of z2 compared to z1
l2  = 174.2420e-3;   % [m] Distance from {2} to CoM of link 2
m2  = 307.424e-3;	% [kg] Mass of link 2


%% Inertias
%[I1, I2] = InertiaCalculations([a1 a2],[m1 m2]);

I1_xx = 1237092.59e-9
I1_yy = 21058153.33e-9
I1_zz = 20909842.62e-9
I1_xy = -5512.53e-9
I1_yz =  584.44e-9
I1_xz = 2358470.81e-9

I2_xx = 81789.271e-9
I2_yy = 1069200.617e-9
I2_zz = 1118883.857e-9 
I2_xy = 0.001e-9
I2_yz = 0
I2_xz = -26501.404e-9

I1 = [I1_xx, I1_xy, I1_xz
      I1_xy, I1_yy, I1_yz
      I1_xz, I1_yz, I1_zz]

I2 = [I2_xx, I2_xy, I2_xz
      I2_xy, I2_yy, I2_yz
      I2_xz, I2_yz, I2_zz]

Izz1=I1(3,3);Izz2=I2(3,3);

%% Motor Inertia
In1 = 0.282e-4 + 1210e-7; % shoudler gear and motor inertia
In2 = 0.282e-4 + 181e-7;  % elbow gear and motor inertia

%% Frictions 
cm=[0.0660 0.0359];%[165.0942/(N^2) 89.7613/(N^2)];%[31.519/(N^2) 18.6925/(N^2)];%[224.8743/(N^2) 95.9248/(N^2)];%[283.27/(N^2) 110.16/(N^2)];%[119.9795/(N^2) 51.5666/(N^2)];
vm= [1.9469e-4 4.4047e-5]; %[0.4867/(N^2) 0.1101/(N^2)];% [2.0377/(N^2) 1.0787/(N^2)];%[0.7988/(N^2) 0.274/(N^2)];%[0.9872/(N^2) 0.4129/(N^2)]; [1.2548/(N^2) 0.5650/(N^2)];
sigmoidpar=[0.1383 0.0889];

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
params.In1 = In1;
params.In2 = In2;
params.N = N;
params.kt1 = kt1;
params.kt2 = kt2;
params.sigmoidpar=sigmoidpar;
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
