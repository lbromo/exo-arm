#include <stdio.h>
#include "AxoArmUtils.h"

using namespace AxoArm;

#define SAMPLE_F 100 // Hz
#define SAMPLE_T_MS 1000 * 1/SAMPLE_F
#define SHOULDER 0
#define ELBOW 1

const int PWM_MAX = 235;
const int PWM_MIN = 25;
const int REF_LEN=12;
const char START_CHAR='$';
const char RDY_CHAR ='&';
const char REF_CHAR ='R';
const char STOP_CHAR = 'S';

Vector meas(4);
Vector ref(4);

Matrix K(2,4);

bool on = false;

// Analog inputs
int pin_cur_elbow = A0;
int pin_vel_elbow = A1;
int pin_pos_elbow = A2;
int pin_cur_shoulder = A3;
int pin_vel_shoulder = A4;
int pin_pos_shoulder = A5;


// Outputs
int pin_on_shoulder = 2;
int pin_dir_shoulder = 3;
int pin_pwm_shoulder = 4; // 5 for normal Arduino
int pin_on_elbow = 7;
int pin_dir_elbow = 8;
int pin_pwm_elbow = 9;

//reference vector
bool newRef = 0;
unsigned long T_c = millis();

void setup(){

    Serial.begin(230400);
      //analogReference(EXTERNAL);
    
    pinMode(pin_on_shoulder,OUTPUT);
    pinMode(pin_dir_shoulder,OUTPUT);
    pinMode(pin_pwm_shoulder,OUTPUT);

    pinMode(pin_on_elbow,OUTPUT);
    pinMode(pin_dir_elbow,OUTPUT);
    pinMode(pin_pwm_elbow,OUTPUT);

    pinMode(13,OUTPUT);
    pinMode(12,OUTPUT);

    analogReadResolution(12);

    analogWrite(pin_pwm_shoulder, 25);
    analogWrite(pin_pwm_elbow, 25);

    K[0][0] = 12;
    K[0][2] = 3.5;
    K[1][1] = 12;
    K[1][3] = 3.5;

  }


float getPos(int joint){

    if (joint == SHOULDER){
        return analogRead(pin_pos_shoulder) * -0.001681795 + 3.1331837;
    }
    else if (joint == ELBOW){
        return analogRead(pin_pos_elbow) * -0.00165696 + 3.4945247;
    }
    else{
        return 0;
    }
}

float getCur(int joint){

    int reading;

    if (joint == SHOULDER){
        // return (analogRead(pin_cur1) * 0.0014652 - 3.1414);
        reading = analogRead(pin_cur_shoulder);
        return ((reading-2144) * 0.0014652);
    }
    else if (joint == ELBOW){
        // return (analogRead(pin_cur2) * 0.0004884 - 1.0471);
        reading = analogRead(pin_cur_elbow);
        return ((reading-2144) * 0.0004884);
    }
    else{
        return -1;
    }
}

float getVel(int joint){
int reading; 

    if (joint == SHOULDER){
        // return (analogRead(pin_vel1) * 0.153398 - 328.8852);
        reading = analogRead(pin_vel_shoulder);
        return ((reading-2144) * 0.153398)* 0.02; // 0.02 is due to gear ratio
    }
    else if (joint == ELBOW){
        // return (analogRead(pin_vel2) * 0.153398 - 328.8852);
        reading = analogRead(pin_vel_elbow);
        return ((reading-2144) * 0.153398)* 0.02;
    }
    else{
        return -1;
    }
}

void sendMeas(int joint, unsigned long time, int pos, int vel, int cur){

    char msg[50];

    sprintf(msg, "%c,%d,%lu,%d,%d,%d",START_CHAR,joint,time,pos,vel,cur);
    Serial.println(msg);
}

void measure(){

    unsigned long time;
    time = millis();

    sendMeas(SHOULDER, time,    (int)(100*getPos(SHOULDER)),    (int)(100*getVel(SHOULDER)),    (int)(100*getCur(SHOULDER)));
    sendMeas(ELBOW, time,       (int)(100*getPos(ELBOW)),       (int)(100*getVel(ELBOW)),       (int)(100*getCur(ELBOW)));

}

void getRef(){

    char pos1_buff[4], pos2_buff[4], vel1_buff[4], vel2_buff[4];
    
    // String terminators for later use with atoi()
    pos1_buff[3] = '\0';
    pos2_buff[3] = '\0';
    vel1_buff[3] = '\0';
    vel2_buff[3] = '\0';

    // Wait for whole message to be available
    while(Serial.available() < REF_LEN) {
        //Serial.println(Serial.available());
    };

    Serial.readBytes(pos1_buff,3);
    Serial.readBytes(pos2_buff,3);
    Serial.readBytes(vel1_buff,3);
    Serial.readBytes(vel2_buff,3);

    ref[0] = 0.01 * atoi(pos1_buff);
    ref[1] = 0.01 * atoi(pos2_buff);
    ref[2] = 0.01 * atoi(vel1_buff);
    ref[3] = 0.01 * atoi(vel2_buff);
    
}

int convert2pwm(int joint, float cur){

    int pwm = 0;

    if (joint == SHOULDER){
        pwm = (int)(abs(cur) * (PWM_MAX-PWM_MIN)/3.0);
    }
    else if (joint == ELBOW){
        pwm = int(abs(cur) * (PWM_MAX-PWM_MIN)/1.0);
    }

    pwm += PWM_MIN;

    if (pwm > PWM_MAX){
        pwm = PWM_MAX;
    } else if (pwm < PWM_MIN){
        pwm = PWM_MIN;
    }

    return pwm;

}

int getDir(float u){

    return (int)(u > 0);
}

void applyControl(float* u){

    int dir_shoulder, dir_elbow;
    int pwm_shoulder, pwm_elbow;

    dir_shoulder    = getDir(u[SHOULDER]);
    dir_elbow       = getDir(u[ELBOW]);

    pwm_shoulder    = convert2pwm(SHOULDER, u[SHOULDER]);
    pwm_elbow       = convert2pwm(ELBOW, u[ELBOW]);

    digitalWrite(pin_dir_shoulder, dir_shoulder);
    digitalWrite(pin_dir_elbow, dir_elbow);

    analogWrite(pin_pwm_shoulder, pwm_shoulder);
    analogWrite(pin_pwm_elbow, pwm_elbow);

}

void ctrl(){

    meas[0] = getPos(SHOULDER);
    meas[1] = getPos(ELBOW);
    meas[2] = getVel(SHOULDER);
    meas[3] = getVel(ELBOW);

    controller(meas,ref,K);

}


void loop(){

    char inByte;

    digitalWrite(pin_on_shoulder,on);
    digitalWrite(pin_on_elbow,on);

    if(Serial.available())
    {
        inByte = Serial.read();
    } else {
        inByte = '\0';
    }

    if (inByte == RDY_CHAR){

        measure();

    }
    else if (inByte == REF_CHAR){

        getRef();
        newRef = 1;
        on = true;
        
    }
    else if (inByte == STOP_CHAR){

        on = false;
    }
        
    if (millis() >= (T_c + SAMPLE_T_MS))
    {
        T_c = millis();
        ctrl();
    }

}
