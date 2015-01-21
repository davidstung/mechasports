#include <SoftwareSerial.h>

char * Latitude;
char * NS;
char * Longitude;
char * EW;
char * Time;
char * Date;
char * Alt;
char * Speed;
boolean Fix;

int newGGA;
int newRMC;
int Locations[25];
String strGPS;
SoftwareSerial portGPS(5,4);
int SeshID = 0;
int Start;

float Velocity;
float dT;
float curTime;
float preTime;

char gpsData[100];
int gpsDataPos;

int ggaBool;
int rmcBool;
int stBool;

void setup() {
  Serial.begin(115200); 
  portGPS.begin(9600);
  delay(5000);
  newGGA = 0;
  newRMC = 0;
  gpsDataPos = 0;
  ggaBool = 0;
  rmcBool = 0;
  Start = 0;
  Velocity = 0;
  pinMode(14,OUTPUT);
  pinMode(15,OUTPUT);
  Fix = false;
  preTime = 0;
  curTime = 0;
  gpsInit();
  
}

void gpsInit(){
  delay(1000);
  portGPS.write("$PGCMD,33,0*6D\r\n");
  delay(100);
  portGPS.write("$PMTK220,100*2F\r\n");
  delay(100);
  portGPS.write("$PMTK314,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0*29\r\n");
  delay(100);
  //#define PMTK_SET_NMEA_UPDATE_5HZ  "$PMTK220,200*2C"
//#define PMTK_SET_NMEA_UPDATE_10HZ "$PMTK220,100*2F"
//#define PMTK_SET_NMEA_UPDATE_1HZ  "$PMTK220,1000*1F"
//#define PGCMD_NOANTENNA "$PGCMD,33,0*6D" 
//#define PMTK_SET_NMEA_OUTPUT_RMCONLY "$PMTK314,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0*29"
//#define PMTK_SET_NMEA_OUTPUT_RMCGGA "$PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0*28"
//
}

void loop(){
  char Test = '4';
  if (portGPS.read() == '$'){
    Test = '.';
    while(Test != '\n'){
      if (portGPS.available()){
        Test = portGPS.read();
        gpsData[gpsDataPos] = Test;
        gpsDataPos++;
      }
    }
    if (gpsData[2] == 'R' and rmcBool == 0){
      //Serial.println(gpsData);
      FindCommas();
      CheckFix();
      if (Fix == false){
        digitalWrite(14,HIGH);
        digitalWrite(15,HIGH);
      }
      else{
        InitRMCHolder();
        ExtractRMCData();
        rmcBool = 1;
      }
    }
    if (rmcBool == 1 and Fix == true){
      Serial.println(gpsData);
      Serial.println();
      Serial.print(Date);
      Serial.print(" ");
      Serial.print(Time);
      Serial.print(" ");
      Serial.print(Alt);
      Serial.print(" ");
      Serial.print(Speed);
      Serial.print(" ");
      Serial.print(Velocity);
      Serial.println();
      if (Velocity < 2){
        digitalWrite(14,LOW);
        digitalWrite(15,LOW);
      }
      else if (Velocity > 2 && Velocity < 4 ){
        digitalWrite(14,LOW);
        digitalWrite(15,HIGH);
      }
      else if (Velocity > 4 && Velocity < 6){
        digitalWrite(14,HIGH);
        digitalWrite(15,LOW);
      }
      else{
        digitalWrite(14,HIGH);
        digitalWrite(15,HIGH);
      }
      FreeAlloc();
      rmcBool = 0;
    }
    NullgpsData();
    gpsDataPos = 0;
  }
}

void NullgpsData(void){
  for (int i = 0; i < gpsDataPos; i++){
    gpsData[i] = '\0';
  }
}  

void NullString(char * str, int length){
  for (int i = 0; i < length; i++){
    str[i] = '\0';
  }
}

void FindCommas(){
  int i = 0;
  int Index = 0;
  ResetLocations();
  while(i < gpsDataPos){
    if (gpsData[i] == ','){
      Locations[Index] = i;
      Index++;
    }
    i++;
  };
}

void CheckFix(){
  if (gpsData[Locations[1]+1] == 'A'){
    Fix = true;
  }
  else{
    Fix = false;
  }
}


void InitRMCHolder(){
  Time = (char *)malloc((Locations[1]-Locations[0])*sizeof(char)); 
  Date = (char *) malloc((Locations[9]-Locations[8])*sizeof(char));
  Speed = (char *) malloc((Locations[7]-Locations[6])*sizeof(char));

  NullString(Date,Locations[9]-Locations[8]);
  NullString(Speed,Locations[7]-Locations[6]);
  NullString(Time,Locations[1]-Locations[0]);

}


void ExtractRMCData(){
  for (int i = Locations[8] + 1; i < Locations[9]; i++){
    Date[i-Locations[8]-1] = gpsData[i];
  }
  
  for (int i = Locations[6] + 1; i < Locations[7]; i++){
    Speed[i-Locations[6]-1] = gpsData[i];
  }
  
  Velocity = atof(Speed);
  
  for (int i = Locations[0] + 1; i < Locations[1]; i++){
    Time[i-Locations[0]-1] = gpsData[i];
  }
}

void FreeAlloc(){
  //free(Latitude);
  //free(NS);
  //free(Longitude);
  //free(EW);
  free(Time);
  free(Date);
  free(Speed);
}

void ResetLocations(){
  for (int i = 0; i < 25; i++){
    Locations[i] = 0;
  }
}
