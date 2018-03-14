#!/usr/bin/env python3

# Modified & Programmed by Elliott Watson on 3/13/18:
# closely modeled on  Pero Krivić's script, but with different subprocess mechanics
# https://helentronica.com/2016/01/11/magic-mirror-with-motion-detector/
 
import sys
import time
import RPi.GPIO as io
import subprocess
 
io.setmode(io.BCM)
SHUTOFF_DELAY = 30  # seconds
PIR_PIN = 4         # pin 7 on the board

# commands to turn the monitor on and off
MONITOR_ON = ["vcgencmd", "display_power", "0"]
MONITOR_OFF = ["vcgencmd", "display_power", "1"]
 
def main():
    io.setup(PIR_PIN, io.IN)
    turned_off = False
    last_motion_time = time.time()
 
    while True:
        if io.input(PIR_PIN):
            print("motion detected")
            last_motion_time = time.time()
            sys.stdout.flush()
            if turned_off:
                turned_off = False
                turn_on()
        else:
            if not turned_off and time.time() > (last_motion_time + SHUTOFF_DELAY):
                print("time to sleep")
                turned_off = True
                turn_off()
        time.sleep(.1)
 
def turn_on():
    subprocess.call(MONITOR_ON)
 
def turn_off():
    subprocess.call(MONITOR_OFF)
 
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        io.cleanup()
