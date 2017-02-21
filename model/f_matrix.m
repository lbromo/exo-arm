function F = fcn(dth, vm, cm, N, sigmoidpar)


Fmatrix = [...
	vm(1)*dth(1)+ cm(1)*(2./(1+exp(-sigmoidpar(1) * dth(1)))-1);... +cm(1)*sign(dth(1));...
	vm(2)*dth(2) + cm(2)*(2./(1+exp(-sigmoidpar(2) * dth(2)))-1)...+cm(2)*sign(dth(2));...
];


F = Fmatrix*(N^2);