
#include "libraries/FreeRTOSv9.0.0/FreeRTOS/Source/include/FreeRTOS.h"
#include "libraries/FreeRTOSv9.0.0/FreeRTOS/Source/include/task.h"
/*
#include "libraries/FreeRTOSv9.0.0/FreeRTOS/Source/include/semphr.h"
#include "libraries/FreeRTOSv9.0.0/FreeRTOS/Source/include/queue.h"
#include "libraries/FreeRTOSv9.0.0/FreeRTOS/Source/include/timers.h"
#include "libraries/FreeRTOSv9.0.0/FreeRTOS/Source/include/event_groups.h"
#include "libraries/FreeRTOSv9.0.0/FreeRTOS/Source/include/mpu_prototypes.h"
*/

void vBlinkTask(void *pvParameters){
  bool flag = false;
  if(xTaskCreate){}
  while(true){
    digitalWrite(13, flag);
    flag = !flag;
    vTaskDelay(500/portTICK_RATE_MS);
  }
}

void setup() {
  pinMode(13, OUTPUT);
  
  // put your setup code here, to run once:
  xTaskCreate(vBlinkTask, "Blinker", 1000, NULL, 0, NULL);
  vTaskStartScheduler();
}

void loop() {
  // put your main code here, to run repeatedly:

}
