# Python program to blink five LEDs as a binary counter from zero to 31
# Inspired by Paul McWhorter's Raspberry Pi Lesson 5
# Add in an OLED display to show the binary numbers
# Lori Pfahler
# August 2022

# import libraries
import RPi.GPIO as GPIO
from time import sleep
# libraries to use OLED display
from board import SCL, SDA
import busio
# from https://pypi.org/project/oled-text/
# easy to use oled text library
from oled_text import OledText, Layout64, BigLine, SmallLine

# setup board numbering system and GPIO pins for LEDs
# use GPIO pins 7, 12, 16, 20, 21
GPIO.setmode(GPIO.BCM)
GPIO.setup(7, GPIO.OUT)
GPIO.setup(12, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(20, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)

delayTime = 1

# Create the display, pass its pixel dimensions
i2c = busio.I2C(SCL, SDA)
oled = OledText(i2c, 128, 64)

# A panel with 3 lines and 3 icons to the right
# only using first line for this program
oled.layout = Layout64.layout_3medium_3icons()
oled.auto_show = True

try:
    while True:
        for x in range(0, 32, 1):
            # use format function to convert x to binary with five digits
            binString = format(x, '05b')
            # print binary to screen for verification
            print(binString)
            # send binary number to OLED display
            oled.text(binString, 1)
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
            sleep(delayTime) 

except KeyboardInterrupt:
    #  turn off LEDs
    GPIO.output(7, 0)
    GPIO.output(12, 0)
    GPIO.output(16, 0)
    GPIO.output(20, 0)
    GPIO.output(21, 0)
    # clear OLED display
    oled.text("", 1)
    # clear GPIO settings
    GPIO.cleanup()
