#include <stdio.h>
#include "MatrixMath.h"

#define SAMPLE_F 100 // Hz
#define SAMPLE_T_MS 1000 * 1/SAMPLE_F
#define SHOULDER 1
#define ELBOW 2


const float k_m[2][4] = {{42.48, 0, 12.39, 0},{0, 45.84, 0, 13.37}};
const int REF_LEN=12;
const char START_CHAR='$';
const char RDY_CHAR ='&';
const char REF_CHAR ='R';

float n_v[2], B_m[2][2], u_v[2], y_v[4], r_v[4];
int ref[4] = {0,0,0,0};


void n(float ths,float the,float dths,float dthe)
{
    n_v[0]= dths*4.86725E-1+sin(the+ths)*1.591091295955199E-1+sin(ths)*2.173806515142+4.82E2/(exp(dths*(-1.9E1/4.0E2))+1.0)-dthe*sin(the)*(dthe+dths*2.0)*5.35229487936E-3-2.41E2;
    n_v[1] = dthe*1.101175E-1+sin(the+ths)*1.5910912959552E-1+(dths*dths)*sin(the)*5.35229487936E-3+3.6E1/(exp(dthe*(-1.299E-1))+1.0)-1.8E1;
}

void B(float ths,float the,float dths,float dthe){
    B_m[0][0] = cos(the)*1.070458975872E-2+4.395832773706053E-1;
    B_m[0][1] = cos(the)*5.352294879359999E-3+1.974569836531137E-3;
    B_m[1][0] = cos(the)*5.352294879359999E-3+1.974569836531137E-3;
    B_m[1][1] = 1.177245698365311E-1;
}

bool led = false;

// Analog inputs
int pin_cur2 = A0;
int pin_vel2 = A1;
int pin_pos2 = A2;
int pin_cur1 = A3;
int pin_vel1 = A4;
int pin_pos1 = A5;


// Outputs
int pin_on1 = 2;
int pin_dir1 = 3;
int pin_pwm1 = 5; // 4 for UDOO
int pin_on2 = 7;
int pin_dir2 = 8;
int pin_pwm2 = 9;

//reference vector
bool newRef = 0;
unsigned long T_c = millis();

void setup(){

    Serial.begin(230400);
      //analogReference(EXTERNAL);
    
    led = 0;
    
    pinMode(pin_on1,OUTPUT);
    pinMode(pin_on2,OUTPUT);
    pinMode(pin_dir1,OUTPUT);
    pinMode(pin_dir2,OUTPUT);
    pinMode(pin_pwm1,OUTPUT);
    pinMode(pin_pwm2,OUTPUT);
    pinMode(13,OUTPUT);
    pinMode(12,OUTPUT);

    analogWrite(pin_pwm1, 25);
    analogWrite(pin_pwm2, 25);

  }


float getPos(int joint){
        if (joint == SHOULDER){
                return (616 - analogRead(pin_pos1)) * 2 * PI / 1232;
        }
        else if (joint == ELBOW){
                return (694 - analogRead(pin_pos2)) * 2 * PI / 1304.1;
        }
        else{
                return -1;
        }
}

float getCur(int joint){

        if (joint == SHOULDER){
                return 0.005865 * (analogRead(pin_cur1) - 511.5);
        }
        else if (joint == ELBOW){
                return 0.005965 * (analogRead(pin_cur2) - 509);
        }
        else{
                return -1;
        }
}

float getVel(int joint){

        if (joint == SHOULDER){
                return (5.865 * analogRead(pin_vel1-511.5)) * (2*PI/60);
        }
        else if (joint == ELBOW){
                return (5.865 * analogRead(pin_vel1-511.5)) * (2*PI/60);
        }
        else{
                return -1;
        }
}

void sendMeas(int joint, unsigned long time, int ang, int vel, int cur){

        char msg[50];
        sprintf(msg, "%c,%f,%f,%f,%f,%f",START_CHAR,joint,time,ang,vel,cur);
        Serial.println(msg);
}

void measure(){

        unsigned long time;
        time = millis();

        sendMeas(SHOULDER, time, getPos(SHOULDER), getVel(SHOULDER), getCur(SHOULDER));
        sendMeas(ELBOW, time, getPos(ELBOW), getVel(ELBOW), getCur(ELBOW));

}

void getRef(){

led =!led;
digitalWrite(13,led);

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

    ref[0] = atoi(pos1_buff);
    ref[1] = atoi(pos2_buff);
    ref[2] = atoi(vel1_buff);
    ref[3] = atoi(vel2_buff);
    
}


void controller(){

    float e_v[4];
    char msg[100];

    r_v[0] = (float)ref[0]*0.01;
    r_v[1] = (float)ref[1]*0.01;
    r_v[2] = (float)ref[2]*0.01;
    r_v[3] = (float)ref[3]*0.01;

    y_v[0] = getPos(SHOULDER);
    y_v[1] = getPos(ELBOW);
    y_v[2] = getVel(SHOULDER);
    y_v[3] = getVel(ELBOW);

    Matrix.Subtract(r_v,y_v,4,1,e_v);

    sprintf(msg,"%d,%d,%d,%d",(int)(e_v[0]*100),(int)(e_v[1]*100),(int)(e_v[2]*100),(int)(e_v[3]*100));

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

    if (inByte == RDY_CHAR){

            measure();

    }
    else if (inByte == REF_CHAR){

        getRef();
        newRef = 1;
        
    }
        
    if (millis() >= (T_c + SAMPLE_T_MS))
    {
        T_c = millis();
        if (newRef)
        {
            controller();
            newRef = 0;
        }
    }

}