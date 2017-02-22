#include <stdio.h>

#define SAMPLE_F 100 // Hz
#define SAMPLE_T_MS 1000 * 1/SAMPLE_F
#define START_CHAR '$'
#define RDY_CHAR '&'
#define SHOULDER 1
#define ELBOW 2
#define MSG_LEN 10

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
int pin_pwm1 = 5;
int pin_on2 = 7;
int pin_dir2 = 8;
int pin_pwm2 = 9;


void setup(){

        Serial.begin(115200);
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

        //Serial.println("HERE IS A MESSAGE FOR LOGGING:");
        char msg[50];
        sprintf(msg, "%c,%d,%d,%d,%d,%d",START_CHAR,joint,time,ang,vel,cur);
        Serial.println(msg);
        // Serial.println(START_CHAR);
        // Serial.print(',');
        // Serial.print(joint);
        // Serial.print(',');
        // Serial.print(time);
        // Serial.print(',');
        // Serial.print(ang);
        // Serial.print(',');
        // Serial.print(vel);
        // Serial.print(',');
        // Serial.println(cur);

}

void measure(){
        int vel1, cur1, ang1;
        int vel2, cur2, ang2;
        unsigned long time;

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

void loop(){


    if ( Serial.read() == RDY_CHAR){
        measure();
        led = !led;
        digitalWrite(13,led);
    }
    

}