# Program to use a PIR Motion Sensor with a Raspberry Pi
# From McWhorter's Raspberry Pi Lesson #24
# Lori Pfahler
# January 2023

# load modules
import RPi.GPIO as GPIO
from time import sleep


# setup board numbering system
GPIO.setmode(GPIO.BCM)

# output pin on PIR sensor connected to GPIO18 as an input
motionPin = 18
GPIO.setup(motionPin, GPIO.IN)

# allow sensor to initialize
sleep(10)

try:
# where the action happens    
    while True:
        motion = GPIO.input(motionPin)
        print(motion)
        sleep(0.1)
    
except KeyboardInterrupt:
    GPIO.cleanup()


