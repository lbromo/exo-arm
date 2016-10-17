function Minv = fcn(th, l1, l2, m1, m2, a1, a2, I1, I2)
%#codegen
%th1 = th(1);
th2 = th(2);

Izz1 = I1(3,3);
Izz2 = I2(3,3);

MinvMatrix = [...
 (m2*a2^2 - 2*m2*a2*l2 + m2*l2^2 + Izz2)/(Izz1*Izz2 + a1^2*a2^2*m2^2 + a1^2*l2^2*m2^2 + Izz2*a1^2*m1 + Izz1*a2^2*m2 + Izz2*a1^2*m2 + Izz2*l1^2*m1 + Izz1*l2^2*m2 - a1^2*a2^2*m2^2*cos(th2)^2 - a1^2*l2^2*m2^2*cos(th2)^2 - 2*a1^2*a2*l2*m2^2 + a1^2*a2^2*m1*m2 + a1^2*l2^2*m1*m2 + a2^2*l1^2*m1*m2 + l1^2*l2^2*m1*m2 - 2*Izz2*a1*l1*m1 - 2*Izz1*a2*l2*m2 + 2*a1^2*a2*l2*m2^2*cos(th2)^2 - 2*a1*a2^2*l1*m1*m2 - 2*a1^2*a2*l2*m1*m2 - 2*a1*l1*l2^2*m1*m2 - 2*a2*l1^2*l2*m1*m2 + 4*a1*a2*l1*l2*m1*m2),                                                      -(m2*a2^2 - 2*m2*a2*l2 + a1*m2*cos(th2)*a2 + m2*l2^2 - a1*m2*cos(th2)*l2 + Izz2)/(Izz1*Izz2 + a1^2*a2^2*m2^2 + a1^2*l2^2*m2^2 + Izz2*a1^2*m1 + Izz1*a2^2*m2 + Izz2*a1^2*m2 + Izz2*l1^2*m1 + Izz1*l2^2*m2 - a1^2*a2^2*m2^2*cos(th2)^2 - a1^2*l2^2*m2^2*cos(th2)^2 - 2*a1^2*a2*l2*m2^2 + a1^2*a2^2*m1*m2 + a1^2*l2^2*m1*m2 + a2^2*l1^2*m1*m2 + l1^2*l2^2*m1*m2 - 2*Izz2*a1*l1*m1 - 2*Izz1*a2*l2*m2 + 2*a1^2*a2*l2*m2^2*cos(th2)^2 - 2*a1*a2^2*l1*m1*m2 - 2*a1^2*a2*l2*m1*m2 - 2*a1*l1*l2^2*m1*m2 - 2*a2*l1^2*l2*m1*m2 + 4*a1*a2*l1*l2*m1*m2);...
 -(m2*a2^2 - 2*m2*a2*l2 + a1*m2*cos(th2)*a2 + m2*l2^2 - a1*m2*cos(th2)*l2 + Izz2)/(Izz1*Izz2 + a1^2*a2^2*m2^2 + a1^2*l2^2*m2^2 + Izz2*a1^2*m1 + Izz1*a2^2*m2 + Izz2*a1^2*m2 + Izz2*l1^2*m1 + Izz1*l2^2*m2 - a1^2*a2^2*m2^2*cos(th2)^2 - a1^2*l2^2*m2^2*cos(th2)^2 - 2*a1^2*a2*l2*m2^2 + a1^2*a2^2*m1*m2 + a1^2*l2^2*m1*m2 + a2^2*l1^2*m1*m2 + l1^2*l2^2*m1*m2 - 2*Izz2*a1*l1*m1 - 2*Izz1*a2*l2*m2 + 2*a1^2*a2*l2*m2^2*cos(th2)^2 - 2*a1*a2^2*l1*m1*m2 - 2*a1^2*a2*l2*m1*m2 - 2*a1*l1*l2^2*m1*m2 - 2*a2*l1^2*l2*m1*m2 + 4*a1*a2*l1*l2*m1*m2), (Izz1 + Izz2 + a1^2*m1 + a1^2*m2 + a2^2*m2 + l1^2*m1 + l2^2*m2 - 2*a1*l1*m1 - 2*a2*l2*m2 + 2*a1*a2*m2*cos(th2) - 2*a1*l2*m2*cos(th2))/(Izz1*Izz2 + a1^2*a2^2*m2^2 + a1^2*l2^2*m2^2 + Izz2*a1^2*m1 + Izz1*a2^2*m2 + Izz2*a1^2*m2 + Izz2*l1^2*m1 + Izz1*l2^2*m2 - a1^2*a2^2*m2^2*cos(th2)^2 - a1^2*l2^2*m2^2*cos(th2)^2 - 2*a1^2*a2*l2*m2^2 + a1^2*a2^2*m1*m2 + a1^2*l2^2*m1*m2 + a2^2*l1^2*m1*m2 + l1^2*l2^2*m1*m2 - 2*Izz2*a1*l1*m1 - 2*Izz1*a2*l2*m2 + 2*a1^2*a2*l2*m2^2*cos(th2)^2 - 2*a1*a2^2*l1*m1*m2 - 2*a1^2*a2*l2*m1*m2 - 2*a1*l1*l2^2*m1*m2 - 2*a2*l1^2*l2*m1*m2 + 4*a1*a2*l1*l2*m1*m2)...
 ];

Minv = MinvMatrix;
