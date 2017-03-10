#include <stdio.h>
#include "MatrixMath.h"

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

const float k_m[2][4] = {{12, 0, 3.5, 0},{0, 12, 0, 3.5}};

float n_v[2], B_m[2][2], u_v[2], y_v[4], r_v[4];
int ref[4] = {0,0,0,0};


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
    
    led = 0;
    
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
        return ((reading-2144) * 0.153398);
    }
    else if (joint == ELBOW){
        // return (analogRead(pin_vel2) * 0.153398 - 328.8852);
        reading = analogRead(pin_vel2);
        return ((reading-2144) * 0.153398);
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

    sendMeas(SHOULDER, time,    (int)(100*getPos(SHOULDER)),    (int)(getVel(SHOULDER)),    (int)(100*getCur(SHOULDER)));
    sendMeas(ELBOW, time,       (int)(100*getPos(ELBOW)),       (int)(getVel(ELBOW)),       (int)(100*getCur(ELBOW)));

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

int convert2pwm(int joint, float cur){

    int pwm;

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

    if ( u > 0) {
        return 1;
    }
    return 0;
}

void applyControl(float* u){

    int dir_shoulder, dir_elbow;
    int pwm_shoulder, pwm_elbow;
    char msg[100];

    dir_shoulder = getDir(u[SHOULDER]);
    dir_elbow    = getDir(u[ELBOW]);

    pwm_shoulder = convert2pwm(SHOULDER, u[SHOULDER]);
    pwm_elbow = convert2pwm(ELBOW, u[ELBOW]);

    digitalWrite(pin_dir_shoulder, dir_shoulder);
    digitalWrite(pin_dir_elbow, dir_elbow);

    sprintf(msg,"PWM: %d,%d,%d,%d",pwm_shoulder,dir_shoulder,pwm_elbow,dir_elbow);
    // Serial.println(msg);

    analogWrite(pin_pwm_shoulder, pwm_shoulder);
    analogWrite(pin_pwm_elbow, pwm_elbow);

}

void controller(){

    float e_v[4], k_tmp[2],B_tmp[2];
    char msg1[100],msg2[100],msg3[100];

    r_v[0] = (float)ref[0]*0.01;
    r_v[1] = (float)ref[1]*0.01;
    r_v[2] = (float)ref[2]*0.01;
    r_v[3] = (float)ref[3]*0.01;

    y_v[0] = getPos(SHOULDER);
    y_v[1] = getPos(ELBOW);
    y_v[2] = getVel(SHOULDER);
    y_v[3] = getVel(ELBOW);

    Matrix.Subtract(r_v,y_v,4,1,e_v);

    B(y_v[0], y_v[1], y_v[2], y_v[3]);
    n(y_v[0], y_v[1], y_v[2], y_v[3]);

    Matrix.Multiply((float*)k_m,(float*)e_v,2,4,1,(float*)k_tmp);
    Matrix.Multiply((float*)B_m,(float*)k_tmp,2,2,1,(float*)B_tmp);
    Matrix.Add(B_tmp,n_v,2,1,u_v);


    applyControl(u_v);

    sprintf(msg1,"%d,%d",(int)(u_v[0]*100),(int)(u_v[1]*100));
    // sprintf(msg2,"%d,%d,%d,%d",(int)(y_v[0]*100),(int)(y_v[1]*100),(int)(y_v[2]*100),(int)(y_v[3]*100));
    // sprintf(msg3,"%d,%d,%d,%d",(int)(e_v[0]*100),(int)(e_v[1]*100),(int)(e_v[2]*100),(int)(e_v[3]*100));

    // Matrix.Print((float*)e_v, 4,1,"ERROR");
    // Matrix.Print((float*)u_v, 2,1,"INPUT");

    // Matrix.Print((float*)k_tmp, 2,1,"k_tmp");
    // Matrix.Print((float*)B_tmp, 2,1,"B_tmp");

    // Serial.println(msg1);
    // Serial.println(msg2);
    // Serial.println(msg3);

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
        
    }
    else if (inByte == STOP_CHAR){

        on = !on;
    }
        
    if (millis() >= (T_c + SAMPLE_T_MS))
    {
        T_c = millis();
        controller();
    }

}
