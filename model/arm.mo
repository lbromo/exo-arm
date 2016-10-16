model arm

extends Modelica.SIunits;

// Input torques
parameter Torque tau1(start=1);
parameter Torque tau2(start=1);

// Variables
Angle thetaShoulder(start=0);
Angle thetaElbow(start=0);
AngularVelocity w1_1[1,3](start=0);
AngularVelocity w2_2[1,3](start=0);
AngularVelocity w1_0[1,3](start=0);
AngularVelocity w2_0[1,3](start=0);
AngularAcceleration a1_0[1,3] (start=0);
AngularAcceleration a2_0[1,3] (start=0);

// Denavit-hartenberg parameters for rotation matrices
final parameter Length a1=0.25;
final parameter Length a2=0.25;

// Distances to CoM of links in local coordinates
final parameter Length l1=0.035;
final parameter Length l2=0.151;
// Position of CoM of links in local coordinates
final parameter Real C1_1[4,1] = [-l1; 0; 0; 1];
final parameter Real C2_2[4,1] = [-l2; 0; 0; 1];
// Position of CoM if links in global coordinates
Real C1_0[4,1];
Real C2_0[4,1];

// Dimensions
final parameter Mass m1=0.241 "mass of motor";
final parameter Mass m2=0.231 "mass of motor";
final parameter Length upperArmDim[1,3]=[0.3, 0.05, 0.01] "LBH - link";
final parameter Length lowerArmDim[1,3]=[0.3, 0.05, 0.01] "LBH - link";
final parameter Density linkDensity=2700 "kg/m3 - aluminum";
final parameter Mass upperArmMass = upperArmDim[1,1]*upperArmDim[1,2]*upperArmDim[1,3]*linkDensity;
final parameter Mass lowerArmMass = lowerArmDim[1,1]*lowerArmDim[1,2]*lowerArmDim[1,3]*linkDensity;

// Gravitational acceleration in 0 coordinates
final parameter Acceleration g0[1,4]=[9.81, 0, 0, 0];

// Rotation matrices
Real T01[4,4];
Real T12[4,4];

// Energy
Energy u1 "Potential energy";
Energy u2;
Energy k1 "Kinetic energy in global frame";
Energy k2 "Kinetic energy in global frame";

// Velocities
Velocity v1[4,1];
Velocity v2[4,1];

// Inertia of joints
final parameter Inertia Ixx1 = (upperArmMass+m1) * (4*upperArmDim[2]*upperArmDim[3]-2*upperArmDim[3]*upperArmDim[3])/12;
final parameter Inertia Iyy1 = a1*a1*(upperArmMass/3+m2);
final parameter Inertia Izz1 = Iyy1;
final parameter Inertia Ixx2 = (lowerArmMass+m2) * (4*lowerArmDim[2]*lowerArmDim[3]-2*lowerArmDim[3]*lowerArmDim[3])/12;
final parameter Inertia Iyy2 = a2*a2*(lowerArmMass/3+m2);
final parameter Inertia Izz2 = Iyy2;
final parameter Inertia I1[3,3] = diagonal({Ixx1, Iyy1, Izz1});
final parameter Inertia I2[3,3] = diagonal({Ixx2, Iyy2, Izz2});
Inertia I1_0[3,3] "Global Coordinates";
Inertia I2_0[3,3] "Global Coordinates";


//***********************************************''
// Equations
//***********************************************''
equation

// Rotation matrices
T01 = [cos(thetaShoulder), -sin(thetaShoulder), 0, a1 * cos(thetaShoulder);
      sin(thetaShoulder), cos(thetaShoulder), 0, a1 * sin(thetaShoulder);
      0, 0, 1, 0;
      0, 0, 0, 1];
T12 = [cos(thetaElbow), -sin(thetaElbow), 0, a2 * cos(thetaElbow);
      sin(thetaElbow), cos(thetaElbow), 0, a2 * sin(thetaElbow);
      0, 0, 1, 0;
      0, 0, 0, 1];

// Projections of centre of mass to the zero frame
C1_0 = T01 * C1_1;
C2_0 = T01*T12 * C2_2;

// Potential energy
u1 = sum(-m1*(g0*C1_0));
u2 = sum(-m2*(g0*C2_0));

// Kinetic energy
v1 = der(C1_0);
v2 = der(C2_0);

// Angular  velocity vectors in local coordinates
w1_1 = [0,0,der(thetaShoulder)];
w2_2 = [0,0,der(thetaElbow)];

// Angular velocity vectors in global coordinates
w1_0 = w1_1;
w2_0 = w1_0 + w2_2*T01[1:3,1:3];

// Inertia in global coordinates
I1_0 = I1;
I2_0 = T01[1:3,1:3]*I2*T01[1:3,1:3];

//k1 = sum(0.5*(m1+upperArmMass)*transpose(v1)*v1+0.5*w1_0*I1_0*transpose(w1_0));
//k2 = sum(0.5*(m2+lowerArmMass)*transpose(v2)*v2+0.5*w2_0*I2_0*transpose(w2_0));

w1_1 = [0, 0, der(thetaShoulder)];
w2_2 = [0, 0, der(thetaElbow)];

a1_0 = der(w1_0);
a2_0 = der(w2_0);

end arm;