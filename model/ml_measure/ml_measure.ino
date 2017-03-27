#include <stdio.h>
#include "AxoArmUtils.h"

using namespace AxoArm;

#define SAMPLE_F 100 // Hz
#define SAMPLE_T_MS 1000 * 1/SAMPLE_F
#define SHOULDER 0
#define ELBOW 1

const int PWM_MAX = 230;
const int PWM_MIN = 25;
const int REF_LEN = 50;
const char START_CHAR='$';
const char RDY_CHAR ='&';
const char REF_CHAR ='R';
const char STOP_CHAR = 'S';
const char END_CHAR = 'E';

const float Nkt0 = 3.54;
const float Nkt1 = 3.82;

Vector meas(4);
Vector ref(4);

Matrix K(2,4);

bool on = false;

int dir_shoulder, dir_elbow;
int pwm_shoulder, pwm_elbow;


void ctrl();


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

bool newRef = 0;
bool led = false;

void setup(){

    Serial.begin(230400);

  #ifdef ARDUINO
  analogReference(EXTERNAL);
  #endif
    
    pinMode(pin_on_shoulder,OUTPUT);
    pinMode(pin_dir_shoulder,OUTPUT);
    pinMode(pin_pwm_shoulder,OUTPUT);

    pinMode(pin_on_elbow,OUTPUT);
    pinMode(pin_dir_elbow,OUTPUT);
    pinMode(pin_pwm_elbow,OUTPUT);

    pinMode(13,OUTPUT);
    pinMode(12,OUTPUT);

#ifdef __arm__
    analogReadResolution(12);
#endif

    analogWrite(pin_pwm_shoulder, 25);
    analogWrite(pin_pwm_elbow, 25);

    
    K[0][0] = 12;
    K[0][2] = 3;
    K[1][1] = 12;
    K[1][3] = 3;
    
    /*
    K[0][0] = 6;
    K[0][2] = 1;
    K[1][1] = 6;
    K[1][3] = 1;
    */

  }


float getPos(int joint){

    if (joint == SHOULDER){
        return (4 * analogRead(pin_pos_shoulder) * -0.001681795 + 3.1331837);
    }
    else if (joint == ELBOW){
        return (4 * analogRead(pin_pos_elbow) * -0.00165696 + 3.4945247);
    }
    else{
        return 0;
    }
}

float getCur(int joint){

    int reading;

    if (joint == SHOULDER){
        // return (analogRead(pin_cur1) * 0.0014652 - 3.1414);
        reading = 4 * analogRead(pin_cur_shoulder);
        return ((reading-2144) * 0.0014652);
    }
    else if (joint == ELBOW){
        // return (analogRead(pin_cur2) * 0.0004884 - 1.0471);
        reading = 4 * analogRead(pin_cur_elbow);
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
        reading = 4 * analogRead(pin_vel_shoulder);
        return (((reading-2144) * 0.153398)* 0.02); // 0.02 is due to gear ratio
    }
    else if (joint == ELBOW){
        // return (analogRead(pin_vel2) * 0.153398 - 328.8852);
        reading = 4 * analogRead(pin_vel_elbow);
        return (((reading-2144) * 0.153398)* 0.02);
    }
    else{
        return -1;
    }
}

void sendMeas(unsigned long time, int spos, int svel, int scur, int epos, int evel, int ecur){

    char msg[100];

    sprintf(msg, "%d,%d,%d,%d",spos,svel,epos,evel);
    Serial.println(msg);
}

void measure(){

    unsigned long time;
    time = millis();

    // sendMeas(SHOULDER, time,    (int)(100*getPos(SHOULDER)),    (int)(100*getVel(SHOULDER)),    (int)(100*getCur(SHOULDER)));
    // sendMeas(ELBOW, time,       (int)(100*getPos(ELBOW)),       (int)(100*getVel(ELBOW)),       (int)(100*getCur(ELBOW)));

    sendMeas(time,(int)(100*getPos(SHOULDER)),    (int)(100*getVel(SHOULDER)),    (int)(100*getCur(SHOULDER)),
                  (int)(100*getPos(ELBOW)),       (int)(100*getVel(ELBOW)),       (int)(100*getCur(ELBOW)));

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
        pwm = (int)(fabs(cur) * (PWM_MAX-PWM_MIN)/3.0);
    }
    else if (joint == ELBOW){
        pwm = (int)(fabs(cur) * (PWM_MAX-PWM_MIN)/1.0);
    }

    pwm += PWM_MIN;

    if (pwm > PWM_MAX){
        pwm = PWM_MAX;
    } else if (pwm < PWM_MIN){
        pwm = PWM_MIN;
    }

    return pwm;

}


void loop(){

    char inByte;

    digitalWrite(pin_on_shoulder,false);
    digitalWrite(pin_on_elbow,false);

    if(Serial.available())
    {
        inByte = Serial.read();
    } else {
        inByte = '\0';
    }

    if (inByte == RDY_CHAR){

        measure();
      digitalWrite(13,on);
      on = !on;
    }
        
}
