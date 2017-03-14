#include <stdio.h>
#include "MatrixMath.h"

#define SAMPLE_F 100 // Hz
#define SAMPLE_T_MS 1000 * 1/SAMPLE_F
#define SHOULDER 0
#define ELBOW 1

const int REF_LEN=12;
const char START_CHAR='$';
const char REF_CHAR='R';

const float k_m[2][4] = {{12, 0, 3.5, 0},{0, 12, 0, 3.5}};
const float ktN[2] = {0.28249, 0.26178};
// const float k_m[2][4] = {{3, 0, 0, 0},{0, 3, 0, 0}};

float n_v[2], B_m[2][2], u_v[2], y_v[4], r_v[4];
int meas[4] = {0,0,0,0};
float ref[4] = {0,0,0,0};

bool led = false;
bool on = false;

// Analog inputs
int pin_cur2 = A0;
int pin_vel2 = A1;
int pin_pos2 = A2;
int pin_cur1 = A3;
int pin_vel1 = A4;
int pin_pos1 = A5;


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

  }


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


float getPos(int joint){

    if (joint == SHOULDER){
        return analogRead(pin_pos1) * -0.001681795 + 3.1331837;
    }
    else if (joint == ELBOW){
        return analogRead(pin_pos2) * -0.00165696 + 3.4945247;
    }
    else{
        return 0;
    }
}

float getCur(int joint){

    int reading;

    if (joint == SHOULDER){
        // return (analogRead(pin_cur1) * 0.0014652 - 3.1414);
        reading = analogRead(pin_cur1);
        return ((reading-2144) * 0.0014652);
    }
    else if (joint == ELBOW){
        // return (analogRead(pin_cur2) * 0.0004884 - 1.0471);
        reading = analogRead(pin_cur2);
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
        reading = analogRead(pin_vel1);
        return ((reading-2144) * 0.153398)* 0.02; // 0.02 is due to gear ratio
    }
    else if (joint == ELBOW){
        // return (analogRead(pin_vel2) * 0.153398 - 328.8852);
        reading = analogRead(pin_vel2);
        return ((reading-2144) * 0.153398)* 0.02;
    }
    else{
        return -1;
    }
}

void sendMeas(int joint, unsigned long time, int pos, int vel, int cur){

    char msg[50];

    sprintf(msg, "%c,%d,%lu,%d,%d,%d,%d",START_CHAR,joint,time,pos,vel,cur,ref[joint]);
    Serial.println(msg);
}

void measure(){

    unsigned long time;
    time = millis();

    sendMeas(SHOULDER, time,    (int)(100*getPos(SHOULDER)),    (int)(100*getVel(SHOULDER)),    (int)(100*getCur(SHOULDER)));
    sendMeas(ELBOW, time,       (int)(100*getPos(ELBOW)),       (int)(100*getVel(ELBOW)),       (int)(100*getCur(ELBOW)));

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

    ref[0] = atoi(pos1_buff);
    ref[1] = atoi(pos2_buff);
    ref[2] = atoi(vel1_buff);
    ref[3] = atoi(vel2_buff);
    
}


void controller(){

    float e_v[4], k_tmp[2],B_tmp[2], u_tmp[2];
    char msg1[100],msg2[100],msg3[100];

    r_v[0] = (float)ref[0]*0.01;
    r_v[1] = (float)ref[1]*0.01;
    r_v[2] = (float)ref[2]*0.01;
    r_v[3] = (float)ref[3]*0.01;

    y_v[0] = meas[0];
    y_v[1] = meas[1];
    y_v[2] = meas[2];
    y_v[3] = meas[3];

    Matrix.Subtract(r_v,y_v,4,1,e_v);                               // e_v = r_v -y_v

    B(y_v[0], y_v[1], y_v[2], y_v[3]);
    n(y_v[0], y_v[1], y_v[2], y_v[3]);

    Matrix.Multiply((float*)k_m,(float*)e_v,2,4,1,(float*)k_tmp);   // k_tmp = k_m * e_v
    Matrix.Multiply((float*)B_m,(float*)k_tmp,2,2,1,(float*)B_tmp); // B_tmp = B_m * k_tmp
    Matrix.Add(B_tmp,n_v,2,1,u_tmp);                                // u_v = B_tmp + n_v
    u_v[0] = u_tmp[0] * ktN[0];
    u_v[1] = u_tmp[1] * ktN[1];

    sprintf(msg1,"%d,%d",(int)(u_v[0]*100),(int)(u_v[1]*100));
    Serial.println(msg1);

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

    if (inByte == START_CHAR){

        getInput();
        controller();

    }

    if (inByte == REF_CHAR){

        getRef();

    }

}