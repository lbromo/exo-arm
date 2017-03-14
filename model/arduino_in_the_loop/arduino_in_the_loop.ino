#include <stdio.h>
#include "AxoArmUtils.h"

using namespace AxoArm;

#define SAMPLE_F 100 // Hz
#define SAMPLE_T_MS 1000 * 1/SAMPLE_F
#define SHOULDER 0
#define ELBOW 1

const int REF_LEN=12;
const char START_CHAR='$';
const char REF_CHAR='R';

Vector meas(4);
Vector ref(4);

Matrix K(2,4);


bool on = false;

void setup(){

    Serial.begin(230400);
      //analogReference(EXTERNAL);

    K[0][0] = 12;
    K[0][2] = 3.5;
    K[1][1] = 12;
    K[1][3] = 3.5;
}


void getInput(){

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

    meas[0] = 0.01 * atoi(pos1_buff);
    meas[1] = 0.01 * atoi(pos2_buff);
    meas[2] = 0.01 * atoi(vel1_buff);
    meas[3] = 0.01 * atoi(vel2_buff);
    
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


void ctrl(){

char msg[50];

auto u = controller(meas,ref, K);

sprintf(msg,"%d,%d",(int)(100*u[0]),(int)(100*u[1]));
Serial.println(msg);

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