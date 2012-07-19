// Send out a radio packet every minute, consuming as little power as possible
// 2010-08-29 <jc@wippler.nl> http://opensource.org/licenses/mit-license.php

#include <JeeLib.h>

static long payload;

// this must be added since we're using the watchdog for low-power waiting
ISR(WDT_vect) { Sleepy::watchdogEvent(); }

void setup() {
    cli();
    CLKPR = bit(CLKPCE);
#if defined(__AVR_ATtiny84__)
    CLKPR = 0; // div 1, i.e. speed up to 8 MHz
#else
    CLKPR = 1; // div 2, i.e. slow down to 8 MHz
#endif
    sei();
    rf12_initialize(17, RF12_868MHZ, 5);
    // see http://tools.jeelabs.org/rfm12b
    rf12_config(0xC040); // set low-battery level to 2.2V i.s.o. 3.1V
}

void loop() {
    ++payload;
    
    while (!rf12_canSend())
        rf12_recvDone();
    
    rf12_sendStart(0, &payload, sizeof payload);
    // set the sync mode to 2 if the fuses are still the Arduino default
    // mode 3 (full powerdown) can only be used with 258 CK startup fuses
    rf12_sendWait(2);
    
    rf12_sleep(RF12_SLEEP);
    Sleepy::loseSomeTime(60000);
    rf12_sleep(RF12_WAKEUP);
}
