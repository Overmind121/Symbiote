#include <AFMotor.h>
//Forward is char character:102
//Backward is char character: 98
//Left is char character: 108
//right is char character: 114
//stop is char characterL 83
AF_DCMotor motorL(3, MOTOR34_64KHZ);
AF_DCMotor motorR(4, MOTOR34_64KHZ);

void setup(){
  Serial.begin(9600);
  motorL.setSpeed(255);
  motorR.setSpeed(255);
}

void loop(){
  if(Serial.read() == 102){ //forward
    motorL.run(FORWARD);
    motorR.run(FORWARD);

  }
  if(Serial.read() == 98){ //backward
    motorL.run(BACKWARD);
    motorR.run(BACKWARD);

  }
  if(Serial.read() == 108){ //Left
    motorL.run(FORWARD);
    motorR.run(RELEASE);
  }
  if(Serial.read() == 114){ //right
    motorL.run(RELEASE);
    motorR.run(FORWARD);
  } 
  if(Serial.read() == 83){
    motorL.run(RELEASE);
    motorR.run(RELEASE);
  }
  
 }
