#define SAMPLE_F 4 // Hz
#define SAMPLE_T_MS 1000 * 1/SAMPLE_F
#define START_CHAR '$'
#define SHOULDER 1
#define ELBOW 2
#include <TaskScheduler.h>


// Analog inputs
int pin_vel1 = A0;
int pin_cur1 = A1;
int pin_pos1 = A2;
int pin_vel2 = A3;
int pin_cur2 = A4;
int pin_pos2 = A5;


// Outputs
int pin_on1 = 2;
int pin_dir1 = 3;
int pin_pwm1 = 4;
int pin_on2 = 7;
int pin_dir2 = 8;
int pin_pwm2 = 9;



// Callback methods prototypes
void set_pwm();
void measure();

//Tasks
Task t1(1000, TASK_FOREVER, &set_pwm);
Task t2(1000, TASK_FOREVER, &measure);
Scheduler runner;



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

        Serial.println("HERE IS A MESSAGE FOR LOGGING:");
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


void set_pwm(){
        int Bcount, outdir1, outpwm1, outdir2, outpwm2;
        Bcount=Serial.available();
        char input_Buffer[10];
        char pwm1_buffer[3];
        char dir1_buffer[1];
        char pwm2_buffer[3];
        char dir2_buffer[1];

        if (Bcount >= 9){ /* 1 byte for direction (0 or 1), 3 byte for pwm (0-100 %), 1 byte for newline*/
                Serial.readBytes(input_Buffer, Bcount);

                Serial.println("THIS IS WHAT WAS RECEIVED");
                Serial.println(input_Buffer);


                memcpy(dir1_buffer, input_Buffer, 1);
                outdir1=atoi(dir1_buffer);
                memcpy(pwm1_buffer, &input_Buffer[1], 3);
                outpwm1=atoi(pwm1_buffer);



                memcpy(dir2_buffer, &input_Buffer[4], 1);
                outdir2=atoi(dir2_buffer);
                memcpy(pwm2_buffer, &input_Buffer[5], 3);
                outpwm2=atoi(pwm2_buffer);

                digitalWrite(pin_dir1,outdir1);
                digitalWrite(pin_dir2,outdir2);
                analogWrite(pin_pwm1,outpwm1);
                analogWrite(pin_pwm2,outpwm2);
                digitalWrite(pin_on1,1);
                digitalWrite(pin_on2,1);
                Serial.println("HERE IS WHAT WAS WRITTEN:");
                Serial.print(pin_dir1);
                Serial.println(pin1_pwm);

        }

}


void setup(){
        Serial.begin(9600);

        Serial.println("Scheduler running");

        
        pinMode(pin_on1,OUTPUT);
        pinMode(pin_on2,OUTPUT);
        pinMode(pin_dir1,OUTPUT);
        pinMode(pin_dir2,OUTPUT);

        runner.init();

        runner.addTask(t1);

        runner.addTask(t2);

        t1.enable();

//        t2.enable();
}



void loop(){

        runner.execute();

}
