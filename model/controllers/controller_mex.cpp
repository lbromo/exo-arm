/*==========================================================
 * arduino_feedback_lin.c - Test function to validate feedback linearization
 *
 * This is a MEX-file for MATLAB.
 * Copyright 2007-2012 x[1] MathWorks, Inc.
 *
 *========================================================*/
#include <math.h>
#include "mex.h"
#include <AxoArmUtils.h>

using namespace AxoArm;

void mexFunction(
	int nOutputs, mxArray *out[],
	int nInputs, const mxArray *in[]
	){

	double *x; /* states */
	double *u; /* inputs */
	double *ref;/* reference */

	x = mxGetPr(in[0]);
	ref = mxGetPr(in[1]);

	out[0] = mxCreateDoubleMatrix(2,1,mxREAL);
	u = mxGetPr(out[0]);

	Vector x_v(4), ref_v(4);
	Matrix K(2,4);

	for (int i; i<4; i++){
		x_v[i] = x[i];
		ref_v[i] = ref[i];
	}

	K[0][0] = 12;
	K[1][1] = 12;
	K[0][2] = 3.5;
	K[1][3] = 3.5;

	auto u_v = controller(x_v,ref_v,K);

	u[0] = u_v[0] * 0.282485875706215;
	u[1] = u_v[1] * 0.261780104712042;

}