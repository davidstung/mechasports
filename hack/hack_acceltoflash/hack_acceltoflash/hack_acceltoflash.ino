#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_LSM303_U.h>
#include <Adafruit_BMP085_U.h>
#include <Adafruit_10DOF.h>
#include <Adafruit_GPS.h>
#include <SoftwareSerial.h>
//#include <WirelessHEX69.h>
#include <SPIFlash.h>
//#include <RFM69.h>

#include <SPIFlash.h>    //get it here: https://github.com/LowPowerLab/SPIFlash
#include <SPI.h>

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

//////////////////////////////////////////
// flash(SPI_CS, MANUFACTURER_ID)
// SPI_CS          - CS pin attached to SPI flash chip (8 in case of Moteino)
// MANUFACTURER_ID - OPTIONAL, 0x1F44 for adesto(ex atmel) 4mbit flash
//                             0xEF30 for windbond 4mbit flash
//////////////////////////////////////////
SPIFlash flash(FLASH_SS, 0xEF30);

/* Assign a unique ID to the sensors */
Adafruit_10DOF                dof   = Adafruit_10DOF();
Adafruit_LSM303_Accel_Unified accel = Adafruit_LSM303_Accel_Unified(30301);
Adafruit_LSM303_Mag_Unified   mag   = Adafruit_LSM303_Mag_Unified(30302);
Adafruit_BMP085_Unified       bmp   = Adafruit_BMP085_Unified(18001);

/* Update this with the correct SLP for accurate altitude measurements */
float seaLevelPressure = SENSORS_PRESSURE_SEALEVELHPA;

SoftwareSerial mySerial(5, 4);
Adafruit_GPS GPS(&mySerial);

// Set GPSECHO to 'false' to turn off echoing the GPS data to the Serial console
// Set to 'true' if you want to debug and listen to the raw GPS sentences. 
#define GPSECHO  true
uint32_t timer = millis();

// this keeps track of whether we're using the interrupt
// off by default!
boolean usingInterrupt = false;
void useInterrupt(boolean); // Func prototype keeps Arduino 0023 happy
/**************************************************************************/
/*!
    @brief  Initialises all the sensors used by this example
*/
/**************************************************************************/
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

/**************************************************************************/
/*!
*/
/**************************************************************************/
void setup(void)
{
  Serial.begin(115200);
  Serial.println(F("Adafruit 10 DOF Pitch/Roll/Heading Example")); Serial.println("");
  
  /* Initialise the sensors */
  initSensors();

    Serial.begin(SERIAL_BAUD);
  Serial.print("Start...");

  if (flash.initialize())
    Serial.println("Init OK!");
  else
    Serial.println("Init FAIL!");
//  GPS.begin(9600);
//  
//  GPS.sendCommand(PMTK_SET_NMEA_OUTPUT_RMCGGA);
//  
//    // Set the update rate
//  GPS.sendCommand(PMTK_SET_NMEA_UPDATE_1HZ);   // 1 Hz update rate
//  // For the parsing code to work nicely and have time to sort thru the data, and
//  // print it out we don't suggest using anything higher than 1 Hz
//
//  // Request updates on antenna status, comment out to keep quiet
//  GPS.sendCommand(PGCMD_ANTENNA);
//
//  // the nice thing about this code is you can have a timer0 interrupt go off
//  // every 1 millisecond, and read data from the GPS for you. that makes the
//  // loop code a heck of a lot easier!
//  useInterrupt(true);
//
//  delay(1000);
  // Ask for firmware version
  mySerial.println(PMTK_Q_RELEASE);
  
}

// Interrupt is called once a millisecond, looks for any new GPS data, and stores it
//SIGNAL(TIMER0_COMPA_vect) {
//  char c = GPS.read();
//  // if you want to debug, this is a good time to do it!
//#ifdef UDR0
//  if (GPSECHO)
//    if (c) UDR0 = c;  
//    // writing direct to UDR0 is much much faster than Serial.print 
//    // but only one character can be written at a time. 
//#endif
//}

//void useInterrupt(boolean v) {
//  if (v) {
//    // Timer0 is already used for millis() - we'll just interrupt somewhere
//    // in the middle and call the "Compare A" function above
//    OCR0A = 0xAF;
//    TIMSK0 |= _BV(OCIE0A);
//    usingInterrupt = true;
//  } else {
//    // do not call the interrupt function COMPA anymore
//    TIMSK0 &= ~_BV(OCIE0A);
//    usingInterrupt = false;
//  }
//}

