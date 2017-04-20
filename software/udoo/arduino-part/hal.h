#include "Arduino.h"

namespace AxoArm{
	const int SAMPLE_F = 200; // Hz
	const unsigned long SAMPLE_T_MS = 1000 * 1/SAMPLE_F;
	const unsigned long SAMPLE_T_US = 1000000 * 1/SAMPLE_F;
	const int SHOULDER = 0;
	const int ELBOW = 1;

	const int PWM_MAX = 230;
	const int PWM_MIN = 25;
	const int REF_LEN = 50;

	const char START_CHAR = '$';
	const char MEAS_CHAR = 'M';
	const char REF_CHAR = 'R';
	const char STOP_CHAR = 'S';
	const char END_CHAR = 'E';

	const float Nkt0 = 3.54; // Gear and motor constant multipliers
	const float Nkt1 = 3.82;
	const int N_STATES = 4; // Number of states

	// Analog inputs
	const int pin_cur_elbow = A3;
	const int pin_vel_elbow = A4;
	const int pin_pos_elbow = A5;
	const int pin_cur_shoulder = A0;
	const int pin_vel_shoulder = A1;
	const int pin_pos_shoulder = A2;

	// Outputs
	const int pin_on_elbow = 2;
	const int pin_dir_elbow = 3;
	const int pin_pwm_elbow = 5; // 5 for normal Arduino
	const int pin_on_shoulder = 7;
	const int pin_dir_shoulder = 8;
	const int pin_pwm_shoulder = 9;

	float getPos(int joint);
	float getCur(int joint);
	float getVel(int joint);
	int cur2pwm(int joint, float cur);
	int getDir(float u);
}
