/* 
 *  stepper_cloud2: cloud moves with fixed acceleration to either side of the rail. 
 *  Changes direction when input receiving a "1" from the raspberry pi. Doesn't 
 *  work with fixed speed. (
 *  
 */
#include <AccelStepper.h>
AccelStepper stepper1(AccelStepper::DRIVER, 2, 3); 

int x; // the integer read from the raspberry pi 
int len = 9000; // the length of the rail 
int target_position = len; // set the initial target position to the other side of the rail 
bool cont = false; // don't start moving yet 

void setup(void)
{
  Serial.begin(9600);
  stepper1.setMaxSpeed(100); // max speed
  stepper1.setAcceleration(100); // acceleration 
  
  while(!cont) { // don't start moving until signal received from raspi
    if(Serial.available()) {
      if(Serial.read() == 0)  cont = true; 
    }
  }
  
  stepper1.moveTo(target_position); // start moving to opposite side of rail 
} 


void loop(void)
{ 
    if(Serial.available()) { 
      x = Serial.read(); 
      if(x & 1) { // if input is equal to 1, then change position 
        if (target_position == 0) target_position = len;
        else target_position = 0;
        stepper1.moveTo(target_position);
      }
   
      Serial.println(x); // send info back to raspi
    }
    
    stepper1.run(); // run to target posiiton with set acceleration
}
