#define SAMPLE_F 4 // Hz
#define SAMPLE_T_MS 1000 * 1/SAMPLE_F
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

void sendMeas(int joint, unsigned long time, int ang, int vel, int cur){

Serial.println(START_CHAR);
Serial.print(',');
Serial.print(joint);
Serial.print(',');
Serial.print(time);
Serial.print(',');
Serial.print(ang);
Serial.print(',');
Serial.print(vel);
Serial.print(',');
Serial.println(cur);

}

void measure(){
int vel1, cur1, ang1;
int vel2, cur2, ang2;

ang1 = getPos(SHOULDER);
cur1 = getCur(SHOULDER);
vel1 = getVel(SHOULDER);
time = millis();
sendMeas(SHOULDER, time, ang1, vel1, cur1);

ang2 = getPos(ELBOW);
cur2 = getCur(ELBOW);
vel2 = getVel(ELBOW);
sendMeas(ELBOW, time, ang2, vel2, cur2);
}

void setup(){
    Serial.begin(9600);
}

void loop(){

}
