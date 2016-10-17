function V = fcn(th, dth, l2, m2, a1, a2)
%#codegen
%th1 = th(1);
th2 = th(2);


dth1 = dth(1);
dth2 = dth(2);


Vmatrix = [...
	 -a1*m2*sin(th2)*dth2*(2*dth1 + dth2)*(a2 - l2);...
     a1*m2*sin(th2)*dth1^2*(a2 - l2)...
	];

V = Vmatrix; % Even though it's a vector...
 