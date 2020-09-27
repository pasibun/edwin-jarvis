//Steppermorors
#define stapBase          5 //GPIO5---D1
#define dirBase           4 //GPIO4---D2
#define stapFirst         0 //GPIO0--D3
#define dirFirst          2 //GPIO2--D4

//micro switches for stopping the motor
#define stopBtnBaseLeft   12 //GPB4--5
#define stopBtnBaseRight  13 //GPB5--6

//controlling the motors
#define baseLeftBtn       8 //GPB0--1
#define baseRightBtn      9 //GPB1--2
#define firstAxleLeftBtn  10 //GPB2--3
#define firstAxleRightBtn 11 //GPB3--4

int valueForBase = LOW;

//for testing
String baseLeftCommand = "/Command=left-base";
String baseRightCommand = "/Command=right-base";

Adafruit_MCP23017 mcp;

AccelStepper stepper1(1, stapBase, dirBase);
AccelStepper stepper2(1, stapFirst, dirFirst);
