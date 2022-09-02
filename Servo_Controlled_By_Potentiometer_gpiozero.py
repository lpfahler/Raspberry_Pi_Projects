# A program to control a servo on a Raspberry Pi with a potentiometer.
# You must first calibrate your servo to know what duty cycle will
# produce a zero degree angle (1-2 %) and what duty cycle will
# produce a 180 degree angle (10-15%).
# My servo is 2% for 0 degrees and 12% for 180 degrees.

# Inspired by Lesson 20 in the Raspberry Pi Tutorials
# by Paul McWhorter.


# Lori Pfahler
# August 2022

# import modules and setup GPIO pin number to BCM
# import RPi.GPIO as GPIO
from time import sleep
from smbus import SMBus
from gpiozero import Servo 

# import pigpio for hardware control of pulses to control servo
# reduce jitter from software control of pulses
# in terminal window issue this command (sudo pigpiod) before running
# to make sure pigpio server is running in the background
# From "Gary Explains" on YouTube:
# 'Raspberry Pi Servo Motor Control - No Jitter!'

from gpiozero.pins.pigpio import PiGPIOFactory
myFactory = PiGPIOFactory()

# set delay time
delayTime = 0.05

# setup servo on pin 26 set min (0.5 msec) and max pulse (2.5 msec) width to use full range
myServo = Servo(26, min_pulse_width = 0.5/1000, max_pulse_width = 2.5/1000,
                pin_factory=myFactory)
# start at 90 degrees
myServo.value = 0

# functions for ADS7830 - Analog to Digital Convertor board
# list of addresses for the eight channels on the ADS7830
ads7830_commands = (0x84, 0xc4, 0x94, 0xd4, 0xa4, 0xe4, 0xb4, 0xf4)

# function to read from ADS7830
# From M Heidenreich code and youtube video on ADC ADS7830
def read_ads7830(input):
    bus.write_byte(0x4b, ads7830_commands[input])
    return bus.read_byte(0x4b)

# start an SMBus object
bus = SMBus(1)

# ask user for desired scale
print('Enter desired scale direction.  Yellow = 0 deg to the right and 180 deg left')
print('OR Blue = 0 deg to the left and 180 deg right')
userScale = input('Enter desired scale direction (Yellow OR Blue): ')
while userScale != 'Yellow' and userScale != 'Blue':
    print('You must enter Yellow or Blue.')
    userScale = input('Enter desired scale direction (Yellow OR Blue): ')
if userScale == 'Yellow':
      slope = 2/255
      intercept = -1
if userScale == 'Blue':
      slope = -2/255
      intercept = 1

# where the action happens
try:
    while True:
        # Read potentiometer from channel 0
        potValue = read_ads7830(0)
        servoValue = slope*potValue + intercept
        # pwmServo.ChangeDutyCycle(DC)
        myServo.value = servoValue
        if userScale == 'Blue':
            angle = -90*servoValue + 90
            print('BLUE SCALE: potValue =', potValue, '| servoValue =',
                  round(servoValue, 1), '| angle =', round(angle, 0))
        if userScale == 'Yellow':
            angle = 90*servoValue + 90
            print('YELLOW SCALE: potValue =', potValue, '| servoValue =',
                  round(servoValue, 1), '| angle =', round(angle, 0))
        sleep(delayTime)

except KeyboardInterrupt:
    myServo.value = None