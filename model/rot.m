function [position1, position2] = rot(angle1, angle2)


a1 = 0.3; % meter

A1 = [cos(angle1) sin(angle1)*-cos(0) 0 a1*cos(angle1);
	sin(angle1) cos(angle1)*cos(0) 0 a1*sin(angle1);
	0 sin(0) cos(0) 0;
	0 0 0 1 ];


a2 = 0.2;

A2 = [cos(angle2) sin(angle2)*-cos(0) sin(angle2)*sin(0) a2*cos(angle2);
	sin(angle2) cos(angle2)*cos(0) cos(angle2)*-sin(0) a2*sin(angle2);
	0 sin(0) cos(0) 0;
	0 0 0 1 ];

T2 = A1 * A2;
T1 = A1;

position1 = [T1(1,end) T1(2,end)];
position2 = [T2(1,end) T2(2,end)];

end