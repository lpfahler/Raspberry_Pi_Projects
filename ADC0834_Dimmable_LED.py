# A program to use an potentiometer to dim an LED on a raspberry pi.
# Inspired by Lesson 15 in the Raspberry Pi Tutorials by Paul McWhorter.
# This program will use an analog to digital converter to read the signal
# from the potentiometer.  This version will use the ADC083, an ADC chip from
# the Sunfounder Kit for the Raspberry Pi

# A driver (python module - ADC0834.py) was included with the code from the kit
# This was placed in /usr/lib/python3.9 directory.

# I will incorporate a nonlinear scale for increasing or decreasing
# the brightness so that turning the potentiometer appears to create a
# linear change in perceived brightness.

# Lori Pfahler
# August 2022

# import modules and setup GPIO pins
import RPi.GPIO as GPIO
import ADC0834
from time import sleep

# Use BCM pin numbers since extender board and ADC0834 module use BCM
GPIO.setmode(GPIO.BCM)
ADC0834.setup()
delayTime = 0.1

# Setup LED
LEDPin = 16
GPIO.setup(LEDPin, GPIO.OUT)
LEDDutyCycle = 0
# create Pulse Width Modulation object with frequency of 100
LEDPWM = GPIO.PWM(LEDPin, 1000)
LEDPWM.start(LEDDutyCycle)

# Let user choose whether to change duty cycle linearly or nonlinearly
# when adjusting the potentiometer
changeType = int(input('Enter 1 for Linear Change OR 2 for Nonlinear Change: '))


# where the action happens
try:
    while True:
        # Read analog signal from channel 0
        analogValue = ADC0834.getResult(0)
        
        # scale to analogValue (0-255) to duty cycle range (1-100) linearly
        if changeType == 1:
            LEDDutyCycle = (100/255)*analogValue
            LEDPWM.ChangeDutyCycle(LEDDutyCycle)
        
        # using a nonlinear scale duty cycle = a**analogValue where
        # max(analogValue) is 255 since preceived brightness of LED varies
        # nonlinearly.  We need to find "a" in equation.  When duty cycle is 100,
        # analogValue should be 255 (the max).  Equation becomes
        # 100 = a**255 or a = 100**(1/255) a = 1.01822355
        if changeType == 2:
            LEDDutyCycle = 1.01822355**analogValue
        # catch if LEDValue gets close to 100 or zero
            if LEDDutyCycle >= 99:
                LEDDutyCycle = 100
            if LEDDutyCycle <= 1:
                LEDDutyCycle = 0
            LEDPWM.ChangeDutyCycle(LEDDutyCycle)
            
        print(analogValue, LEDDutyCycle)            
        # short delay    
        sleep(delayTime)
        
except KeyboardInterrupt:
    LEDPWM.stop()
    GPIO.cleanup()
