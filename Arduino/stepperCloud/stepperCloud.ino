/* 
 *  stepperCloud - Changes the direction of the stepper motor according to the 
 *                 direction sent by the Raspberry Pi. The stepper motor  
 *                 will continue moving in that direction until it reaches
 *                 the end of either rail or a change in direction is recorded
 *                 by the Raspberry Pi. Sends the current position of the 
 *                 stepper motor every iteration of the loop.  
 */
 
#include <AccelStepper.h>
AccelStepper stepper1(AccelStepper::FULL2WIRE, 2, 3); 

const int len = 16000; // the length of the rail 
const int initialSpeed = 800;  
const int displayWidth = 960; // width of monitor

int x; // the integer read from the raspberry pi 
int targetPos = 0; 
int currPos = 0; 
int currSpeed = 0;

unsigned long prevMillis = 0; 
unsigned long delta = 1000; // time between sending updated position


void setup(void)
{ 
  Serial.begin(9600);
  stepper1.setCurrentPosition(0);
  stepper1.setMaxSpeed(1000);

} 

void moveRight() {
  targetPos = len;  
  currSpeed = initialSpeed;
}

void moveLeft() {
  targetPos = 0;
  currSpeed = -initialSpeed;
}

void stopMoving() {
  targetPos = stepper1.currentPosition();
  currSpeed = 0;
}

// Ensure current position is within bounds
void fixPositions() {
  int pos = stepper1.currentPosition(); 
  if(pos > len)
    stepper1.setCurrentPosition(len);
  else if(pos < 0)
    stepper1.setCurrentPosition(0);
}


// Change direction of stepper motor according to direction send by raspi
void changeDirection() {
  fixPositions(); 
  
  x = Serial.read(); 
  if(x == 1) 
    moveRight(); 
  else if (x == 2)
    moveLeft();
  else if(x == 0)
    stopMoving();
  else
    Serial.println(-1);

   stepper1.moveTo(targetPos); 
   stepper1.setSpeed(currSpeed); 
}


void loop(void)
{     
    if(Serial.available()) changeDirection(); 
    stepper1.runSpeed(); // run to target positon with a set speed

   
    if(millis() - prevMillis > delta) { 
      currPos = stepper1.currentPosition(); 
      currPos = map(currPos, 0, len, 0, displayWidth); 
      Serial.println(currPos);
      prevMillis = millis(); 
    }
  
}
