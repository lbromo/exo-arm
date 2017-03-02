function F = fcn(dth, vm, cm, N, sigmoidpar)


Fmatrix = [...
	vm(1)*dth(1)+ cm(1) * sigmoid(dth(1),sigmoidpar(1));...%cm(1)*(2./(1+exp(-sigmoidpar(1) * dth(1)))-1);... +cm(1)*sign(dth(1));...
	vm(2)*dth(2)+ cm(2) * sigmoid(dth(2),sigmoidpar(2))...%cm(2)*(2./(1+exp(-sigmoidpar(2) * dth(2)))-1)...+cm(2)*sign(dth(2));...
];

%plot([-100:1:100],vm(2)*[-100:1:100] +cm(2)*(2./(1+exp(-sigmoidpar(2) * [-100:1:100]))-1))
%grid on
%Fmatrix(1)=Fmatrix(1)*0.4;
%Fmatrix(2)=Fmatrix(2)*0.25;
F = Fmatrix*(N^2);