/**************************************************************************/
/*!
    @brief  Constantly check the roll/pitch/heading/altitude/temperature
*/
/**************************************************************************/
void loop(void)
{
  sensors_event_t accel_event;
  sensors_event_t mag_event;
  sensors_event_t bmp_event;
  sensors_vec_t   orientation;

  /* Calculate pitch and roll from the raw accelerometer data */
  accel.getEvent(&accel_event);
  if (dof.accelGetOrientation(&accel_event, &orientation))
  {
    /* 'orientation' should have valid .roll and .pitch fields */
    // Serial.println(F("Roll: "));
    // Serial.println(orientation.roll);
    // Serial.println(F("; "));
    // Serial.println(F("Pitch: "));
    // Serial.println(orientation.pitch);
    // Serial.println(F("; "));
    Serial.print("\nWriteByte("); Serial.print(input); Serial.print(")");
    flash.writeByte(input-48, millis()%2 ? 0xaa : 0xbb);

  }

    if (Serial.available() > 0) {
    input = Serial.read();
    if (input == 'd') //d=dump flash area
    {
      Serial.println("Flash content:");
      int counter = 0;

      while(counter<=256){
        Serial.print(flash.readByte(counter++), HEX);
        Serial.print('.');
      }
      
      Serial.println();
    }
    else if (input == 'e')
    {
      Serial.print("Erasing Flash chip ... ");
      flash.chipErase();
      while(flash.busy());
      Serial.println("DONE");
    }
    else if (input == 'i')
    {
      Serial.print("DeviceID: ");
      Serial.println(flash.readDeviceId(), HEX);
    }
    // else if (input >= 48 && input <= 57) //0-9
    // {
    //   Serial.print("\nWriteByte("); Serial.print(input); Serial.print(")");
    //   flash.writeByte(input-48, millis()%2 ? 0xaa : 0xbb);
    // }
  }

  // Periodically blink the onboard LED while listening for serial commands
  if ((int)(millis()/500) > lastPeriod)
  {
    lastPeriod++;
    pinMode(9, OUTPUT);
    digitalWrite(9, lastPeriod%2);
  }
  
  /* Calculate the heading using the magnetometer */
//  mag.getEvent(&mag_event);
//  if (dof.magGetOrientation(SENSOR_AXIS_Z, &mag_event, &orientation))
//  {
//    /* 'orientation' should have valid .heading data now */
//    Serial.println(F("Heading: "));
//    Serial.println(orientation.heading);
//    Serial.println(F("; "));
//  }
//
//  /* Calculate the altitude using the barometric pressure sensor */
//  bmp.getEvent(&bmp_event);
//  if (bmp_event.pressure)
//  {
//    /* Get ambient temperature in C */
//    float temperature;
//    bmp.getTemperature(&temperature);
//    /* Convert atmospheric pressure, SLP and temp to altitude    */
//    Serial.println(F("Alt: "));
//    Serial.println(bmp.pressureToAltitude(seaLevelPressure,
//                                        bmp_event.pressure,
//                                        temperature)); 
//    Serial.println(F(" m; "));
    /* Display the temperature */
//    Serial.println(F("Temp: "));
//    Serial.println(temperature);
//    Serial.println(F(" C"));
//  }
  
//  Serial.println(F(""));
//  delay(1000);
//  
//  // in case you are not using the interrupt above, you'll
//  // need to 'hand query' the GPS, not suggested :(
//  if (! usingInterrupt) {
//    // read data from the GPS in the 'main loop'
//    char c = GPS.read();
//    // if you want to debug, this is a good time to do it!
//    if (GPSECHO)
//      if (c) Serial.print(c);
//  }
//  
//  // if a sentence is received, we can check the checksum, parse it...
//  if (GPS.newNMEAreceived()) {
//    // a tricky thing here is if we print the NMEA sentence, or data
//    // we end up not listening and catching other sentences! 
//    // so be very wary if using OUTPUT_ALLDATA and trytng to print out data
//    //Serial.println(GPS.lastNMEA());   // this also sets the newNMEAreceived() flag to false
//  
//    if (!GPS.parse(GPS.lastNMEA()))   // this also sets the newNMEAreceived() flag to false
//      return;  // we can fail to parse a sentence in which case we should just wait for another
//  }
//
//  // if millis() or timer wraps around, we'll just reset it
//  if (timer > millis())  timer = millis();
//
//  // approximately every 2 seconds or so, print out the current stats
//  if (millis() - timer > 2000) { 
//    timer = millis(); // reset the timer
//    
//    Serial.print("\nTime: ");
//    Serial.print(GPS.hour, DEC); Serial.print(':');
//    Serial.print(GPS.minute, DEC); Serial.print(':');
//    Serial.print(GPS.seconds, DEC); Serial.print('.');
//    Serial.println(GPS.milliseconds);
//    Serial.print("Date: ");
//    Serial.print(GPS.day, DEC); Serial.print('/');
//    Serial.print(GPS.month, DEC); Serial.print("/20");
//    Serial.println(GPS.year, DEC);
//    Serial.print("Fix: "); Serial.print((int)GPS.fix);
//    Serial.print(" quality: "); Serial.println((int)GPS.fixquality); 
//    if (GPS.fix) {
//      Serial.print("Location: ");
//      Serial.print(GPS.latitude, 4); Serial.print(GPS.lat);
//      Serial.print(", "); 
//      Serial.print(GPS.longitude, 4); Serial.println(GPS.lon);
//      Serial.print("Location (in degrees, works with Google Maps): ");
//      Serial.print(GPS.latitudeDegrees, 4);
//      Serial.print(", "); 
//      Serial.println(GPS.longitudeDegrees, 4);
//      
//      Serial.print("Speed (knots): "); Serial.println(GPS.speed);
//      Serial.print("Angle: "); Serial.println(GPS.angle);
//      Serial.print("Altitude: "); Serial.println(GPS.altitude);
//      Serial.print("Satellites: "); Serial.println((int)GPS.satellites);
//    }
//  }
  
}
