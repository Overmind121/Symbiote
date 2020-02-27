#include <AFMotor.h>
#include <AFMotor.h>
//Forward is char character:102
//Backward is char character: 98
//Left is char character: 108
//right is char character: 114
//stop is char characterL 83
AF_DCMotor motorL(1, MOTOR34_64KHZ);
AF_DCMotor motorR(4, MOTOR34_64KHZ);

void setup(){
  Serial.begin(9600);
  motorL.setSpeed(255);
  motorR.setSpeed(255);
}

void loop(){
  byte comm = Serial.read();
  if (comm < 254){
    Serial.println(comm);
  }
  Serial.println(comm);
  if(comm == 102){ //forward
    motorL.run(FORWARD);
    motorR.run(FORWARD);

  }
  if(comm == 98){ //backward
    motorL.run(BACKWARD);
    motorR.run(BACKWARD);

  }
  if(comm == 108){ //Left
    motorL.run(FORWARD);
    motorR.run(RELEASE);
  }
  
  if(comm == 114){ //right
    motorL.run(RELEASE);
    motorR.run(FORWARD);
  } 
  
  if(comm == 115){ //stop
    motorL.run(RELEASE);
    motorR.run(RELEASE);
  }
  
 }
