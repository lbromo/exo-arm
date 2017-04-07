#define SAMPLE_F 100 // Hz
#define SAMPLE_T_MS 1000 * 1/SAMPLE_F
#define START_CHAR '$'
#define SHOULDER 1
#define ELBOW 2
#define MSG_LEN 10

bool led;

// Analog inputs
int pin_cur1 = A0;
int pin_vel1 = A1;
int pin_pos1 = A2;
int pin_cur2 = A3;
int pin_vel2 = A4;
int pin_pos2 = A5;


// Outputs
int  pin_on2 = 2;
int pin_dir2 = 3;
int pin_pwm2 = 5;
int  pin_on1 = 7;
int pin_dir1 = 8;
int pin_pwm1 = 9;


void setup(){

        analogReference(EXTERNAL);

        Serial.begin(115200);

        Serial.println("Scheduler running");
        
        led = 0;
        
        pinMode(pin_on1,OUTPUT);
        pinMode(pin_on2,OUTPUT);
        pinMode(pin_dir1,OUTPUT);
        pinMode(pin_dir2,OUTPUT);
        pinMode(pin_pwm1,OUTPUT);
        pinMode(pin_pwm2,OUTPUT);
        pinMode(13,OUTPUT);
        pinMode(12,OUTPUT);

        digitalWrite(13, led);
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

        char msg[50];
        Serial.println(START_CHAR);
        sprintf(msg, "%d,%lu,%d,%d,%d",joint,time,ang,vel,cur);
        Serial.println(msg);

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

void read_msg(){

        char dir1_buff[2], dir2_buff[2], on1_buff[2], on2_buff[2];
        char pwm1_buff[4], pwm2_buff[4];
        char chkbt;
        int on1, on2, dir1, dir2, pwm1, pwm2;
        int data_arr[6];

        // String terminators for later use with atoi()
        on1_buff[1] = '\0';
        on2_buff[1] = '\0';
        pwm1_buff[3] = '\0';
        pwm2_buff[3] = '\0';
        dir1_buff[1] = '\0';
        dir2_buff[1] = '\0';

        // Wait for start char..
        chkbt = Serial.read();
        while(chkbt != '$') {
                chkbt = Serial.read();
                digitalWrite(13,1);
        };
        
        digitalWrite(13,0);

        // Wait for whole message to be available
        while(Serial.available() < MSG_LEN) {
            digitalWrite(12,1);
                //Serial.println("waiting for rest of msg");
                //delay(500);
        };
        digitalWrite(12,0);

        // Read and convert all the shit!
        on1_buff[0] = Serial.read();
        dir1_buff[0] = Serial.read();
        
        for (int i = 0; i<3; i++){
                pwm1_buff[i] = Serial.read();
        }
        
        on1 = atoi(on1_buff);
        dir1 = atoi(dir1_buff);
        pwm1 = atoi(pwm1_buff);

        on2_buff[0] = Serial.read();
        dir2_buff[0] = Serial.read();
        
        for (int i = 0; i<3; i++){
                pwm2_buff[i] = Serial.read();
        }

        on2 = atoi(on2_buff);
        dir2 = atoi(dir2_buff);
        pwm2 = atoi(pwm2_buff);


        digitalWrite(pin_on1, on1);
        digitalWrite(pin_dir1, dir1);
        analogWrite(pin_pwm1, pwm1);
        digitalWrite(pin_on2, on2);
        digitalWrite(pin_dir2, dir2);
        analogWrite(pin_pwm2, pwm2);
        
}



void loop(){

	int starttime;
	starttime = int(millis());

  read_msg();
	measure();
  // delay(500);
	
	//delay(starttime+SAMPLE_T_MS-int(millis()));

//    digitalWrite(pin_on1,LOW);
//    digitalWrite(pin_on2,LOW);

}
