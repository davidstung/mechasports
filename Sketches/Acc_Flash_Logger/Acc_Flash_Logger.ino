#include <SPIFlash.h>    //get it here: https://github.com/LowPowerLab/SPIFlash
#include <SPI.h>

#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_LSM303_U.h>
#include <Adafruit_BMP085_U.h>
#include <Adafruit_L3GD20_U.h>
#include <Adafruit_10DOF.h>

#define SERIAL_BAUD      115200
char input = 0;
long lastPeriod = -1;

#ifdef __AVR_ATmega1284P__
  #define LED           15 // Moteino MEGAs have LEDs on D15
  #define FLASH_SS      23 // and FLASH SS on D23
#else
  #define LED           9 // Moteinos have LEDs on D9
  #define FLASH_SS      8 // and FLASH SS on D8
#endif

SPIFlash flash(FLASH_SS, 0xEF30);

/* Assign a unique ID to the sensors */
Adafruit_LSM303_Accel_Unified accel = Adafruit_LSM303_Accel_Unified(30301);
Adafruit_LSM303_Mag_Unified   mag   = Adafruit_LSM303_Mag_Unified(30302);
Adafruit_BMP085_Unified       bmp   = Adafruit_BMP085_Unified(18001);
Adafruit_L3GD20_Unified       gyro  = Adafruit_L3GD20_Unified(20);

uint32_t Index;

uint32_t Page;

union fit
{
  char bytes[4];
  float f;
  uint32_t i;
} fit;


void setup(){
  
  Serial.begin(SERIAL_BAUD);
  Serial.print("Start...");
  
  flash.chipErase();
  while(flash.busy());
  Serial.println("Chip Erased!");
  
  if (flash.initialize())
    Serial.println("Init OK!");
  else
    Serial.println("Init FAIL!");

  FinishPages();
  Serial.println("Memory Prepared!");
  accel.begin();
  gyro.begin();
  
  Index = 0;
  Page = 0;
  
  Serial.println("here");
}

void loop()
{
  if (Index / 6 < 21000){
    sensors_event_t event;
    accel.getEvent(&event);
    
    
    Extracter(event.acceleration.x);
    WriteData(0);
    Serial.print(fit.f);
    Serial.print(",");
    Extracter(event.acceleration.y);
    WriteData(1);
    Serial.print(fit.f);
    Serial.print(",");
    Extracter(event.acceleration.z);
    WriteData(2);
    Serial.print(fit.f);
    Serial.print(",");
    
    gyro.getEvent(&event);
    Extracter(event.gyro.x);
    WriteData(3);
    Serial.print(fit.f);
    Serial.print(",");
    Extracter(event.gyro.y);
    WriteData(4);
    Serial.print(fit.f);
    Serial.print(",");
    Extracter(event.gyro.z);
    WriteData(5);
    Serial.print(fit.f);
    Serial.print(",");
    Serial.println();    
    Index++;
  }
  
  if (Index == 10){
    //FinishPage();
    Index = 0;
    Page++;
  }
  Serial.println(Page*10+Index);
  delay(20);
}

void Extracter(float magnitude){

  fit.f = magnitude;
  
}

void Extracter2 (void){

  fit.i = Index;
  
}


void WriteData(uint32_t Offset){
  for (uint32_t i = 0; i < 4; i++){
    flash.writeByte(Page*256+(Index*24)+4*Offset+i,fit.bytes[i]);
  }
}

void FinishPage(void){
  for (uint32_t i = 0; i < 16; i++){
    flash.writeByte(Page*256+(Index*24)+i,0x00);
  }
}

void FinishPages(void){
  for (uint32_t j = 0; j < 2048; j++){
    for (uint32_t i = 0; i < 16; i++){
      flash.writeByte(j*256+(10*24)+i,0x00);
    }
  }
}


