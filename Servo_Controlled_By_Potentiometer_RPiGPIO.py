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
import RPi.GPIO as GPIO
from time import sleep
from smbus import SMBus
GPIO.setmode(GPIO.BCM)

# set delay time
delayTime = 0.1

# setup servo
ServoPin = 26
GPIO.setup(ServoPin, GPIO.OUT)

# pwm object using frequency of 50 Hz
pwmServo=GPIO.PWM(ServoPin, 50)
# start pwm object at Duty Cycle of zero
pwmServo.start(0)

# functions for ADS7830
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
      slope = 10/255
      intercept = 2
if userScale == 'Blue':
      slope = -10/255
      intercept = 12
    
try:
    while True:
        # Read potentiometer from channel 0
        potValue = read_ads7830(0)
        DC = slope*potValue + intercept
        pwmServo.ChangeDutyCycle(DC)
        if userScale == 'Blue':
            angle = -18*DC + 216
            print('BLUE SCALE: potValue =', potValue, '| DC =', round(DC, 0),
                  '| Angle =', round(angle, 0))
        if userScale == 'Yellow':
            angle = 18*DC - 36
            print('YELLOW SCALE: potValue =', potValue, '| DC =', round(DC, 0),
                  '| Angle =', round(angle, 0))
        sleep(delayTime)

except KeyboardInterrupt:
    pwmServo.stop()
    GPIO.cleanup()