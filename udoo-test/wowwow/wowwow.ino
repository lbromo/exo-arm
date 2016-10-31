#include "FreeRTOS.h"
#include "task.h"

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
