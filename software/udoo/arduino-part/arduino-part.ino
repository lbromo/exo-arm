#include <stdio.h>
#include "AxoArmUtils.h"
#include "hal.h"

#include <imx6sx_sdb_m4.h>
#include <hwtimer_epit.h>

using namespace AxoArm;

Vector meas(N_STATES);
Vector ref(N_STATES);

Matrix K(2, N_STATES);

bool on = false;
bool do_control = false;
bool do_interface = false;

int dir_shoulder, dir_elbow;
int pwm_shoulder, pwm_elbow;

void ctrl();  
void interface(); 

// Periodic tasks
void t_ctrl(void *param);
void t_interface(void *param);

HWTIMER timer1, timer2;

int cnt = 0;
bool led = false;

void setup() {

  Serial0.begin(230400);

  #if not defined(__arm__)
    analogReference(EXTERNAL);
  #endif

  pinMode(pin_on_shoulder, OUTPUT);
  pinMode(pin_dir_shoulder, OUTPUT);
  pinMode(pin_pwm_shoulder, OUTPUT);

  pinMode(pin_on_elbow, OUTPUT);
  pinMode(pin_dir_elbow, OUTPUT);
  pinMode(pin_pwm_elbow, OUTPUT);

  pinMode(13,OUTPUT);

  #ifdef __arm__
    analogReadResolution(12);
  #endif

  analogWrite(pin_pwm_shoulder, 25);
  analogWrite(pin_pwm_elbow, 25);

  K[0][0] = 0;//100;
  K[0][2] = 20;
  K[1][1] = 0;//100;
  K[1][3] = 20;

  // K[0][0] = 12;
  // K[0][2] = 3;
  // K[1][1] = 12;
  // K[1][3] = 3;


  hwtimer_init(&timer2, &BSP_HWTIMER2_DEV, BSP_HWTIMER2_ID, 2);
  hwtimer_set_period(&timer2, BSP_HWTIMER2_SOURCE_CLK, SAMPLE_T_US);
  hwtimer_callback_reg(&timer2, t_ctrl, 0);
  hwtimer_start(&timer2);

  hwtimer_init(&timer1, &BSP_HWTIMER1_DEV, BSP_HWTIMER1_ID, 1);
  hwtimer_set_period(&timer1, BSP_HWTIMER1_SOURCE_CLK, SAMPLE_T_US);
  hwtimer_callback_reg(&timer1, t_interface, 0);
  hwtimer_start(&timer1);

}

/*
** Pulse function that blinks an LED to show that stuff is running
*/
void pulse() {

  cnt++;
  if(cnt > 500000/SAMPLE_T_US)
  {
    led = !led;
    digitalWrite(13, led);
    cnt = 0;
  }
}

/*
** Function that gets a set of measurements and thansmits them over the Serial0 port.
**
** Run everytime the RDY_CHAR is received.
*/
void measure() {

  unsigned long time;
  char msg[100];
  time = millis();

  int spos,svel,scur,epos,evel,ecur;

  spos = (int) (100 * getPos(SHOULDER));
  svel = (int) (100 * getVel(SHOULDER));
  scur = (int) (100 * getCur(SHOULDER));
  epos = (int) (100 * getPos(ELBOW));
  evel = (int) (100 * getVel(ELBOW));
  ecur = (int) (100 * getCur(ELBOW));

  sprintf(msg, "%c,%lu,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d", START_CHAR, time, SHOULDER, (int)(100*ref[0]), spos, svel, scur, ELBOW, (int)(100*ref[1]), epos, evel, ecur);
  Serial0.println(msg);

}

/*
** Receives, parses and sets the new reference vector in angle and angular velocity domain.
**
** ref = [theta_s theta_e thetadot_s thetadot_e]
*/
void getRef() {

  char *pos1_buff, *pos2_buff, *vel1_buff, *vel2_buff;
  char buff[50];
  
  Serial0.readBytesUntil(END_CHAR, buff, 50);
  
  pos1_buff = strtok(buff, ",");
  pos2_buff = strtok(NULL, ",");
  vel1_buff = strtok(NULL, ",");
  vel2_buff = strtok(NULL, ",");

  ref[0] = 0.01 * atoi(pos1_buff);
  ref[1] = 0.01 * atoi(pos2_buff);
  ref[2] = 0.01 * atoi(vel1_buff);
  ref[3] = 0.01 * atoi(vel2_buff);

}

/*
** Parses input current into something than can be applied in HW
** 
** Called from ctrl()
*/
void applyControl(Vector u) {

  // Create direction signal
  dir_shoulder    = getDir(u[SHOULDER]);
  dir_elbow       = getDir(u[ELBOW]);

  // Convert current to PWM
  pwm_shoulder    = cur2pwm(SHOULDER, u[SHOULDER]);
  pwm_elbow       = cur2pwm(ELBOW, u[ELBOW]);

  digitalWrite(pin_dir_shoulder, dir_shoulder);
  digitalWrite(pin_dir_elbow, dir_elbow);

  analogWrite(pin_pwm_shoulder, pwm_shoulder);
  analogWrite(pin_pwm_elbow, pwm_elbow);

}

void t_interface(void *param){

  do_interface = true;
  pulse();

}

void t_ctrl(void *param){

  do_control = true;
  
}

/*
** Main controller task
** Gets measurements and applies control
**
** Is run with a period of SAMPLE_T_US on hwtimer2
*/
void ctrl(void *param) {

  // Do measurements
  meas[0] = getPos(SHOULDER);
  meas[1] = getPos(ELBOW);
  meas[2] = getVel(SHOULDER);
  meas[3] = getVel(ELBOW);

  // Run cuntroller
  auto u = controller(meas, ref, K);

  // auto u_tmp = K * (ref - meas);

  // Convert torque to current
  u[0] /= Nkt0;
  u[1] /= Nkt1;

  // Apply current
  applyControl(u);

}


void interface(void *param){

  digitalWrite(pin_on_shoulder, on);
  digitalWrite(pin_on_elbow, on);

  char inByte;

  // Get command
  if (Serial0.available())
  {
    inByte = Serial0.read();
  } else {
    inByte = '\0';
    return;
  }

  // Figure out what to do!
  switch(inByte) {
    case MEAS_CHAR:
      measure();
      break;
    case REF_CHAR:
      getRef();
      on = true;
      break;
    case STOP_CHAR:
      on = false;
      break;
    default:
      break;
  }

}


void loop() {

  if (do_control){
    ctrl(NULL);
    do_control = false;
  }
  if (do_interface){
    interface(NULL);
    do_interface = false;
  }  

}
