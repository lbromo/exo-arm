#include <stdio.h>
#include "AxoArmUtils.h"
#include "hal.h"

#include <imx6sx_sdb_m4.h>
#include <hwtimer_epit.h>

using namespace AxoArm;

Vector meas(N_STATES);
Vector ref(N_STATES);
Vector e(N_STATES_W_INTEGRATOR);

Matrix K(2, N_STATES_W_INTEGRATOR);

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

void setup(){
  /*
   * If we are running on an Arduino are we using a external 3.3v analog reference
   * On the Udoo (with an M4) are the ADC 12 bit
   */
  #if not defined(__arm__)
  analogReference(EXTERNAL);
  #elif defined (__arm__)
  analogReadResolution(12);
  #endif /* __arm__ */

  Serial0.begin(230400);

  /* Setup shoulder pins */
  pinMode(pin_on_shoulder, OUTPUT);
  pinMode(pin_dir_shoulder, OUTPUT);
  pinMode(pin_pwm_shoulder, OUTPUT);

  /* Setup elbow pins */
  pinMode(pin_on_elbow, OUTPUT);
  pinMode(pin_dir_elbow, OUTPUT);
  pinMode(pin_pwm_elbow, OUTPUT);

  /* For blinky :-) */
  pinMode(pin_led, OUTPUT);

  /* The drivers gets angry if there isn't a signal, so we put on a little bit */
  analogWrite(pin_pwm_shoulder, 25);
  analogWrite(pin_pwm_elbow, 25);

  /* CONTROLLER */
  int ki = 216;
  int kp = 108;
  int kd = 18;

  K[0][0] = ki; // shoulder Ki;
  K[0][2] = kp; // Shoulder Kp;
  K[0][4] = kd; // Shoulder Kd;
  K[1][1] = ki; // shoulder Ki;
  K[1][3] = kp; // Shoulder Kp;
  K[1][5] = kd; // Shoulder Kd;

  /*
   * We use small intterups as pseudo tasks
   * Timer1 is setting a flag to run the interface and pulse function
   * Timer2 it setting a falg to run the controller function
   */
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

  if(cnt >= 500000/SAMPLE_T_US)
  {
    led = !led;
    digitalWrite(pin_led, led);
    cnt = 0;
  }
}

/*
** Function that gets a set of measurements and transmits them over the Serial0 port.
**
** Run everytime the RDY_CHAR is received.
*/
void measure() {
  unsigned long time;
  char msg[100];
  time = millis();

  /* Map values in easier to read variables */
  int iepos, spos, svel, scur;
  int ispos, epos, evel, ecur;

  ispos = (int) (100 * e[0]);
  iepos = (int) (100 * e[1]);
  spos = (int) (100 * meas[0]);
  spos = (int) (100 * meas[1]);
  svel = (int) (100 * meas[2]);
  svel = (int) (100 * meas[3]);
  scur = (int) (100 * getCur(SHOULDER));
  ecur = (int) (100 * getCur(ELBOW));

  sprintf(msg, "%c,%lu,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d%d,%d", START_CHAR, time, SHOULDER, (int)(100*ref[2]), ispos, spos, svel, scur, ELBOW, (int)(100*ref[3]), iepos, epos, evel, ecur);
  Serial0.println(msg);
}

/*
** Receives, parses and sets the new reference vector in angle and angular velocity domain.
**
** ref = [0 0 theta_s theta_e thetadot_s thetadot_e]
*/
void getRef() {
  char *pos1_buff, *pos2_buff, *vel1_buff, *vel2_buff;
  char buff[50];

  Serial0.readBytesUntil(END_CHAR, buff, 50);

  pos1_buff = strtok(buff, ",");
  pos2_buff = strtok(NULL, ",");
  vel1_buff = strtok(NULL, ",");
  vel2_buff = strtok(NULL, ",");

  ref[2] = 0.01 * atoi(pos1_buff);
  ref[3] = 0.01 * atoi(pos2_buff);
  ref[4] = 0.01 * atoi(vel1_buff);
  ref[5] = 0.01 * atoi(vel2_buff);
}

/*
** Parses input current into something than can be applied in HW
**
** Called from ctrl()
*/
void applyControl(const Vector& u) {
  // Create direction signal
  dir_shoulder    = getDir(u[SHOULDER]);
  dir_elbow       = getDir(u[ELBOW]);

  // Convert current to PWM
  pwm_shoulder    = cur2pwm(SHOULDER, u[SHOULDER]);
  pwm_elbow       = cur2pwm(ELBOW, u[ELBOW]);

  /* Set direction */
  digitalWrite(pin_dir_shoulder, dir_shoulder);
  digitalWrite(pin_dir_elbow, dir_elbow);

  /* Set PWM signal */
  analogWrite(pin_pwm_shoulder, pwm_shoulder);
  analogWrite(pin_pwm_elbow, pwm_elbow);
}

/*
 * Small ISR for Timer 1
 */
void t_interface(void *param){
  do_interface = true;
  pulse();
}

/*
 * Small ISR for Timer 2
 */
void t_ctrl(void *param){
  do_control = true;
}

/*
 * Main controller task
 * Gets measurements and applies control
 *
 * Is run whenever do_control is true
 * states = [i_theta_s i_theta_e theta_s theta_e thetadot_s thetadot_e]
 */
void ctrl() {
  /*
  auto s_pos = getPos(SHOULDER);
  auto e_pos = getPos(ELBOW);

  meas[0] += -1 * SAMPLE_T_S * s_pos; // Flipped sign as we later do ref - meas 
  meas[1] += -1 * SAMPLE_T_S * e_pos; // Flipped sign as we later do ref - meas 
  meas[2] = s_pos;
  meas[3] = e_pos;
  meas[4] = getVel(SHOULDER);
  meas[5] = getVel(ELBOW);
  */

  meas[0] = getPos(SHOULDER);
  meas[1] = getPos(ELBOW);
  meas[2] = getVel(SHOULDER);
  meas[3] = getVel(ELBOW);

  e[0] += SAMPLE_T_S * (ref[0]-meas[0]); 
  e[1] += SAMPLE_T_S * (ref[1]-meas[1]); 
  e[2] = ref[0] - meas[0];  
  e[3] = ref[1] - meas[1];
  e[4] = ref[2] - meas[2];
  e[5] = ref[3] - meas[3];


  // Run cuntroller
  auto u = controller(meas, e, K);

  // Convert torque to current
  u[0] /= Nkt0;
  u[1] /= Nkt1;

  // Apply current
  applyControl(u);
}

/*
 * The interface task revices and performs commands based on inputs from the serial interface
 */
void interface(){
  /* Set "enable" signal */
  digitalWrite(pin_on_shoulder, on);
  digitalWrite(pin_on_elbow, on);

  /* Input buffer - commands headers are 1 byte */
  char inByte;

  // Get command
  if (Serial0.available())
  {
    inByte = Serial0.read();
  } else {
    inByte = '\0';
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

void loop(){
  if (do_control){
    ctrl();
    do_control = false;
  }
  if (do_interface){
    interface();
    do_interface = false;
  }
}
