jeenode-roommon
===============

JeeNode based room monitor using IR motion sensor and JeeNodes (written in Processing)

This software assumes that you have a pair of jeenodes, available from:
http://shop.moderndevice.com/products/jeenode-kit ($22) 

Find a way to power them, I use a 1800mAh battery on the roomnode ,
which I estimate will give me over a year of operations. The other
node is FTDI cable powered.

With the RF12 sensors, and a Parallex IR sensor, available from Parallax:
http://www.parallax.com/tabid/768/ProductID/83/Default.aspx ($20-25)

Obviously, you also need an FTDI cable for programming: 
https://www.adafruit.com/products/70 ($20) 

Solder and build both jeenodes. (beyond the scope of this document)

Using the Arduino software: 

1. Upload roomNode to one JeeNode. Wire the PIR sensor into it (see schematic)
2. Upload the RF12demo example to the other device
3. Plug the RF12demo jeenode into your machine via FTDI cables
4. Install pyserial on your machine.
5. Serial console into the RF12 device, make sure it works.
6. Edit roommon.py. Add your email address if you wish (it will just syslog otherwise)
7. Write an init script or whatever to keep the monitor running.
8. Profit. I use this thing to monitor my cats, my housekeeper, and pet
care takers to see if they're coming to do their job, etc.