# rpi-temp
rpi-temp is a Raspberry-pi temperature sensor node with DS18B20 digital temperature sensor which uses Nagios check to monitor server rack ambient temperature. It is based on Rasbian OS and Raspberry pi 2B platform.

Implementation: a SysV init script (rpi_temp.sh) daemonizes the main Python3 script (rpi_temp.py) for ambient temperature data collection.  A remote Nagios check (check_rpitemp) will query the data collection file on a fixed interval and display the current temperature reading plus corresponding alert on the remote Nagios server dashboard. Alert types are OK, WARNING, CRITICAL which are based on temperature readings.

# Hardware Design & Configuration
The hardware components are a breadboard, 40-pin GPIO breakout board for Raspberry Pi, a DS18B20 digital temperature sensor, a 0.10mF capacitor, and jumper wires.

Three options of jumper wire connectivity could be used: 1.Pi Cobbler+ 40-pin GPIO breakout board.  2.T-Cobber Plus 40-pin GPIO breakout board.  3.Direct jumper wire connectivity between breadboard and Raspberry Pi GPIO.
Note: direct jumper wire connectivity is the lowest cost. Fritzing is used for breadboard diagram design.

**Breadboard diagram: Pi Cobbler+ 40-pin GPIO breakout board**
![rpi_temp_bb](https://user-images.githubusercontent.com/2264686/112409280-30c63f00-8d54-11eb-90dc-f979dd050f34.png)

**Breadboard diagram: T-Cobber Plus 40-pin GPIO breakout board**
![rpi_temp1_bb](https://user-images.githubusercontent.com/2264686/112409331-463b6900-8d54-11eb-8bbd-3974f30f13d4.png)

**Breadboard diagram: Direct jumper wire connectivity between breadboard and Raspberry Pi GPIO**  
![rpi_temp2_bb](https://user-images.githubusercontent.com/2264686/112410555-53f1ee00-8d56-11eb-9682-efa815be211a.png)






