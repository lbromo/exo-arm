/*==========================================================
 * arduino_feedback_lin.c - Test function to validate feedback linearization
 *
 * This is a MEX-file for MATLAB.
 * Copyright 2007-2012 x[1] MathWorks, Inc.
 *
 *========================================================*/
#include <math.h>
#include "mex.h"
#include "matrix.h"

void n(double *x, double *n_v)
{
    n_v[0]= x[2]*4.86725E-1+sin(x[1]+x[0])*1.591091295955199E-1+sin(x[0])*2.173806515142+4.82E2/(exp(x[2]*(-1.9E1/4.0E2))+1.0)-x[3]*sin(x[1])*(x[3]+x[2]*2.0)*5.35229487936E-3-2.41E2;
    n_v[1] = x[3]*1.101175E-1+sin(x[1]+x[0])*1.5910912959552E-1+(x[2]*x[2])*sin(x[1])*5.35229487936E-3+3.6E1/(exp(x[3]*(-1.299E-1))+1.0)-1.8E1;
}

void B(double *x, double *B_m){

	/*
    B_m[0][0] = cos(x[1])*1.070458975872E-2+4.395832773706053E-1;
    B_m[0][1] = cos(x[1])*5.352294879359999E-3+1.974569836531137E-3;
    B_m[1][0] = cos(x[1])*5.352294879359999E-3+1.974569836531137E-3;
    B_m[1][1] = 1.177245698365311E-1;
	*/
 
    B_m[0] = cos(x[1])*1.070458975872E-2+4.395832773706053E-1;
    B_m[1] = cos(x[1])*5.352294879359999E-3+1.974569836531137E-3;
    B_m[2] = cos(x[1])*5.352294879359999E-3+1.974569836531137E-3;
    B_m[3] = 1.177245698365311E-1;

}

void mexFunction(
	int nOutputs, mxArray *out[],
	int nInputs, const mxArray *in[]
	){

	double *x; /* states */
	char *matrix_type;
	double *u; /* inputs */

	x = mxGetPr(in[0]);
	matrix_type = mxArrayToString(in[1]);
/*
	printf("Variables initialized \n");
	printf("input: %d \n", nInputs);
	printf("output: %d \n", nOutputs);
	printf("Variables loaded \n");
	printf("Type: %c\n", matrix_type[0]);
*/
	if (matrix_type[0] == 'B'){
		out[0] = mxCreateDoubleMatrix(4,1,mxREAL);
		u = mxGetPr(out[0]);
		B(x, u);
	} else if (matrix_type[0] == 'n'){
		out[0] = mxCreateDoubleMatrix(2,1,mxREAL);
		u = mxGetPr(out[0]);
		n(x, u);
	}
}