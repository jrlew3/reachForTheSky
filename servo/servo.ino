#include <Servo.h>
Servo myServo;
const int servoPin = 9;
float n = 0; 
float pos;
 
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  myServo.attach(9);
  myServo.write(0);
}

void loop() {

    if(Serial.available()) {
      n = Serial.parseInt(); 
      pos = map(n, 0, 1024, 0, 180) ; 
      Serial.println(pos);
      myServo.write(pos);
    }
    delay(50);

  
}

void turn(int n) {
    myServo.write(n);  
}
