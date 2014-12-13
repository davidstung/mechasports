// ***************************************************************************************
// Sample RFM69 sketch for Moteino to illustrate sending and receiving, button interrupts
// ***************************************************************************************
// When you press the button on the SENDER Moteino, it will send a short message to the
// RECEIVER Moteino and wait for an ACK (acknowledgement that message was received) from 
// the RECEIVER Moteino. If the ACK was received, the SENDER will blink the onboard LED
// a few times. The RECEIVER listens to a specific token, and it alternates the onboard LED
// state from HIGH to LOW or vice versa whenever this token is received.
// ***************************************************************************************
// Hardware setup:
// ***************************************************************************************
// On the sender, hook up a momentary tactile button to D3 like this:
//          __-__
//        __|   |___
// GND ----> BTN ----> D3
// Load this sketch on the RECEIVER with NODEID=RECEIVER (adjust in config section below)
// Load this sketch on the SENDER with NODEID=SENDER (adjust in config section below)
// RFM69 library and code by Felix Rusu - felix@lowpowerlab.com
// Get libraries at: https://github.com/LowPowerLab/
// Make sure you adjust the settings in the configuration section below !!!
// **********************************************************************************
// Copyright Felix Rusu, LowPowerLab.com
// Library and code by Felix Rusu - felix@lowpowerlab.com
// **********************************************************************************
// License
// **********************************************************************************
// This program is free software; you can redistribute it 
// and/or modify it under the terms of the GNU General    
// Public License as published by the Free Software       
// Foundation; either version 3 of the License, or        
// (at your option) any later version.                    
//                                                        
// This program is distributed in the hope that it will   
// be useful, but WITHOUT ANY WARRANTY; without even the  
// implied warranty of MERCHANTABILITY or FITNESS FOR A   
// PARTICULAR PURPOSE. See the GNU General Public        
// License for more details.                              
//                                                        
// You should have received a copy of the GNU General    
// Public License along with this program.
// If not, see <http://www.gnu.org/licenses/>.
//                                                        
// Licence can be viewed at                               
// http://www.gnu.org/licenses/gpl-3.0.txt
//
// Please maintain this license information along with authorship
// and copyright notices in any redistribution of this code
// **********************************************************************************

#include <RFM69.h>    //get it here: https://www.github.com/lowpowerlab/rfm69
#include <SPI.h>
#include <LowPower.h> //get library from: https://github.com/lowpowerlab/lowpower
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_LSM303_U.h>
#include <Adafruit_BMP085_U.h>
#include <Adafruit_10DOF.h>
#include <stdio.h>
#include <stdlib.h>

/* Assign a unique ID to the sensors */
Adafruit_10DOF                dof   = Adafruit_10DOF();
Adafruit_LSM303_Accel_Unified accel = Adafruit_LSM303_Accel_Unified(30301);
Adafruit_LSM303_Mag_Unified   mag   = Adafruit_LSM303_Mag_Unified(30302);
Adafruit_BMP085_Unified       bmp   = Adafruit_BMP085_Unified(18001);

/* Update this with the correct SLP for accurate altitude measurements */
float seaLevelPressure = SENSORS_PRESSURE_SEALEVELHPA;

//*********************************************************************************************
// *********** IMPORTANT SETTINGS - YOU MUST CHANGE/ONFIGURE TO FIT YOUR HARDWARE *************
//*********************************************************************************************
#define NETWORKID     100  //the same on all nodes that talk to each other
#define RECEIVER      1    //unique ID of the gateway/receiver
#define SENDER        2
#define NODEID        SENDER  //change to "SENDER" if this is the sender node (the one with the button)
//Match frequency to the hardware version of the radio on your Moteino (uncomment one):
//#define FREQUENCY     RF69_433MHZ
#define FREQUENCY     RF69_868MHZ
//#define FREQUENCY     RF69_915MHZ
#define ENCRYPTKEY    "sampleEncryptKey" //exactly the same 16 characters/bytes on all nodes!
#define IS_RFM69HW    //uncomment only for RFM69HW! Remove/comment if you have RFM69W!
//*********************************************************************************************

#define SERIAL_BAUD   115200
#define LED           9 //Moteinos have onboard LEDs on D9
#define BUTTON_INT    1 //user button on interrupt 1 (D3)
#define BUTTON_PIN    3 //user button on interrupt 1 (D3)
RFM69 radio;


void initSensors()
{
  if(!accel.begin())
  {
    /* There was a problem detecting the LSM303 ... check your connections */
    Serial.println(F("Ooops, no LSM303 detected ... Check your wiring!"));
    while(1);
  }
  if(!mag.begin())
  {
    /* There was a problem detecting the LSM303 ... check your connections */
    Serial.println("Ooops, no LSM303 detected ... Check your wiring!");
    while(1);
  }
  if(!bmp.begin())
  {
    /* There was a problem detecting the BMP180 ... check your connections */
    Serial.println("Ooops, no BMP180 detected ... Check your wiring!");
    while(1);
  }
}


