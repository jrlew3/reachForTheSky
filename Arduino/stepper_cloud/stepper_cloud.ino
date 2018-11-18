/* 
 *  stepper_cloud: cloud moves with fixed speed to position that is determined by the raspi 
 *  Buggy when the change in position is too small, stepper motor has trouble with
 *  slow speeds. Assumes input is sent from the arduino at a fixed rate.  
 *  
 *  (stepper_cloud2 is the newer version)
 */

#include <AccelStepper.h>

AccelStepper stepper1(AccelStepper::DRIVER, 2, 3); 

int x = 0; // the target position 
int pos = 0;
int t = 5; // the amount of time inbetween raspi input

void setup(void)
{
  stepper1.setMaxSpeed(1000);
  stepper1.setAcceleration(500);
  Serial.begin(9600);
} 


void loop(void)
{
  
    if(Serial.available()) {
      x = Serial.read(); 
      x = map(x, 0, 255, 0, 3000); //map position, length of rail = 3000
      //int diff = x - pos; 
      //pos = x; 

      stepper1.moveTo(x);
      stepper1.setSpeed((x - stepper1.currentPosition())/5); //approximate speed 
      Serial.println(x);
    }
    
    stepper1.runSpeed();  
}
