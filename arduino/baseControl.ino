
//void initBaseControl() {
//  Serial.println("Init base controler");
//  mcp.pinMode(stopBtnBaseLeft, INPUT);
//  mcp.pinMode(stopBtnBaseRight, INPUT);
//  
//  stepper1.setMaxSpeed(100.0);
//  stepper1.setAcceleration(100.0);
//  delay(100);
//  stepper2.setMaxSpeed(100.0);
//  stepper2.setAcceleration(100.0);
//  delay(500);
//  Serial.println("Putting base motor to 0 position");
//  moveMotor(40000, stepper1);  
//  delay(500);
//  resetted();
//  Serial.println("Motor on 0 position");
//}

//void responceOnWeb(String webRequest) {
//  int i = 0;
//  int value = LOW;
//  if (webRequest.indexOf(baseLeftCommand) != -1)  {
//    Serial.println("left-base");
//    moveMotor(400, stepper1);
//    valueForBase = HIGH;
//  } else if (webRequest.indexOf(baseRightCommand) != -1)  {
//    Serial.println("backward-base");
//    moveMotor(-400, stepper1);
//    valueForBase = LOW;
//  }
//}

void responceOnControlInput(int state, String directionInput) {
  while (stepper1.currentPosition() != 99999) {
    stepper1.setSpeed(100);
    if (baseStoppersCheck() and state == HIGH) {
      stepper1.runSpeed();
    } else {
      stepper1.setCurrentPosition(99999);
    }
    yield();
  }
}

//void moveMotor(int steps, AccelStepper stepperMotor) {
//  while (stepper1.currentPosition() != steps) {
//    stepper1.setSpeed(100);
//    if (baseStoppersCheck()) {
//      stepper1.runSpeed();
//    } else {
//      stepper1.setCurrentPosition(steps);
//    }
//    yield();
//  }
//}
//
//void resetted() {
//  stepper1.setCurrentPosition(0);
//}
//
//boolean baseStoppersCheck() {
//  return mcp.digitalRead(stopBtnBaseRight) == HIGH and mcp.digitalRead(stopBtnBaseLeft) == HIGH;
//}
