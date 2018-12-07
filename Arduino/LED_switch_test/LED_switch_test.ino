/*
 * 16-223: Reach for the Sky by Jen Kwang and Jessica Lew
 * Use this code ONLY to debug circuit/mechanism or when altering Rpi code.  
 * 
 * Given that an LED strip, two switches, a stepper motor, and a flex sensor
 * are connected, the stepper motor should move back and forth without
 * delays.  Using Serial Monitor, you can observe values of the flex sensor.
 * 
 * Note that the parts of this code relating to the flex sensor are identical to
 * the code integrated in lightning_squish_feature.ino
 */


//change following two var depending on how quickly program runs
const int flex_count_thresh = 5;
const int led_count_thresh = 10;

unsigned long time;

const int DIR_PIN = 2;     // The direction pin controls the direction of stepper motor rotation.
const int STEP_PIN = 3;    // Each pulse on the STEP pin moves the stepper motor one angular unit.
// #define ENABLE_PIN 4  // Optional control of the driver power.
int pos = 0; //motor func use
int n =0; //motor func use

const int SWITCH_PIN = 10;
const int FLEX_PIN = A1;
const int R_PIN = 9;
const int G_PIN = 5;
const int B_PIN = 6;

int value; //cur value of flex sensor
int sec;
int flex_init = 0;
int count = 0; //loop counter used to calibrate flex sensor/time the lightning

void setup() {
  Serial.begin(9600);

  //motor setup
  pinMode(DIR_PIN, OUTPUT); 
  pinMode(STEP_PIN, OUTPUT);
  //pinMode(ENABLE_PIN, OUTPUT);
  //digitalWrite(ENABLE_PIN, LOW);


  pinMode(SWITCH_PIN, INPUT);
  pinMode(FLEX_PIN, INPUT);
  pinMode(R_PIN, OUTPUT);
  pinMode(G_PIN, OUTPUT);
  pinMode(B_PIN, OUTPUT);
  
  // Start off with the LED off.
 // setColor(0,0,0);


}

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

void setColor(int red, int green, int blue)
{
  analogWrite(R_PIN, red);
  analogWrite(G_PIN, green);
  analogWrite(B_PIN, blue);  
}

void move(int x){
  int diff = x - pos; 
  rotate_stepper(diff, 400);
  pos = x;
     
}

void loop() {
  if (flex_init == 0)
  {
    delay(10);
   flex_init = analogRead(FLEX_PIN); 
  }

  Serial.print("  Time: ");
  time = millis();
  Serial.println(time);

  Serial.print("  Sec var: ");
  
  sec = time / 1000;
  Serial.println(sec);
  
  value = analogRead(FLEX_PIN); 
  Serial.print("          flex value:  ");
  Serial.println(value);  
  Serial.print("FLEX INIT:    ");
  Serial.print(flex_init);
  Serial.print("    ");

  // if squished, turn on LED
  if (flex_init - 10 > value || flex_init + 10 < value)
  {
    Serial.print("~~~~~~~~~~~~~~~~flex init value: ");
    Serial.print(flex_init);
    Serial.print("_______________flex cur value: ");
    Serial.print(value);
    count = count + 1;

    //turn on led color depending on count
    if (count % 2 == 0){
      setColor(80, 0, 80);  // purple
   
    }
    else if (count % 2 != 0){
      setColor(0, 255, 255);  // aqua
     
    }

    // if flex sensor permanently bent out of shape, reset its neutral state value.
    if (count >= flex_count_thresh)
    {
      flex_init = value;
      count = 0;
    }

  }

  // if not squished, update the flex neutral state value.
  else
  {
    flex_init = value;
  }
  
  // if touching edge of box (switch pushed), value is 0, and 1 otherwise
  int is_edge = digitalRead(SWITCH_PIN);
  
  Serial.print("\n Switch value:  ");
  Serial.print(is_edge);

  //testing the motor
  move(100);
  move(0);

}
