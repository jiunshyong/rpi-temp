# rpi-temp
rpi-temp is a Raspberry-pi temperature sensor node with DS18B20 digital temperature sensor which uses Nagios check to monitor server rack ambient temperature. It is based on Rasbian OS and Raspberry pi 2B platform.

Current implementation: a SysV init script (rpi_temp.sh) daemonizes the main Python3 script (rpi_temp.py) for ambient temperature data collection.  A remote Nagios check (check_rpitemp) will query the data collection file on a fixed interval and display the current temperature reading plus corresponding alert on the remote Nagios server dashboard. Alert types are OK, WARNING, CRITICAL which are based on temperature readings.

# Hardware Design & Configuration
The hardware components are a breadboard, GPIO Breakout Board for Raspberry Pi, a DS18B20 digital temperature sensor, a 0.10mF capacitor, and jumper wires.






