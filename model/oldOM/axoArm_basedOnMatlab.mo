model axoArm_basedOnMatlab

// Interfaces
Modelica.Mechanics.Rotational.Interfaces.Flange_a shoulderFlange;
Modelica.Mechanics.Rotational.Interfaces.Flange_a elbowFlange;


// Constants
final parameter Real g = 9.81;

// Link 1
final parameter Real d1 = 0;
final parameter Real a1 = 0.25 "distance from frame 0 to frame 1 along x1";
final parameter Real alpha1 = 0;
final parameter Real l1 = 3.5e-1;
final parameter Real m1 = 0.241 "link mass"; 

// Link 2
final parameter Real d2 = 0;
final parameter Real a2 = 0.25 "distance from frame 1 to frame 2 along x2";
final parameter Real alpha2 = 0;
final parameter Real l2 = 0.151;
final parameter Real m2 = 0.231 "link mass";

// Link dimensions
final parameter Real wb = 25.4e-3;
final parameter Real tkb = 3e-3;

// Motor masses
final parameter Real mMot1 = 0.14;
final parameter Real mMot2 = 0.176;


final parameter Real inertia1[3, 3] = [a1*a1*((m1-mMot2)/3+mMot1),0,0;0,a1*a1*((m1-mMot2)/3+mMot1),0;0,0, m1*(0.047*0.047+0.04*0.04)/12];

final parameter Real inertia2[3, 3] = [m2*(4*wb*tkb-2*tkb*tkb)/12,0,0; 0,a2*a2*(m2/3+mMot2),0;0,0, a1*a1*((m1-mMot2)/3+mMot1)];

Real theta1(start=0);
Real w_1(start=0);
Real acc_1(start=0);

Real theta2(start=0);
Real w_2(start=0);
Real acc_2(start=0);

Real theta[2,1];
Real acc[2,1];

Real G[2,1];
Real V[2,1];
Real Minv[2,2];
final parameter Real Izz1 = m1*(0.047*0.047+0.04*0.04)/12;
final parameter Real Izz2 = a1*a1*((m1-mMot2)/3+mMot1);
Real tau[2,1];
Real FBtau[2,1];
Real tau_a[2,1];

equation

acc= [acc_1; acc_2];
theta = [theta1; theta2];

theta = [shoulderFlange.phi; elbowFlange.phi]; 
tau = [shoulderFlange.tau; elbowFlange.tau];

G = [g*(a1*m1*sin(theta1)+a1*m2*sin(theta1)-l1*m1*sin(theta1)+a2*m2*sin(theta1+theta2-l2*m2*sin(theta1+theta2))); g*m2*sin(theta1+theta2)*(a2-12)];

V = [-a1*m2*sin(theta2)*w_2*(2*w_1+w_2)*(a2-12); a1*m2*sin(theta2)*w_1*w_1*(a2-12)];

