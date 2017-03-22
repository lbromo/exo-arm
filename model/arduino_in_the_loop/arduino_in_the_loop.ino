#include <stdio.h>
#include "AxoArmUtils.h"
#include <string.h>

using namespace AxoArm;

#define SAMPLE_F 100 // Hz
#define SAMPLE_T_MS 1000 * 1/SAMPLE_F
#define SHOULDER 0
#define ELBOW 1

const int PWM_MAX = 230;
const int PWM_MIN = 25;
const int REF_LEN=12;
const char START_CHAR='$';
const char REF_CHAR='R';
const char END_CHAR='E';

const float Nkt0 = 3.54;
const float Nkt1 = 3.82;

Vector meas(4);
Vector ref(4);
Vector u;

Matrix K(2,4);


bool on = false;

void setup(){

    Serial.begin(230400);
      //analogReference(EXTERNAL);

    K[0][0] = 12;
    K[0][2] = 3.5;
    K[1][1] = 12;
    K[1][3] = 3.5;

/*
    K[0][0] = 50;
    K[0][2] = 10;
    K[1][1] = 50;
    K[1][3] = 10;
*/
}


void getInput(){

    char* pos1_buff, *pos2_buff, *vel1_buff, *vel2_buff;
    char buff[50];
    char msg[50];
    
    Serial.readBytesUntil(END_CHAR,buff,50);

    pos1_buff = strtok(buff,",");
    pos2_buff = strtok(NULL,",");
    vel1_buff = strtok(NULL,",");
    vel2_buff = strtok(NULL,",");

    meas[0] = 0.01 * atoi(pos1_buff);
    meas[1] = 0.01 * atoi(pos2_buff);
    meas[2] = 0.01 * atoi(vel1_buff);
    meas[3] = 0.01 * atoi(vel2_buff);
    
    // sprintf(msg,"%3d,%3d,%3d,%3d", (int)(100*meas[0]),(int)(100*meas[1]),(int)(100*meas[2]),(int)(100*meas[3]));
    // Serial.println(msg);

}

void getRef(){

    char *pos1_buff, *pos2_buff, *vel1_buff, *vel2_buff;
    char buff[50];

    Serial.readBytesUntil(END_CHAR,buff,50);

    pos1_buff = strtok(buff,",");
    pos2_buff = strtok(NULL,",");
    vel1_buff = strtok(NULL,",");
    vel2_buff = strtok(NULL,",");

    ref[0] = 0.01 * atoi(pos1_buff);
    ref[1] = 0.01 * atoi(pos2_buff);
    ref[2] = 0.01 * atoi(vel1_buff);
    ref[3] = 0.01 * atoi(vel2_buff);
    
}

int cur2pwm(int joint, float cur){

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

void applyControl(){
    char msg[100];

    int dir_shoulder, dir_elbow;
    int pwm_shoulder, pwm_elbow;

    dir_shoulder    = getDir(u[SHOULDER]);
    dir_elbow       = getDir(u[ELBOW]);

    pwm_shoulder    = cur2pwm(SHOULDER, u[SHOULDER]);
    pwm_elbow       = cur2pwm(ELBOW, u[ELBOW]);

    sprintf(msg,"%d,%d,%d,%d",pwm_shoulder,pwm_elbow,dir_shoulder,dir_elbow);
    Serial.println(msg);

}


void ctrl(){
    char msg[100];

    u = controller(meas,ref, K);
  
    u[0] /= Nkt0;
    u[1] /= Nkt1;

    sprintf(msg,"%d,%d",(int)(100 * u[0]),(int)(100 * u[1]));
    //Serial.println(msg);
    applyControl();

}


void loop(){

    char inByte;

    if(Serial.available())
    {
        inByte = Serial.read();
    } else {
        inByte = '\0';
    }

    if (inByte == START_CHAR){

        getInput();
        ctrl();

    }

    if (inByte == REF_CHAR){

        getRef();

    }

}
