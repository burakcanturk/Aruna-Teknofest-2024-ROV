#define rs485 Serial2

void setup() {
  Serial.begin(9600);
  rs485.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    rs485.write(Serial.read());
  }
  if (rs485.available() > 0) {
    Serial.write(rs485.read());
  }
}
