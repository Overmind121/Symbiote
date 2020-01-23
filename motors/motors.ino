#include <AFMotor.h>
//Forward is char character:102
//Backward is char character: 98
//Left is char character: 108
//right is char character: 114
AF_DCMotor motorL(3, MOTOR34_64KHZ);
AF_DCMotor motorR(4, MOTOR34_64KHZ);

void setup(){
  Serial.begin(9600);
  motorL.setSpeed(255);
  motorR.setSpeed(255);
}

void loop(){
  if(Serial.read() == 102){
    motorL.run(FORWARD);
    motorR.run(FORWARD);
    delay(5000);
    motorL.run(RELEASE);
    motorR.run(RELEASE);
    delay(1000);
  } 
}
