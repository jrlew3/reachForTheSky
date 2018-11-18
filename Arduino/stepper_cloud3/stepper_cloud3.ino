/* 
 *  stepper_cloud3: newer vision of stepper_cloud2 where the stepper motor attempts to move 
 *  at a constant speed (has not been tested) 
 *  
 */
 
#include <AccelStepper.h>
AccelStepper stepper1(AccelStepper::DRIVER, 2, 3); 

int x; // the integer read from the raspberry pi 
int len = 9000; // the length of the rail 
int target_position = len; // set the initial target position to the other side of the rail 
bool cont = false; // don't start moving yet 
int curr_speed = 100;  

void setup(void)
{
  Serial.begin(9600);
  
  while(!cont) { // don't start moving until signal received from raspi
    if(Serial.available()) {
      if(Serial.read() == 0)  cont = true; 
    }
  }

  stepper1.moveTo(target_position); // start moving to opposite side of rail 
  stepper1.setSpeed(curr_speed); 
} 


void loop(void)
{ 
    if(Serial.available()) { 
      x = Serial.read(); 
      if(x & 1) { // if input is equal to 1, then change position 
        if (target_position == 0) target_position = len;
        else target_position = 0;
        
        stepper1.moveTo(target_position);
        curr_speed = -curr_speed;
        stepper1.setSpeed(-curr_speed); // the speed must also indicates direction 
      
        Serial.println(stepper1.currentPosition()); // send info back to raspi
      }
    }
    
    stepper1.runSpeed(); // run to target posiiton with a set speed
}
