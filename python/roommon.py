#!/usr/bin/python
#
# Receive data from a JEEnode on the 915mhz network and if someone
# trips the alarm, send me a text.
#
# requires pyserial
#
# J. Adams <jna@retina.net>
# May, 2012
#

import os
import sys
import serial
import re
import syslog
import time

# config
SERIAL_PORT="/dev/tty.usbserial-FTFAYG4O"
BAUD=57600
# if you set this to your email addres, you'll get a mail when motion occurs
#EMAIL="xxxxxxxxxx@text.att.net"
DEBUG=False

# If we alarm, do not alarm again for these many seconds
ALARMWINDOW=90

# Timeout = 0 means block forever. We'll just loop. 
ser = serial.Serial(SERIAL_PORT, BAUD, timeout = 2)

buffer = ''
last_trigger = 0  


def handle_motion():
    """ fired when motion occurs """
    global last_trigger

    print "ALARM at: %d last: %d" % (last_trigger, time.time())

    # eliminate hystersis
    if last_trigger != 0:
        if ((time.time() - last_trigger) < ALARMWINDOW):
            last_trigger = time.time()
            return 

    last_trigger = time.time()

    syslog.syslog(syslog.LOG_NOTICE, "PIR Motion detected")
    if DEBUG:
        print "Motion"

    if 'EMAIL' in globals(): 
      os.system("echo Motion | /usr/bin/mail -s \"ALARM: Motion Detected\" %s" % EMAIL)


# Main Loop
while (True):
    buffer = buffer + ser.read(ser.inWaiting())
    if '\n' in buffer:
        if DEBUG:
            print "***%s***" %  buffer
        m = re.search("OK (\d+) (\d+) (\d+) (\d+)",buffer, re.MULTILINE)
        if m != None:
            if m.group(3) == "1":
                handle_motion()
            else:
                if m.group(3) == "0":
                    syslog.syslog(syslog.LOG_NOTICE, "RoomNode Heartbeat OK")
        buffer = ""
        pass
    else:
        buffer += ser.read(1)
