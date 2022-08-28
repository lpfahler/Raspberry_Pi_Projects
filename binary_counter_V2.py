# Python program to blink five LEDs as a binary counter from zero to 31
# Lori Pfahler
# August 2022

# import libraries and setup GPIO pins 7, 12, 16, 20, 21
import RPi.GPIO as GPIO
import time

# setup board numbering system and GPIO pins for LEDs
GPIO.setmode(GPIO.BCM)
GPIO.setup(7, GPIO.OUT)
GPIO.setup(12, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(20, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)

delayTime = 1

try:
    while True:
        for x in range(0, 32, 1):
            # use format function to convert x to binary with five digits
            binString = format(x, '05b')
            # print binary to screen for verification
            print(binString)
            # separate out digits to each pin variable - make these integers
            pin7 = int(binString[0])
            pin12 = int(binString[1])
            pin16 = int(binString[2])
            pin20 = int(binString[3])
            pin21 = int(binString[4])
            # light up  the LEDS according to the binary representation
            GPIO.output(7, pin7)
            GPIO.output(12, pin12)
            GPIO.output(16, pin16)
            GPIO.output(20, pin20)
            GPIO.output(21, pin21)
            # allow a delay to see the counting
            time.sleep(delayTime) 

except KeyboardInterrupt:
    #  turn off LEDs
    GPIO.output(7, 0)
    GPIO.output(12, 0)
    GPIO.output(16, 0)
    GPIO.output(20, 0)
    GPIO.output(21, 0)
    # clear GPIO settings
    GPIO.cleanup()
