/*=============================================================================

  File: PulseExample.pde

  Description: This file demonstrates an example use of the Pulse library.
  
  Notes: N/A
    
  See Also: N/A
    
  10 Feb 2011
  Stellios Leventis

=============================================================================*/
/*---------------------------Dependencies------------------------------------*/
#include <Pulse.h>

/*---------------------------Wiring Constants--------------------------------*/
/*---------------------------Definitions-------------------------------------*/
/*---------------------------Helper-Function Prototypes----------------------*/
/*---------------------------Module Variables--------------------------------*/
/*---------------------------Module Code-------------------------------------*/
void setup() {
  unsigned int period = 100;  // in units of 1/10 millisecond, can be 10 
                              // through 1000 inclusive
  unsigned char pin = 2;      // pin to pulse, can be 2 through 13 inclusive
  if (InitPulse(pin, period) != INIT_OK) {
    // TODO: react to an invalid initialization
  }
}

void loop() {
  if (IsPulseFinished()) Pulse(100);
}
