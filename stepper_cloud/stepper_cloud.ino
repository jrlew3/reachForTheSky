// StepperSweep - move a stepper motor at different rates
//
// Copyright (c) 2016, Garth Zeglin.  All rights reserved. Licensed under the
// terms of the BSD 3-clause license as included in LICENSE.
//
// This program assumes that:
//
//  1. A A4988 stepper motor driver is connected to pins 2 and 3.
//  2. A control potentiometer can vary the voltage on A0.
//  3. The serial console on the Arduino IDE is set to 9600 baud communications speed.

// ================================================================================
// Define constant values and global variables.

// Define the pin numbers on which the outputs are generated.
#define DIR_PIN 2     // The direction pin controls the direction of stepper motor rotation.
#define STEP_PIN 3    // Each pulse on the STEP pin moves the stepper motor one angular unit.
#define ENABLE_PIN 4  // Optional control of the driver power.

float default_speed = 200.0; 
float pos = 0; 

void setup(void)
{
  pinMode(DIR_PIN, OUTPUT); 
  pinMode(STEP_PIN, OUTPUT);
  pinMode(ENABLE_PIN, OUTPUT);

  // Drive the /ENABLE pin low to keep the motor always energized.
  digitalWrite(ENABLE_PIN, LOW);
  
  // Initialize the serial UART at 9600 bits per second.
  Serial.begin(9600);
} 
/****************************************************************/
/// Rotate the stepper motor a specified distance at constant speed.  It does
/// not return until the motion is complete, e.g. it 'blocks' for the duration.
///
/// \param steps angular distance to move; the sign determines the direction,
///     but the precise angle depends upon the driver microstepping
///    configuration and type of motor.
///
/// \param speed speed in steps/second

void rotate_stepper(int steps, float speed)
{
  // Configure the direction pin on the stepper motor driver based on the sign
  // of the displacement.
  int dir = (steps > 0)? HIGH:LOW;
  digitalWrite(DIR_PIN, dir); 

  // Find the positive number of steps pulses to emit.
  int pulses = abs(steps);

  // Compute a delay time in microseconds controlling the duration of each half
  // of the step cycle.
  //  microseconds/half-step = (1000000 microseconds/second) * (1 step/2 half-steps) / (steps/second)
  unsigned long wait_time = 500000/speed;

  // The delayMicroseconds() function cannot wait more than 16.383ms, so the
  // total delay is separated into millisecond and microsecond components.  This
  // increases the range of speeds this function can handle.
  unsigned int msec = wait_time / 1000;
  unsigned int usec = wait_time - (1000*msec);

  // Print a status message to the console.
  Serial.print("Beginning rotation of ");
  Serial.print(steps);
  Serial.print(" steps with delay interval of ");
  Serial.print(msec);
  Serial.print(" milliseconds, ");
  Serial.print(usec);
  Serial.print(" microseconds.\n");
  
  // Loop for the given number of step cycles.  The driver will change outputs
  // on the rising edge of the step signal so short pulses would work fine, but
  // this produces a square wave for easier visualization on a scope.
  for(int i = 0; i < pulses; i++) {
    digitalWrite(STEP_PIN, HIGH);
    if (msec > 0) delay(msec);
    if (usec > 0) delayMicroseconds(usec);

    digitalWrite(STEP_PIN, LOW); 
    if (msec > 0) delay(msec);
    if (usec > 0) delayMicroseconds(usec);
  }
}


void move_x(float x, float speed){
  int steps = (pos - x); 
  rotate_stepper(steps, speed);
  pos = x; 
}

void loop(void)
{
  // Now demonstrate that the stepper can freely rotate.
  rotate_stepper(1000, default_speed);
  rotate_stepper(-1000, default_speed);
 
}

/****************************************************************/