void setup() {
  Serial.begin(SERIAL_BAUD);
  radio.initialize(FREQUENCY,NODEID,NETWORKID);
#ifdef IS_RFM69HW
  radio.setHighPower(); //only for RFM69HW!
#endif
  radio.encrypt(ENCRYPTKEY);
  char buff[50];
  sprintf(buff, "\nListening at %d Mhz...", FREQUENCY==RF69_433MHZ ? 433 : FREQUENCY==RF69_868MHZ ? 868 : 915);
  Serial.println(buff);
  Serial.flush();
  
  /* Initialise the sensors */
  initSensors();
  
}

void loop() {

  
  sensors_event_t accel_event;
  sensors_event_t mag_event;
  sensors_event_t bmp_event;
  sensors_vec_t   orientation;

  /* Calculate pitch and roll from the raw accelerometer data */
  accel.getEvent(&accel_event);
  if (dof.accelGetOrientation(&accel_event, &orientation))
  {
    /* 'orientation' should have valid .roll and .pitch fields */
    /*Serial.println(F("Roll: "));
    Serial.println(orientation.roll);
    Serial.println(F("; "));w
    Serial.println(F("Pitch: "));
    Serial.println(orientation.pitch);
    Serial.println(F("; "));*/
    Serial.print("X Accel: ");
    Serial.print(accel_event.acceleration.x);
    Serial.print(" Y Accel: ");
    Serial.print(accel_event.acceleration.y);
    Serial.print(" Z Accel: ");
    Serial.print(accel_event.acceleration.z);
    Serial.println();
  }
  // test comment
  /* Calculate the heading using the magnetometer */
  /*mag.getEvent(&mag_event);
  if (dof.magGetOrientation(SENSOR_AXIS_Z, &mag_event, &orientation))
  {
    // 'orientation' should have valid .heading data now 
    Serial.println(F("Heading: "));
    Serial.println(orientation.heading);
    Serial.println(F("; "));
  }*/

  /* Calculate the altitude using the barometric pressure sensor */
  bmp.getEvent(&bmp_event);
  if (bmp_event.pressure)
  {
    /* Get ambient temperature in C */
    float temperature;
    bmp.getTemperature(&temperature);
    /* Convert atmospheric pressure, SLP and temp to altitude    */
    Serial.println(F("Alt: "));
    Serial.println(bmp.pressureToAltitude(seaLevelPressure,
                                        bmp_event.pressure,
                                        temperature)); 
    Serial.println(F(" m; "));
    /* Display the temperature */
    Serial.println(F("Temp: "));
    Serial.println(temperature);
    Serial.println(F(" C"));
  }
  
  Serial.println(F(""));
  delay(100);
  
  /*char Array[4];
  Array[0] = '\0';
  Array[1] = '\0';
  Array[2] = '\0';
  Array[3] = '\0';
  
  int Roll = (int) (orientation.roll);
  if (Roll < 0){
    Roll = Roll + 360;
    itoa(Roll, Array, 10);
  }
  else{
    itoa(Roll, Array, 10);
  }
  
  char pArray[4];
  pArray[0] = '\0';
  pArray[1] = '\0';
  pArray[2] = '\0';
  pArray[3] = '\0';
  
  int Pitch = (int) (orientation.pitch);
  if (Pitch < 0){
    Pitch = Pitch + 360;
    itoa(Pitch, pArray, 10);
  }
  else{
    itoa(Pitch, pArray, 10);
  }
    
  
  char Data[8];
  
  for (int i = 0; i < 4; i++){
    if (Array[i] == '\0'){
      Array[i] = 'R';
    }
    if (pArray[i] == '\0'){
      pArray[i] = 'P';
    }
    Data[i] = Array[i];
    Data[i+4] = pArray[i];
  }*/
  
  int acX = (int)(accel_event.acceleration.x*10);
  int acY = (int)(accel_event.acceleration.y*10);
  int acZ = (int)(accel_event.acceleration.z*10);
  char X[5], Z[5], Y[5];
  char Data[15];
  itoa(acX,X,10);
  itoa(acY,Y,10);
  itoa(acZ,Z,10);
  for (int i = 0; i < 5; i++){
    if (X[i] == '\0'){
      X[i] = 'X';
    }
    if(Y[i] == '\0'){
      Y[i] = 'Y';
    }
    if(Z[i] == '\0'){
      Z[i] = 'Z';
    }
    Data[i] = X[i];
    Data[i+5] = Y[i];
    Data[i+10] = Z[i];
  }
  
  //Array[3] = char(Roll - (Roll/1000)*1000 - (Roll/100)*100 - (Roll/10)*10);
  if (1 == 1)
  {
    //radio.sendWithRetry(RECEIVER, Data, 8); //target node Id, message as string or byte array, message length
    radio.sendWithRetry(RECEIVER, Data, 15);
    Serial.println(Data);
  }
  
  //radio.receiveDone(); //put radio in RX mode*/
  //Serial.flush(); //make sure all serial data is clocked out before sleeping the MCU
  //LowPower.powerDown(SLEEP_8S, ADC_OFF, BOD_ON); //sleep Moteino in low power mode (to save battery)
}


