#include <ESP8266WiFi.h>
#include <AccelStepper.h>
#include <ShiftRegister74HC595.h>
#include "properties.h"

void setup() {
  Serial.begin(115200);
  delay(10);
  initBaseControl();
  initWebserver();
}

void loop() {
  checkForWebActivatie();
}
