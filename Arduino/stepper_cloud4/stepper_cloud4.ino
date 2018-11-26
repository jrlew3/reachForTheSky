/* 
 *  stepper_cloud4: newer vision of stepper_cloud3 where the stepper motor sends back its
 *                  position to the raspi. If the stepper motor's position is below zero 
 *                  or above the length of the rail, then that position is set as either
 *                  the new max or the new min. (I think adding switches to the ends
 *                  of the rail and recalibrating the speed/length parameters will fix this
 *                  problem)
 *  
 */
 
#include <AccelStepper.h>
AccelStepper stepper1(AccelStepper::DRIVER, 2, 3); 

const int len = 3000; // the length of the rail 
const int initial_speed = 300;  
const int display_width = 1280; // width of monitor

int x; // the integer read from the raspberry pi 
int target_position = len; // set the initial target position to the other side of the rail 
bool cont = false; // don't start moving yet 

int curr_pos = 0; 
int curr_speed = initial_speed;



void setup(void)
{
  Serial.begin(9600);
  stepper1.setCurrentPosition(0);
  stepper1.setMaxSpeed(1000);
  stepper1.moveTo(len);
  stepper1.setSpeed(curr_speed); 
  
  while(!cont) { // don't start moving until signal received from raspi
    if(Serial.available()) {
      if(Serial.read() == 0)  {
        cont = true;
        Serial.println(stepper1.currentPosition()); 
      }
    }
  }
} 


void loop(void)
{ 
    if(Serial.available()) { 
      x = Serial.read(); 
      if((x & 1) == 1) { // if input is equal to 1, then change position 
        


        //send results positon to raspi
        curr_pos = stepper1.currentPosition(); 
        if(curr_pos > len) {
          curr_pos = len;
          stepper1.setCurrentPosition(len); 
          target_position = 0;
          curr_speed = -initial_speed;
          Serial.println(-1); 
        } else if(curr_pos < 0) {
          curr_pos = 0;
          stepper1.setCurrentPosition(0);
          target_position = len;
          curr_speed = initial_speed;
          Serial.println(-2);
        } else {
          
          // set target position
          if (target_position == 0) target_position = len;
          else if(target_position == len) target_position = 0;
          else {
            Serial.println(target_position);
            Serial.println("target position error");
          }
          
          //set speed
          if(target_position == 0) curr_speed = -initial_speed;
          else if(target_position == len) curr_speed = initial_speed;
 
        }

        // move
        stepper1.moveTo(target_position);
        stepper1.setSpeed(curr_speed); // the speed must also indicates direction 
        curr_pos = map(curr_pos, 0, len, 0, 1280);
        Serial.println(curr_pos); // send info back to raspi
      
      }
    }
    
    stepper1.runSpeed(); // run to target posiiton with a set speed
}
