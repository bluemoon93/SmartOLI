// First we include the libraries
#include <OneWire.h> 
#include <DallasTemperature.h>

const int GP2Y02 = 0;
const int US0_trigPin = 9;
const int US0_echoPin = 10;
const int US1_trigPin = 11;
const int US1_echoPin = 12;
const int ph_pin = 2;
float irValue, distance0, distance1, phValue;

OneWire oneWire(ph_pin); 
DallasTemperature sensors(&oneWire);

void setup() {
  pinMode(US0_trigPin, OUTPUT); // Sets the trigPin as an Output
  pinMode(US0_echoPin, INPUT); // Sets the echoPin as an Input
  pinMode(US1_trigPin, OUTPUT); // Sets the trigPin as an Output
  pinMode(US1_echoPin, INPUT); // Sets the echoPin as an Input
  sensors.begin(); 
  Serial.begin(9600);
}

void loop() {
  // Read IR sensor
  irValue=2547.8/((float)analogRead(GP2Y02)*0.49-10.41)-0.42;
  if(irValue<5)
    irValue=5;
  else if(irValue>80)
    irValue=80;

  // Clears the trigPin
  digitalWrite(US0_trigPin, LOW);
  delayMicroseconds(2);
  
  // Sets the trigPin on HIGH state for 10 micro seconds
  digitalWrite(US0_trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(US0_trigPin, LOW);
  
  // Reads the echoPin, returns the sound wave travel time in microseconds
  // Calculating the distance
  distance0 = pulseIn(US0_echoPin, HIGH, 12000)*0.034/2;
  if(distance0 == 0) distance0 = 200;

  // Clears the trigPin
  digitalWrite(US1_trigPin, LOW);
  delayMicroseconds(2);
  
  // Sets the trigPin on HIGH state for 10 micro seconds
  digitalWrite(US1_trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(US1_trigPin, LOW);
  
  // Reads the echoPin, returns the sound wave travel time in microseconds
  // Calculating the distance
  distance1 = pulseIn(US1_echoPin, HIGH, 3000)*0.034/2;
  if(distance1 == 0) distance1 = 50;


  // Ocasionally send the command to get temperature readings 
  if(random(0, 20)==0)
    sensors.requestTemperatures(); 
  phValue = sensors.getTempCByIndex(0);

  // prints IR sensor
  Serial.print(irValue);
  Serial.print(";");
  // Prints the distance on the Serial Monitor
  Serial.print(distance0);
  Serial.print(";");
  // print water level
  Serial.print(distance1);
  Serial.print(";");
  // print pH
  Serial.print(phValue);
  Serial.println(";");
}
