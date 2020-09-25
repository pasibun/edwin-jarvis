AccelStepper stepper1(1, stapBase, dirBase);
AccelStepper stepper2(1, stapFirst, dirFirst);

void initBaseControl() {
  pinMode(stopBtnBaseLeft, INPUT);
  pinMode(stopBtnBaseRight, INPUT);
  stepper1.setMaxSpeed(400.0);
  stepper1.setAcceleration(100.0);

  stepper2.setMaxSpeed(400.0);
  stepper2.setAcceleration(100.0);
}

void responceOnWeb(String webRequest) {
  Serial.println(digitalRead(stopBtnBaseLeft));
  Serial.println(digitalRead(stopBtnBaseRight));
    stepper1.setCurrentPosition(0);
    while (stepper1.currentPosition() != 400) {
      stepper1.setSpeed(200);
      stepper1.runSpeed();
    }    
    delay(1000);


  //  int i = 0;
  //  int value = LOW;
  //  if (webRequest.indexOf("/Command=forward-base") != -1)  {
  //    Serial.println("forward-base");
  //    digitalWrite(dirBase, HIGH);
  //    for ( i = 1; i <= (RoundForBase / 4); i++) {
  //      digitalWrite(stapBase, HIGH);
  //      delay(1);
  //      digitalWrite(stapBase, LOW);
  //      delay(1);
  //    }
  //    valueForBase = HIGH;
  //  } else if (webRequest.indexOf("/Command=backward-base") != -1)  {
  //    Serial.println("backward-base");
  //    digitalWrite(dirBase, LOW);
  //    for ( i = 1; i <= (RoundForBase / 4); i++) {
  //      digitalWrite(stapBase, HIGH);
  //      delay(1);
  //      digitalWrite(stapBase, LOW);
  //      delay(1);
  //    }
  //    valueForBase = LOW;
  //  }
}
