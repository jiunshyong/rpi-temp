#!/usr/bin/python3
# Print temperature in Celsius every 60s to /tmp/temp.out with cronjob scheduled every hour to empty the output file.  Version: 0.1.0 
# Should be configured  as init script to start everytime device is booted up.
# Import Python modules. 
import glob
import os
import time
import sys
import datetime

now = datetime.datetime.now()

# Issue modprobe command to initialize the GPIO & temperature sensor kernel modules.
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

# Use glob to search the file system for files that match the prefix.
base_dir = '/sys/bus/w1/devices/'
# Save the directory to the file.
datadir = glob.glob(base_dir + '28*')[0]
# Create the full path to the file
datafile = datadir + '/w1_slave'

# Procedure for reading the raw data from the file.  Open the file and read all of the lines then close it.
def read_data():
    f = open(datafile, 'r')
    lines = f.readlines()
    f.close()
    return lines
    
# Read the temperature and return the values found.
def get_temp():
    # Initialize the variables.
    temp_c = None   
    lines = read_data()
    
    # If the end of the first line ends with something other than 'YES', try reading the file again until 'YES' is found.
    while not lines[0].strip().endswith('YES'):
        time.sleep(0.25)
        lines = read_data()

    # Search the second line for the data prefixed with 't='
    pos = lines[1].find('t=')
          
    # A return code of -1 means it is not found.
    if pos != -1:
    
        # Get the raw data located after the 't=' until the end of the line.
        temp_string = lines[1][pos+2:]
        
        # Convert temperature value into 2-digit integer
        temp_c = float(temp_string) / 1000.00       
        temp_c = int(temp_c)        
        
    # Return the values read
    return temp_c
    
# Main loop. Print data to output file then sleep 60s until process is terminated manually or device is rebooted or powered down.
while True:
    temp_c = get_temp()
    with open("/tmp/temp.out", 'a') as f:
        print(str(now), end=" ", file=f)
        print("Temperature is {0} degrees Celsius, ".format(temp_c), file=f)          
time.sleep(60)

def cleanup_pins():
    "cleanup the GPIO pins"
    print("[" + get_now() + "] cleaning up pins!")
    GPIO.cleanup()

def sigterm_handler(_signo, _stack_frame):
    "When sysvinit sends the TERM signal, cleanup before exiting."
    print("[" + get_now() + "] received signal {}, exiting...".format(_signo))
    cleanup_pins()
    sys.exit(0)

signal.signal(signal.SIGTERM, sigterm_handler)
