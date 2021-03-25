## rpi-temp
rpi-temp is a Raspberry-pi temperature sensor node with DS18B20 digital temperature sensor which uses Nagios check to monitor server rack ambient temperature. It is based on Rasbian OS and Raspberry pi 2B platform.

Implementation: a SysV init script (rpi_temp.sh) daemonizes the main Python3 script (rpi_temp.py) for ambient temperature data collection.  A remote Nagios check (check_rpitemp) will query the data collection file on a fixed interval and display the current temperature reading plus corresponding alert on the remote Nagios server dashboard. Alert types are OK, WARNING, CRITICAL which are based on temperature readings.

## Hardware Design & Configuration
The hardware components are a breadboard, 40-pin GPIO breakout board for Raspberry Pi, a DS18B20 digital temperature sensor, a 0.10mF capacitor, and jumper wires.

Three options of jumper wire connectivity between Raspberry pi and DS18B20 could be implemented: 
1. Pi Cobbler+ 40-pin GPIO breakout board.  
2. T-Cobber Plus 40-pin GPIO breakout board.  
3. Direct jumper wire connectivity between breadboard and Raspberry Pi GPIO.

Note: direct jumper wire connectivity is the lowest cost. Fritzing is used for breadboard diagram design.

**Option 1: Pi Cobbler+ 40-pin GPIO breakout board**
![rpi_temp_bb](https://user-images.githubusercontent.com/2264686/112409280-30c63f00-8d54-11eb-90dc-f979dd050f34.png)

**Option 2: T-Cobber Plus 40-pin GPIO breakout board**
![rpi_temp1_bb](https://user-images.githubusercontent.com/2264686/112409331-463b6900-8d54-11eb-8bbd-3974f30f13d4.png)

**Option 3: Direct jumper wire connectivity between breadboard and Raspberry Pi GPIO**  
![rpi_temp2_bb](https://user-images.githubusercontent.com/2264686/112410555-53f1ee00-8d56-11eb-9682-efa815be211a.png)

## Hardware Testing
### Enabling required Linux kernel modules
The Linux kernel modules required to load are w1-gpio and w1-therm. The w1-gpio module registers and loads the new sensor connected to pin GPIO 4. The w1-therm module registers and loads a module that has support for temperature sensors.

To use the modules, enable them by adding the following line to /boot/config.txt with vim before rebooting your Pi.  Note this enables PIN4 as the default. Different pin could be used by adding the option gpiopin=N to the line.

`dtoverlay=w1-gpio`

Save file and then shut down the Raspberry Pi before wiring the sensor.

When modprobe loads these modules, the Raspberry Pi enables data collection on pin GPIO 4 and reads data from the sensor and stores it in a file. The file is named starting with 28 and followed by a unique file name.  The file contains the raw data read from the sensor.
```
pi@raspberrypi:~ $ cd /sys/bus/w1/devices/28-1a1970a57dff
pi@raspberrypi:/sys/bus/w1/devices/28-1a1970a57dff $ ls
driver  hwmon  id  name  power  subsystem  uevent  w1_slave
```
```
pi@raspberrypi:/sys/bus/w1/devices/28-1a1970a57dff $ cat w1_slave
3e 01 55 00 5f ff 0c 10 8b : crc=8d YES
3e 01 55 00 5f ff 0c 10 8b t=19365
```
## rpi_temp.py

This is the main script to 
- load the required Linux kernel modules (w1-gpio, w1-therm) which enable temperature data collection on pin GPIO 4, reading of raw data from the sensor and outputting the raw data to a system file (/sys/bus/w1/devices/28-1a1970a57dff);
- parses the raw data file and converts to degree Celsius temperature numerical integer value;
- outputs the temperature value with time stamp every 60s to a file (/tmp/temp.out) ;
- cleans up the GPIO pins when device is powered down

This file should to be placed in /home/pi/scripts/rpi_temp.py

## rpi_temp.sh

This is the SysV init script which daemonizes the main Python3 script (rpi_temp.py) everytime Raspberry pi boots up.  It shutdowns the main script when the device is powered down.

Installation:
```
$ sudo cp /home/pi/scripts/rpi_temp.sh /etc/init.d/rpi_temp
$ sudo chmod +x /etc/init.d/rpi_temp
$ sudo update-rc.d rpi_temp defaults
```

Usage:
```
$sudo service rpi_temp start
$sudo service rpi_temp stop
$sudo service rpi_temp status
```

## check_rpitemp

This is the Nagios check which runs via check_by_ssh plugin.  This allows the use ssh public keys to authenticate with a target device before running any commands.

On the Raspberry pi device, create a new UNIX user "nagios" and generate the corresponding ssh public keys.  Configure password-less ssh public key authentication
under nagios userid on both the Nagios server and the Raspberry pi.  Test and ensure password-less authentication works both ways.

On the Nagios server, check by running the check_by_ssh plugin to call one of the installed plugins on the Raspberry pi device.
```
$ /usr/local/nagios/libexec/check_by_ssh -H 192.168.1.100 -i /usr/local/nagios/keys/id_rsa  -C '/usr/local/nagios/libexec/check_load -w 15,10,5 -c 30,24,20'
OK - load average: 0.00, 0.00, 0.00|load1=0.000;15.000;30.000;0;
load5=0.000;10.000;24.000;0; load15=0.000;5.000;20.000;0;
```

Once check_by_ssh works, define the new command check_rpitemp to use it in /usr/local/nagios/etc/objects/commands.cfg:
```
define command {
    command_name  check_rpitemp
    command_line  /usr/local/nagios/libexec/check_by_ssh -H $HOSTADDRESS$ -i /usr/local/nagios/keys/id_rsa -C '/usr/local/nagios/libexec/check_rpitemp'
}
```

Apply that command to a new service check as follows, preferably placed beneath the host definition:
```
define service {
    use                  generic-service
    host_name            192.168.1.100
    service_description  RPITEMP_BY_SSH
    check_command        check_by_ssh!/usr/local/nagios/libexec/check_rpitemp 
}
```

Validate the configuration and restart the Nagios Core server:
```
#/usr/local/nagios/bin/nagios -v /usr/local/nagios/etc/nagios.cfg
#/etc/init.d/nagios restart
```














