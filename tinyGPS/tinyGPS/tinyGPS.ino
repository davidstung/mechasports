
void setup() {
  Serial.begin(57600);  
}

void loop() {
  if (Serial.available()) {
    Serial.print(Serial.read(), 0);
  }
}
