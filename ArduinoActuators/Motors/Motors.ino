#include <HCMotor.h>

#include <TimerOne.h>
#include <Servo.h>

//#include "TimerOne.h"
/*

Servo Pins
Blue - 5Vdc
Black - 0V
Yellow - Signal - P10

Distance sensor, presence Pins:
VCC: +5VDC
Trig : Trigger (INPUT) - Pin11
Echo: Echo (OUTPUT) - Pin 12
GND: GND

Distance sensor, water level Pins:
VCC: +5VDC
Trig : Trigger (INPUT) - Pin 7
Echo: Echo (OUTPUT) - Pin 6
GND: GND

*/
Servo myservo1;  // create servo object to control a servo
HCMotor HCMotor; // Step motor

/*Servos Pins and Vars*/

int posServo_1 = 90;    // variable to store the servo posServo_1ition
int servoPin_1 = 10;

#define DIR_PIN 8 //Connect to drive modules 'direction' input.
#define CLK_PIN 9 //Connect to drive modules 'step' or 'CLK' input.

int LedPin = 5; 
int LedDC = 0;  

int ValvePin = 11;



int serialvar = 0;
char serialvarString[5];
int counter = 0;

unsigned long previousMillis = 0; 
const long interval = 1000;
int seconds = 0;
int seconds_lid_up = 0;
int seconds_lid_down = 0;
bool flag_lid_up = 0;
bool flag_lid_down = 0;


void setup() {
  myservo1.attach(10);  // attaches the servo on pin 9 to the servo object
  Serial.begin(9600);

  myservo1.write(posServo_1);              // tell servo to go to position in variable 'pos'

  pinMode(LedPin, OUTPUT);
  pinMode(ValvePin, OUTPUT);

  HCMotor.Init();
  HCMotor.attach(0, STEPPER, CLK_PIN, DIR_PIN);
  HCMotor.Steps(0,CONTINUOUS);
  //Serial.write("System Ready \n");
  
}

void loop() {


  unsigned long currentMillis = millis();

  if (currentMillis - previousMillis >= interval) {
  // save the last time you blinked the LED
  previousMillis = currentMillis;
  seconds++;
  seconds_lid_up++;
  seconds_lid_down++;
  Serial.println(seconds);
  Serial.println(seconds_lid_up);
  Serial.println(seconds_lid_down);
  Serial.println(serialvar);
  Serial.println(flag_lid_up);
  Serial.println(flag_lid_down);
  }

/*
**********************************************************************************************
*Test routine to simulate full and half flush CMD
**********************************************************************************************
*/
 if (Serial.available() > 0) {
                serialvarString[0]=Serial.read();
                
                if(serialvarString[0]=='A')
                {
                  serialvar = 1;  
                  //Serial.println("Half");
                  seconds=0;
                }
                if(serialvarString[0]=='B')
                {
                  serialvar = 2;  
                  //Serial.println("Full");
                  seconds=0;
                }
                if(serialvarString[0]=='C')
                {
                  serialvar = 3;  
                  //Serial.println("End");
                }
                if(serialvarString[0]=='D')
                {
                  serialvar = 4;  
                  //Serial.println("Led 0");
                }
                if(serialvarString[0]=='E')
                {
                  serialvar = 5;  
                  //Serial.println("Led 50");
                }
                if(serialvarString[0]=='F')
                {
                  serialvar = 6;  
                  Serial.println("Led 100");
                }
                 if(serialvarString[0]=='G')
                {
                  serialvar = 7;  
                  Serial.println("Lid Up");
                }
                 if(serialvarString[0]=='H')
                {
                  serialvar = 8;  
                  Serial.println("Lid Down");
                }
                 if(serialvarString[0]=='J')
                {
                  serialvar = 9;  
                  Serial.println("Lid Stop");
                }
                 if(serialvarString[0]=='K')
                {
                  serialvar = 10;  
                  Serial.println("Filter clean");
                }
                
        }

  /* FLUSH TIME CONTROL*/

  if(serialvar==1 && seconds >= 2)
  {
    serialvar = 3;
  }
  if(serialvar==2 && seconds >= 2)
  {
    serialvar = 3;
  }
  if(seconds_lid_up > 15 && flag_lid_up==1)
  {
      serialvar=9;
  }
    if(seconds_lid_down > 16 && flag_lid_down==1)
  {
      serialvar=9;
  }

  /* SERVO POSITION CONTROL  */
  
  switch(serialvar)
  {
  case 1:
    posServo_1 = 121;
    myservo1.write(posServo_1);              // tell servo to go to position in variable 'pos'
    //Serial.println(posServo_1);
    break;
 case 2:
    posServo_1 = 42;
    myservo1.write(posServo_1);              // tell servo to go to position in variable 'pos'
    //Serial.println(pos);
    break;
  case 3:
    posServo_1 = 90;
    myservo1.write(posServo_1);              // tell servo to go to position in variable 'pos'
    //Serial.println(posServo_1);
    break;
  case 4:                                    // LED OFF
    analogWrite(LedPin,0); 
    break;
  case 5:                                    // LED 50
    analogWrite(LedPin,50);
    break;
  case 6:                                    // LED 100
    analogWrite(LedPin,100);
    break;
  case 7:                                    // Lid Up
    HCMotor.Direction(0, FORWARD);
    HCMotor.DutyCycle(0, 400);
    seconds_lid_up=0;
    flag_lid_up=1;
    serialvar=0;
    Serial.println("Lid Up ACK");
    break;
  case 8:                                    // Lid Down
    HCMotor.Direction(0, REVERSE);
    HCMotor.DutyCycle(0, 400);
    seconds_lid_down=0;
    flag_lid_down=1;
    serialvar=0;
    Serial.println("Lid Down ACK");
    break;
  case 9:                                    // Lid Down
    HCMotor.DutyCycle(0, 0);
    flag_lid_down=0;
    flag_lid_up=0;
    //serialvar=0;
    break;
 case 10:                                    // Clean filter
    digitalWrite(ValvePin,HIGH);
    delay(4000);
    digitalWrite(ValvePin,LOW);
    Serial.println("Filter Cleaned");
    //serialvar=0;
    break;
  
  default:
    break;
  }

    
  delay(15);                       // waits 15ms for the servo to reach the position
}
