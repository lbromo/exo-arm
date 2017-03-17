#include <stdio.h>
#include "AxoArmUtils.h"
#include <string.h>

using namespace AxoArm;

#define SAMPLE_F 100 // Hz
#define SAMPLE_T_MS 1000 * 1/SAMPLE_F
#define SHOULDER 0
#define ELBOW 1

const int REF_LEN=12;
const char START_CHAR='$';
const char REF_CHAR='R';
const char END_CHAR='E';

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


void ctrl(){

    char msg[100];

    auto u = controller(meas,ref, K);

    u[0] = u[0] * 0.282485875706215;
    u[1] = u[1] * 0.261780104712042;

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
