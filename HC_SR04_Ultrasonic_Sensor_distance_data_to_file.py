# A program to use HC-SR04 Ultrasonic Sensor.
# Determine the distance to a target in cm - used for experimentation
# to determine performance of sensor
# Measure a specific number of distances - user input
# Write data to a file: data.txt

# Lori Pfahler
# December 2022

# load modules
import RPi.GPIO as GPIO
import time
# board numbering system to use
GPIO.setmode(GPIO.BCM)

# variable to hold a short delay time
delayTime = 0.2

# setup trigger and echo pins
trigPin = 23
echoPin = 24
GPIO.setup(trigPin, GPIO.OUT)
GPIO.setup(echoPin, GPIO.IN)

# ask user for number of replicate distances and short description of run
numReadings = int(input('Enter number of distance readings desired: '))
runText = input('Enter Short Description of Run Parameters: ')
# print to file
print('n =', numReadings, runText, file = open('data.txt', 'a'))


# start loop to measure distances
for i in range(0,numReadings,1):
    # start the pulse to get the sensor to send the ping
    # set trigger pin low for 2 micro seconds
    GPIO.output(trigPin, 0)
    time.sleep(2E-6)
    # set trigger pin high for 10 micro seconds
    GPIO.output(trigPin, 1)
    time.sleep(10E-6)
    # go back to zero - communication compete to send ping
    GPIO.output(trigPin, 0)
    # now need to wait till echo pin goes high to start the timer
    # this means the ping has been sent
    while GPIO.input(echoPin) == 0:
        pass
    # start the time - use system time
    echoStartTime = time.time()
    # wait for echo pin to go down to zero
    while GPIO.input(echoPin) == 1:
        pass
    echoStopTime = time.time()
    # calculate ping travel time
    pingTravelTime = echoStopTime - echoStartTime
    # Use the time to calculate the distance to the target.
    # speed of sound at 72 deg F is 344.44 m/s
    # from weather.gov/epz/wxcalc_speedofsound.
    # equations used by calculator at website above.
    # speed of sound = 643.855*((temp_in_kelvin/273.15)^0.5)
    # temp_in_kelvin = ((5/9)*(temp_in_F - 273.15)) + 32
    #
    # divide in half since the time of travel is out and back
    dist_cm = (pingTravelTime*34444)/2
    # print data to shell and to the file
    print(round(dist_cm, 3))
    print(round(dist_cm, 3), file = open('data.txt', 'a'))
    # sleep to slow things down
    time.sleep(delayTime)
GPIO.cleanup()

