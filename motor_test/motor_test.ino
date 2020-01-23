#include <AFMotor.h>


AF_DCMotor motorL(3, MOTOR34_64KHZ);
AF_DCMotor motorR(4, MOTOR34_64KHZ);
boolean stop = false;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Serial.println("Motor test!");
  motorL.setSpeed(255);
  motorR.setSpeed(255);
}

void loop() {
  // put your main code here, to run repeatedly:

  if(stop == true){
    motorL.run(RELEASE);
    motorR.run(RELEASE);
    delay(1000);
  }
  else{
    motorL.run(FORWARD);
    motorR.run(FORWARD);
    delay(10000);
    stop = true;
  }
 
  
}
