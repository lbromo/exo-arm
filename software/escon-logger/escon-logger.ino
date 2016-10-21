#define SAMPLE_F 1000 // Hz
#define START_CHAR '$'
#define SHOULDER 1
#define ELBOW 2

// Analog inputs
int pin_vel1 = A0;
int pin_cur1 = A1;
int pin_pos1 = A2;
int pin_vel2 = A3;
int pin_cur2 = A4;
int pin_pos2 = A5;

/*
// Outputs
int pin_on1 = 7;
int pin_dir1 = 8;
int pin_pwm1 = 9;
int pin_on2 = 7;
int pin_dir2 = 8;
int pin_pwm2 = 9;
*/

void setup(){

	Serial.begin(9600);

}


int getPos(int joint){

	if (joint == SHOULDER){
		return analogRead(pin_pos1);
	}
	else if (joint == ELBOW){
		return analogRead(pin_pos2);
	}
	else{
		return -1;
	}
}

int getCur(int joint){

	if (joint == SHOULDER){
		return analogRead(pin_cur1);
	}
	else if (joint == ELBOW){
		return analogRead(pin_cur2);
	}
	else{
		return -1;
	}
}

int getVel(int joint){

	if (joint == SHOULDER){
		return analogRead(pin_vel1);
	}
	else if (joint == ELBOW){
		return analogRead(pin_vel2);
	}
	else{
		return -1;
	}
}


void loop(){

int vel1, cur1, angle1;
int vel2, cur2, angle2;

angle1 = getPos(SHOULDER);
cur1 = getCur(SHOULDER);
vel1 = getVel(SHOULDER);

angle2 = getPos(ELBOW);
cur2 = getCur(ELBOW);
vel2 = getVel(ELBOW);

Serial.print(START_CHAR);
Serial.print(SHOULDER);
Serial.print(vel1);
Serial.print(cur1);
Serial.println(angle1);

}