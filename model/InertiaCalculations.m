function [I1, I2] = inertiaCalcs(a,mLink)
%% Beams:
wb = 25.4e-3; % [m], width of beams
tkb = 3e-3; % [m], thickness of beams

%% Masses of motors + beams = links:
mLink1 = mLink(1); % [kg]
mLink2 = mLink(2);

%% Masses of motors alone:
mMot1 = 0.140; % [kg]
mMot2 = 0.176; 
mTool = 0.238;

%% Masses of beams alone:
mBeam1 = mLink1-mMot2;
mBeam2 = mLink2-mTool;

%% Inertias, joint 1:
Ixx1 = mLink1*(4*wb*tkb - 2*tkb^2)/12; % Own axis
Iyy1 = a(1)^2*(mBeam1/3 + mMot2);
Izz1 = Iyy1;

%% Inertias, joint 2:
Ixx2 = mLink2*(4*wb*tkb - 2*tkb^2)/12; % Own axis
Iyy2 = a(2)^2*(mBeam2/3 + mTool);
Izz2 = Iyy2;

%% Combine numbers, output matrices:
I1 = diag([Ixx1, Iyy1, Izz1]);
I2 = diag([Ixx2, Iyy2, Izz2]);