Minv = [ (m2*a2*a2 - 2*m2*a2*l2 + m2*l2*l2 + Izz2)/(Izz1*Izz2 + a1*a1*a2*a2*m2*m2 + a1*a1*l2*l2*m2*m2 + Izz2*a1*a1*m1 + Izz1*a2*a2*m2 + Izz2*a1*a1*m2 + Izz2*l1*l1*m1 + Izz1*l2*l2*m2 - a1*a1*a2*a2*m2*m2*cos(theta2)*cos(theta2) - a1*a1*l2*l2*m2*m2*cos(theta2)*cos(theta2) - 2*a1*a1*a2*l2*m2*m2 + a1*a1*a2*a2*m1*m2 + a1*a1*l2*l2*m1*m2 + a2*a2*l1*l1*m1*m2 + l1*l1*l2*l2*m1*m2 - 2*Izz2*a1*l1*m1 - 2*Izz1*a2*l2*m2 + 2*a1*a1*a2*l2*m2*m2*cos(theta2)*cos(theta2) - 2*a1*a2*a2*l1*m1*m2 - 2*a1*a1*a2*l2*m1*m2 - 2*a1*l1*l2*l2*m1*m2 - 2*a2*l1*l1*l2*m1*m2 + 4*a1*a2*l1*l2*m1*m2) , (m2*a2*a2 - 2*m2*a2*l2 + m2*l2*l2 + Izz2)/(Izz1*Izz2 + a1*a1*a2*a2*m2*m2 + a1*a1*l2*l2*m2*m2 + Izz2*a1*a1*m1 + Izz1*a2*a2*m2 + Izz2*a1*a1*m2 + Izz2*l1*l1*m1 + Izz1*l2*l2*m2 - a1*a1*a2*a2*m2*m2*cos(theta2)*cos(theta2) - a1*a1*l2*l2*m2*m2*cos(theta2)*cos(theta2) - 2*a1*a1*a2*l2*m2*m2 + a1*a1*a2*a2*m1*m2 + a1*a1*l2*l2*m1*m2 + a2*a2*l1*l1*m1*m2 + l1*l1*l2*l2*m1*m2 - 2*Izz2*a1*l1*m1 - 2*Izz1*a2*l2*m2 + 2*a1*a1*a2*l2*m2*m2*cos(theta2)*cos(theta2) - 2*a1*a2*a2*l1*m1*m2 - 2*a1*a1*a2*l2*m1*m2 - 2*a1*l1*l2*l2*m1*m2 - 2*a2*l1*l1*l2*m1*m2 + 4*a1*a2*l1*l2*m1*m2) ; -(m2*a2*a2 - 2*m2*a2*l2 + a1*m2*cos(theta2)*a2 + m2*l2*l2 - a1*m2*cos(theta2)*l2 + Izz2)/(Izz1*Izz2 + a1*a1*a2*a2*m2*m2 + a1*a1*l2*l2*m2*m2 + Izz2*a1*a1*m1 + Izz1*a2*a2*m2 + Izz2*a1*a1*m2 + Izz2*l1*l1*m1 + Izz1*l2*l2*m2 - a1*a1*a2*a2*m2*m2*cos(theta2)*cos(theta2) - a1*a1*l2*l2*m2*m2*cos(theta2)*cos(theta2) - 2*a1*a1*a2*l2*m2*m2 + a1*a1*a2*a2*m1*m2 + a1*a1*l2*l2*m1*m2 + a2*a2*l1*l1*m1*m2 + l1*l1*l2*l2*m1*m2 - 2*Izz2*a1*l1*m1 - 2*Izz1*a2*l2*m2 + 2*a1*a1*a2*l2*m2*m2*cos(theta2)*cos(theta2) - 2*a1*a2*a2*l1*m1*m2 - 2*a1*a1*a2*l2*m1*m2 - 2*a1*l1*l2*l2*m1*m2 - 2*a2*l1*l1*l2*m1*m2 + 4*a1*a2*l1*l2*m1*m2) , (Izz1 + Izz2 + a1*a1*m1 + a1*a1*m2 + a2*a2*m2 + l1*l1*m1 + l2*l2*m2 - 2*a1*l1*m1 - 2*a2*l2*m2 + 2*a1*a2*m2*cos(theta2) - 2*a1*l2*m2*cos(theta2))/(Izz1*Izz2 + a1*a1*a2*a2*m2*m2 + a1*a1*l2*l2*m2*m2 + Izz2*a1*a1*m1 + Izz1*a2*a2*m2 + Izz2*a1*a1*m2 + Izz2*l1*l1*m1 + Izz1*l2*l2*m2 - a1*a1*a2*a2*m2*m2*cos(theta2)*cos(theta2) - a1*a1*l2*l2*m2*m2*cos(theta2)*cos(theta2) - 2*a1*a1*a2*l2*m2*m2 + a1*a1*a2*a2*m1*m2 + a1*a1*l2*l2*m1*m2 + a2*a2*l1*l1*m1*m2 + l1*l1*l2*l2*m1*m2 - 2*Izz2*a1*l1*m1 - 2*Izz1*a2*l2*m2 + 2*a1*a1*a2*l2*m2*m2*cos(theta2)*cos(theta2) - 2*a1*a2*a2*l1*m1*m2 - 2*a1*a1*a2*l2*m1*m2 - 2*a1*l1*l2*l2*m1*m2 - 2*a2*l1*l1*l2*m1*m2 + 4*a1*a2*l1*l2*m1*m2) ];

tau_a = tau-FBtau;
acc = Minv * tau_a;

w_1 = der(theta1);
acc_1 = der(w_1);
w_2 = der(theta2);
acc_2 = der(w_2);

FBtau = V+G;

end axoArm_basedOnMatlab;