#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <AccelStepper.h>
#include "Adafruit_MCP23017.h"
#include "properties.h"

void setup() {
  Serial.begin(115200);
  mcp.begin();
  delay(100);  
  initBaseControl();
  delay(100);
  //initControlBoard();
  //initWebserver();
}

void loop() {
  Serial.println(mcp.digitalRead(stopBtnBaseLeft));
  Serial.println(mcp.digitalRead(stopBtnBaseRight));
  //checkForWebActivatie();  
  //btnControl();  
}

void initBaseControl() {
  Serial.println("Init base controler");
  mcp.pinMode(stopBtnBaseLeft, INPUT);
  mcp.pinMode(stopBtnBaseRight, INPUT);
  
  stepper1.setMaxSpeed(100.0);
  stepper1.setAcceleration(100.0);
  delay(100);
  stepper2.setMaxSpeed(100.0);
  stepper2.setAcceleration(100.0);
  delay(500);
  Serial.println("Putting base motor to 0 position");
  
  //moveMotor(40000, stepper1);  
  delay(500);
  //resetted();
  Serial.println("Motor on 0 position");
}

void initControlBoard(){
  Serial.println("Init control board");  
  mcp.pinMode(baseLeftBtn, INPUT);
  mcp.pinMode(baseRightBtn, INPUT);
  mcp.pinMode(firstAxleLeftBtn, INPUT);
  mcp.pinMode(firstAxleRightBtn, INPUT);
  delay(100);
}

void btnControl(){  
  Serial.print("Left: ");
  Serial.print(mcp.digitalRead(baseLeftBtn));
  Serial.println("");
  Serial.print("Right: ");
  Serial.print(mcp.digitalRead(baseRightBtn));
  Serial.println("");
  //responceOnControlInput(mcp.digitalRead(baseLeftBtn), "Left");
  //responceOnControlInput(mcp.digitalRead(baseRightBtn), "Right");  
}

void moveMotor(int steps, AccelStepper stepperMotor) {
  while (stepper1.currentPosition() != steps) {
    stepper1.setSpeed(100);
    if (baseStoppersCheck()) {
      stepper1.runSpeed();
    } else {
      stepper1.setCurrentPosition(steps);
    }
    yield();
  }
}

void resetted() {
  stepper1.setCurrentPosition(0);
}

boolean baseStoppersCheck() {
  return mcp.digitalRead(stopBtnBaseRight) == HIGH or mcp.digitalRead(stopBtnBaseLeft) == HIGH;
}
