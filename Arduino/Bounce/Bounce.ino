/* 
 *  Bounce: the stepper motor will move back and forth
 *  with a set acceleration (for some reason doesn't 
 *  work with a fixed speed)
 */



#include <AccelStepper.h>

AccelStepper stepper(AccelStepper::DRIVER, 2, 3); // Defaults to AccelStepper::FULL4WIRE (4 pins) on 2, 3, 4, 5

void setup()
{  
  // Change these to suit your stepper if you want
  stepper.setAcceleration(20);
  stepper.setMaxSpeed(1000);
  stepper.moveTo(500);
  //stepper.setSpeed(100);
}
void loop()
{
    // If at the end of travel go to the other end
    if (stepper.distanceToGo() == 0) { 
      stepper.moveTo(-stepper.currentPosition());
      //stepper.setSpeed(500);
    }
    stepper.run();
    //stepper.runSpeed();
}
