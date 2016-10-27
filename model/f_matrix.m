function F = f_matrix(dth, vm, cm)


Fmatrix = [...
            vm(1)*dth(1) + cm(1)*sign(dth(1));...
            vm(2)*dth(2) + cm(2)*sign(dth(2))...
];

F = Fmatrix;
