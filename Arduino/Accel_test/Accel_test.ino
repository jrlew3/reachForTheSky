#include <AccelStepper.h>
AccelStepper stepper1(AccelStepper::FULL4WIRE, 2, 3, 4, 5); 
int default_speed = 500; 
void setup() {
  // put your setup code here, to run once:
  stepper1.setMaxSpeed(600.0);
  stepper1.setAcceleration(200.0);
  Serial.begin(9600); 
  stepper1.setCurrentPosition(0);
  stepper1.moveTo(500); 
}

void loop() {
  // put your main code here, to run repeatedly:
    if(stepper1.distanceToGo() <= 0){
      stepper1.moveTo(-stepper1.currentPosition());
      Serial.println("change direction");
    }
    stepper1.run();  
    Serial.println(stepper1.currentPosition());
}
