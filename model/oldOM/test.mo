model test

axoArm_basedOnMatlab arm;

dcMotor shoulderMotor(ra = 1.24, la=0.00056, ke=374, kt=0.0255);
dcMotor elbowMotor(ra = 1.24, la=0.00056, ke=374, kt=0.0255);
Modelica.Mechanics.Rotational.Components.Fixed fixed;
Modelica.Electrical.Analog.Sources.SupplyVoltage va(Vps=12);
/*Real A1[4,4];
Real A2[4,4];
parameter Real a1 = 0.3;
parameter Real a2 = 0.2;
Real angle1;
Real angle2;
Real T1[4, 4];
Real T2[4, 4];
//Real point1[2];
//Real point2[2];
*/
equation

connect(va.pin_p, shoulderMotor.p);
connect(va.pin_p, elbowMotor.p);
connect(va.pin_n, shoulderMotor.n);
connect(va.pin_n, elbowMotor.n);

connect(shoulderMotor.axel, arm.shoulderFlange);
connect(elbowMotor.axel, arm.elbowFlange);
connect(shoulderMotor.intsup.flange, fixed.flange);
connect(elbowMotor.intsup.flange, fixed.flange);
/*
angle1 = shoulderMotor.phi;
angle2 = shoulderMotor.phi;

A1 = [cos(angle1),-sin(angle1)*cos(0),0,a1*cos(angle1);sin(angle1),cos(angle1)*cos(0),0,a1*sin(angle1);0,sin(0),cos(0),0;0,0,0,1];

A2 = [cos(angle2), -sin(angle2)*cos(0),0,a2*cos(angle2);sin(angle2),cos(angle2)*cos(0),0,a2*sin(angle2);0,sin(0),cos(0),0;0,0,0,1];

T1 = A1;
T2 = A1*A2;
*/
end test;