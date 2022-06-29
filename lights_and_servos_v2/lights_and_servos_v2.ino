#include <Wire.h>
#include <Adafruit_MotorShield.h>
#include <FastLED.h>

// How many leds in your strip?
#define NUM_LEDS 21

// For led chips like Neopixels, which have a data line, ground, and power, you just
// need to define DATA_PIN.  For led chipsets that are SPI based (four wires - data, clock,
// ground, and power), like the LPD8806 define both DATA_PIN and CLOCK_PIN
#define DATA_PIN 4
Adafruit_MotorShield AFMS = Adafruit_MotorShield();
Adafruit_StepperMotor *myMotor = AFMS.getStepper(200, 1);
Adafruit_DCMotor *myDCMotor = AFMS.getMotor(4);
// Define the array of leds
CRGB leds[NUM_LEDS];
//float brightness;
float rate = 0.1;

const int pwmA = 3;
const int pwmB = 11;
const int brakeA = 9;
const int brakeB = 8;
const int dirA = 12;
const int dirB = 13;
const int stepsPerRevolution = 200;  // change this to fit the number of steps per revolution
String inputString = "";         // a String to hold incoming data
bool stringComplete = false;
bool goStep = false;

//Stepper myStepper(stepsPerRevolution, 12, 13);


// Define the AccelStepper interface type:
//#define MotorInterfaceType 2

// Create a new instance of the AccelStepper class:
//AccelStepper myStepper = AccelStepper(MotorInterfaceType, dirA, dirB);

float fadeAmount = 0.5;
float brightness = 0;


void setup() {
  // put your setup code here, to run once:
  
  Serial.begin(9600);
  // reserve 200 bytes for the inputString:
  inputString.reserve(200);
  FastLED.addLeds<WS2812B, DATA_PIN, RGB>(leds, NUM_LEDS);
  FastLED.setBrightness(84);
  switchOnLEDS();
  AFMS.begin();
  myMotor->setSpeed(5);  // 10 rpm
  myDCMotor->setSpeed(150);
  myDCMotor->run(FORWARD);
  int nbSteps=200;
switchOnLEDS();
   delay(500);
    switchOffLEDS();
  delay(500);
    switchOnLEDS();
    delay(500);
    switchOffLEDS();
    delay(500);
    switchOnLEDS();
    delay(500);
    switchOffLEDS();
    delay(500);
    switchOnLEDS();
    delay(500);
    switchOffLEDS();
    delay(500);
    switchOnLEDS();
    delay(500);
    switchOffLEDS();
    delay(500);
    switchOnLEDS();
    myMotor->step(nbSteps, FORWARD, INTERLEAVE);
    delay(500);
    myMotor->release();//step(nbSteps, BACKWARD, INTERLEAVE);
}

void loop() {
  //  turnOffStepper();


  //
  if (stringComplete) {
//    int nbSteps=200;
Serial.println("complete");
//    myMotor->step(nbSteps, FORWARD, INTERLEAVE);
    // clear the string:
    inputString = "";
    stringComplete = false;
    goStep = true;
    switchOffLEDS();
    delay(100);
    switchOnLEDS();
    delay(100);
    switchOffLEDS();
    delay(100);
    switchOnLEDS();
    delay(100);
    switchOffLEDS();
    delay(100);
    switchOnLEDS();

//    myStepper.enableOutputs();
  }
  if (goStep) {
     int nbSteps=50;

//    myMotor->step(nbSteps, FORWARD, DOUBLE);
    switchOffLEDS();
//    myMotor->release();
    //
    //    myStepper.moveTo(50);
    //    myStepper.setSpeed(30);
    //    myStepper.runSpeedToPosition();
    //
    //
    //    if (myStepper.distanceToGo() <= 0) {
    //      goStep = false;
    //      myStepper.setCurrentPosition(0);
    //      myStepper.disableOutputs();
    //
    //    }
  }
  else {
    //    pulseLEDS();
    switchOnLEDS();

  }
}


void turnOffStepper() {
  digitalWrite(pwmA, LOW);
  digitalWrite(pwmB, LOW);
}
void turnOnStepper() {
  digitalWrite(pwmA, HIGH);
  digitalWrite(pwmB, HIGH);
}

void setupStepper() {
  pinMode(pwmA, OUTPUT);
  pinMode(pwmB, OUTPUT);
  pinMode(brakeA, OUTPUT);
  pinMode(brakeB, OUTPUT);
  digitalWrite(pwmA, HIGH);
  digitalWrite(pwmB, HIGH);
  digitalWrite(brakeA, LOW);
  digitalWrite(brakeB, LOW);
  // set the motor speed (for multiple steps only):
//  myStepper.setMaxSpeed(200);


}


void serialEvent() {
  while (Serial.available()) {
    // get the new byte:
    char inChar = (char)Serial.read();
    // add it to the inputString:
    inputString += inChar;
    // if the incoming character is a newline, set a flag so the main loop can
    // do something about it:
    if (inChar == '\n') {
      stringComplete = true;
    }
  }
}
void pulseLEDS() {

  for (int i = 0; i < NUM_LEDS; i++ )
  {
    leds[i].setRGB(255, 255, 255); // Set Color HERE!!!
    leds[i].fadeLightBy(brightness);
  }
  brightness = brightness + fadeAmount;
  // reverse the direction of the fading at the ends of the fade:
  if (brightness < 0 || brightness > 255)
  {
    fadeAmount = -fadeAmount ;
  }
  FastLED.show();
}
void switchOnLEDS() {
  for (int i = 0; i < NUM_LEDS; i++) {
    leds[i] = CRGB::White;
    FastLED.show();
  }
}
void switchOffLEDS() {
  for (int i = 0; i < NUM_LEDS; i++) {
    leds[i] = CRGB::Black;
    FastLED.show();
  }
}
