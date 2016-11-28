bool led;
void setup() {
  pinMode(13, OUTPUT);
  Serial.begin(115200);
  led = 0;
  digitalWrite(13,led);
}

void loop() {
if (Serial.available() > 0){
    Serial.print((char)Serial.read()),    
    digitalWrite(13, led);
    led = !led;
}    
}

