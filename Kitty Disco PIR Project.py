# Program to Animate the Kitty Disco
# Using a PIR Motion Sensor, Kitty LEDs and Dancing Cats
# with a Raspberry Pi

# Inspired by Paul McWhorter's Raspberry Pi Lesson #24

# Lori Pfahler
# January 2023

# load modules
import RPi.GPIO as GPIO
from time import sleep
from gpiozero import Servo

# setup board numbering system
GPIO.setmode(GPIO.BCM)

# output pin on PIR sensor connected to GPIO18 as an input
motionPin = 18
GPIO.setup(motionPin, GPIO.IN)

# setup the Kitty LEDs
GPIO.setup(6, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(26, GPIO.OUT)

# setup the servos
# import pigpio for hardware control of pulses to control servo
# reduce jitter from software control of pulses
# in terminal window issue this command (sudo pigpiod) before running
# to make sure pigpio server is running in the background
from gpiozero.pins.pigpio import PiGPIOFactory
myFactory = PiGPIOFactory()

# servos on pins 23 and 24
myServo1 = Servo(23, min_pulse_width = 0.5/1000, max_pulse_width = 2.5/1000,
                pin_factory=myFactory)
myServo2 = Servo(24, min_pulse_width = 0.5/1000, max_pulse_width = 2.5/1000,
                pin_factory=myFactory)

# allow sensor to initialize
sleep(10)

try:
# where the action happens    
    while True:
        motion = GPIO.input(motionPin)
        print(motion)
        if motion == 1:
            print("Kitty Disco!")
            # Turn on the Kitty LEDs
            GPIO.output(6, True)
            GPIO.output(13, True)
            GPIO.output(26, True)
            # Dance Round 1
            myServo1.mid()
            myServo2.mid()
            sleep(1)
            myServo1.min()
            myServo2.max()
            sleep(1)
            myServo1.max()
            myServo2.min()
            sleep(1)
            # Dance Round 2
            myServo1.mid()
            myServo2.mid()
            sleep(1)
            myServo1.min()
            myServo2.max()
            sleep(1)
            myServo1.max()
            myServo2.min()
            sleep(1)
            # End the Dance in the Middle
            myServo1.mid()
            myServo2.mid()
            # Rest
            sleep(5)
            # Turn off the Kitty LEDs
            GPIO.output(6, False)
            GPIO.output(13, False)
            GPIO.output(26, False)
            print("Time to Rest!")
        sleep(0.1)

except KeyboardInterrupt:
    # turn off LEDs
    GPIO.output(6, 0)
    GPIO.output(13, 0)
    GPIO.output(26, 0)
    myServo1.value = None
    myServo2.value = None
    GPIO.cleanup()

