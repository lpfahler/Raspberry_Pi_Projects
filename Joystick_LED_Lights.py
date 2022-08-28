# A program to use joystick to light some LEDs on a raspberry pi.  The LEDs
# are arranged in a cross pattern.  Moving the joystick will light the LED in
# that direction as shown below (y1, y2, x1 or x2LED)

#                      y1LED(yellow)
#
#        x1LED(blue)  middleLED(red)   x2LED(blue)
#
#                      y2LED(yellow)

# middleLED will start on and pressing the button on the joystick
# will switch the middleLED status (ON vs OFF)

# This program will use an analog to digital converter to read the signal
# from the potentiometers in the joystick.
# This version will use the ADS7830, an ADC chip from
# the Freenove Kit for the Raspberry Pi.  It uses the I2C protocol.

# Lori Pfahler
# August 2022

# import modules and setup GPIO pins
import RPi.GPIO as GPIO
from time import sleep
from smbus import SMBus

# functions for ADS7830
# list of addresses for the eight channels on the ADS7830
ads7830_commands = (0x84, 0xc4, 0x94, 0xd4, 0xa4, 0xe4, 0xb4, 0xf4)

# function to read from ADS7830
# From M Heidenreich code and youtube video on ADS7830
def read_ads7830(input):
    bus.write_byte(0x4b, ads7830_commands[input])
    return bus.read_byte(0x4b)

# Use BCM pin numbers since extender board is labeled in BCM
GPIO.setmode(GPIO.BCM)
delayTime = 0.1

# start an SMBus object
bus = SMBus(1)

# Setup the GPIO pin for the button on the joystick
buttonPin = 26
GPIO.setup(buttonPin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
# variable to keep track of the button value from the previous loop
buttonPrevious = 1
# variable to keep track of whether the middleLED is on or off
middleLEDState = True



# Setup the LED pins
x1LED = 18
x2LED = 24
y1LED = 23
y2LED = 12
middleLED = 25
GPIO.setup(x1LED, GPIO.OUT)
GPIO.setup(x2LED, GPIO.OUT)
GPIO.setup(y1LED, GPIO.OUT)
GPIO.setup(y2LED, GPIO.OUT)
GPIO.setup(middleLED, GPIO.OUT)

# turn middleLED on
GPIO.output(middleLED, True)

# where all the action happens
try:
    while True:
        # Read x signal from channel 0
        xAV = read_ads7830(0)
        # Read y signal from channel 1
        yAV = read_ads7830(1)

        # x joystick direction
        if xAV < 25:
            GPIO.output(x1LED, True)
            GPIO.output(x2LED, False)
        elif xAV > 230:
            GPIO.output(x2LED, True)
            GPIO.output(x1LED, False)
        else:
            GPIO.output(x1LED, False)
            GPIO.output(x2LED, False)
            
        # y joystick direction
        if yAV < 25:
            GPIO.output(y1LED, True)
            GPIO.output(y2LED, False)
        elif yAV > 230:
            GPIO.output(y2LED, True)
            GPIO.output(y1LED, False)
        else:
            GPIO.output(y1LED, False)
            GPIO.output(y2LED, False)
            
        # button toggle
        # read the button
        buttonCurrent = GPIO.input(buttonPin)
        # below is the state of the two variables that indicates the
        # button has been pressed AND let go of
        if (buttonPrevious==0 and buttonCurrent==1):
            # determine if the LED is currently on or off
            # switch LEDState to True or False for next button push
            if middleLEDState==False:
                GPIO.output(middleLED, True)
                middleLEDState=True
            else:
                GPIO.output(middleLED, False)
                middleLEDState=False
        # reset buttonPrevious to buttonCurrent for the next loop
        buttonPrevious = buttonCurrent
        
        # print out values
        print('X, Y and Button Values: ', xAV, yAV, buttonCurrent)
        sleep(delayTime)
        
except KeyboardInterrupt:
    GPIO.cleanup()

