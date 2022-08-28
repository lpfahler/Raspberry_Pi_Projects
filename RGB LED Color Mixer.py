# A program to use three potentiometers to control an RGB LED on a raspberry pi.
# A potentiometer for each color: Red, Green and Blue
# Inspired by the Raspberry Pi Tutorials by Paul McWhorter. HW was given in
# Lesson 16 and his solution provided in Lesson 17.

# This program will use an analog to digital converter to read the signal
# from the potentiometers.  This version will use the ADS7830, an ADC chip from
# the Freenove Kit for the Raspberry Pi

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
# From M Heidenreich code and youtube video on ADC ADS7830
# use 'i2cdetect -y 1' in terminal - must enable I2C protocol on raspberry pi

def read_ads7830(input):
    bus.write_byte(0x4b, ads7830_commands[input])
    return bus.read_byte(0x4b)

# Use BCM pin numbers since extender board is labeled in BCM
GPIO.setmode(GPIO.BCM)
delayTime = 0.5

# start an SMBus object
bus = SMBus(1)

# Setup red, green and blue pins for the RGB LED
redPin = 25
greenPin = 12
bluePin = 16
GPIO.setup(redPin, GPIO.OUT)
GPIO.setup(greenPin, GPIO.OUT)
GPIO.setup(bluePin, GPIO.OUT)

# create Pulse Width Modulation objects with frequency of 1000
redPWM = GPIO.PWM(redPin, 1000)
greenPWM = GPIO.PWM(greenPin, 1000)
bluePWM = GPIO.PWM(bluePin, 1000)

# Create variables to hold the current duty cycles for each color
# initalize the PWM objects and start at OFF
redDC = 0
greenDC = 0
blueDC = 0
redPWM.start(redDC)
greenPWM.start(greenDC)
bluePWM.start(blueDC)


# where the action happens
try:
    while True:
        # Read red signal from channel 0
        redAV = read_ads7830(0)
        # Read green signal from channel 1
        greenAV = read_ads7830(1)       
        # Read blue signal from channel 2
        blueAV = read_ads7830(2)  

        # red
        # scale to analogValue (0-255) to duty cycle range (1-100) linearly
        # included linear change equations as comments
        # redDC = (100/255)*redAV
        
        # using a nonlinear scale duty cycle = a**analogValue where
        # max(analogValue) is 255 since preceived brightness of LED varies
        # nonlinearly.  We need to find "a" in equation.  When duty cycle is 100,
        # analogValue should be 255 (the max).  Equation becomes
        # 100 = a**255 or a = 100**(1/255) a = 1.01822355
        redDC = 1.01822355**redAV
        if redDC >= 99:
            redDC = 100
        if redDC <= 1:
            redDC = 0
        redPWM.ChangeDutyCycle(redDC)
        # green
        # greenDC = (100/255)*greenAV
        greenDC = 1.01822355**greenAV
        if greenDC >= 99:
            greenDC = 100
        if greenDC <= 1:
            greenDC = 0
        greenPWM.ChangeDutyCycle(greenDC)
        # blue
        # blueDC = (100/255)*blueAV
        blueDC = 1.01822355**blueAV
        if blueDC >= 99:
            blueDC = 100
        if blueDC <= 1:
            blueDC = 0
        bluePWM.ChangeDutyCycle(blueDC)
        print("AV, DC (red, green, blue): ", 
              redAV, round(redDC), "|",
              greenAV, round(greenDC), "|",
              blueAV, round(blueDC))

        # short delay    
        sleep(delayTime)
        
except KeyboardInterrupt:
    # make sure all colors are turned off
    redPWM.stop()
    greenPWM.stop()
    bluePWM.stop()
    # cleanup
    GPIO.cleanup()
