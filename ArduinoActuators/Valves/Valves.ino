
int Valve1Pin = 3;
int Valve2Pin = 4;
int Valve3Pin = 5;

char serialvarString[5];
int serialvar = 0;

unsigned long previousMillis = 0; 
const long interval = 1000;
int seconds = 0;
int seconds_cleaning = 0;
int cleaning_running = 0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);

  pinMode(Valve1Pin, OUTPUT);
  pinMode(Valve2Pin, OUTPUT);
  pinMode(Valve3Pin, OUTPUT);

  
}

void loop() {

  unsigned long currentMillis = millis();

  if (currentMillis - previousMillis >= interval) {
  // save the last time you blinked the LED
  previousMillis = currentMillis;
  seconds++;
  seconds_cleaning++;
  }

   if (Serial.available() > 0) {
                serialvarString[0]=Serial.read();
                
                if(serialvarString[0]=='X')
                {
                  serialvar = 1;  
                  seconds_cleaning=0;
                }
                if(serialvarString[0]=='Y')
                {
                  serialvar = 2;
                  seconds=0;
                }
        }

  if(cleaning_running==1 && seconds_cleaning > 5)
  {
        digitalWrite(Valve1Pin, LOW);
        cleaning_running=0;
        Serial.println("Ended cleaning");
  }

switch(serialvar)
  {
  case 1:
    digitalWrite(Valve1Pin, HIGH);
    Serial.println("Cleaning Filter");
    seconds=0;
    cleaning_running=1;
    serialvar=0;
    break;
 case 2:
    digitalWrite(Valve2Pin, !digitalRead(Valve2Pin));
    if(digitalRead(Valve2Pin)==1)
    {
      Serial.println("Reserve tank ON");
    }
        if(digitalRead(Valve2Pin)==0)
    {
      Serial.println("Reserve tank OFF");
    }
    serialvar=0;
    break;
  default:
    break;
  }

}
