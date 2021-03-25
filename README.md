# rpi-temp
rpi-temp is a Raspberry-pi temperature sensor node with DS18B20 digital temperature sensor which uses Nagios check to monitor server rack ambient temperature. It is based on Rasbian OS and Raspberry pi 2B platform.

Current implementation: a SysV init script (rpi_temp.sh) daemonizes the main Python3 script (rpi_temp.py) for ambient temperature data collection.  A remote Nagios check (check_rpitemp) will query the data collection file on a fixed interval and display the current temperature reading plus corresponding alert on the remote Nagios server dashboard. Alert types are OK, WARNING, CRITICAL which are based on temperature readings.

# Hardware Design & Configuration
The hardware components are a breadboard, GPIO Breakout Board for Raspberry Pi, a DS18B20 digital temperature sensor, a 0.10mF capacitor, and jumper wires.


![rpi_temp_bb](https://user-images.githubusercontent.com/2264686/112409280-30c63f00-8d54-11eb-90dc-f979dd050f34.png)

![rpi_temp1_bb](https://user-images.githubusercontent.com/2264686/112409331-463b6900-8d54-11eb-8bbd-3974f30f13d4.png)

![rpi_temp_bb](https://user-images.githubusercontent.com/2264686/112409337-489dc300-8d54-11eb-98fe-e17295b4a5b5.png)





