#This script will test the photresistor to ensure it is displaying readings
#properly before the rest of the project is completed.

#Import statements
import RPi.GPIO as GPIO
import time
from gpiozero import LightSensor
import sys

#Pin assignments for the breadboard
sensor = 19
offButton = 26

#This tells the Pi to use the broadcom pin-numbering scheme. GPIO numbers will 
#now match up to how they appear on the breakout board.
GPIO.setmode(GPIO.BCM) 

#The light sensor line and off button are configured as outputs and inputs,
#respectively
GPIO.setup(offButton, GPIO.IN)

#Light is declared as LightSensor object, so it will now have methods that can
#easily called to get the ambient light values in the room.
light = LightSensor(sensor)

#This loop refreshes the light sensor every second. It runs until the off
#button is held down. 
while (GPIO.input(offButton) == 0):
	#The raw light level is retrieved from the light object. It will range from 0
	#to 1, with 1 being the brightest.
    lightLevel = light.value
    print(lightLevel)
    time.sleep(1)

#Everything is cleaned up and the program is ended.
light.close()
GPIO.cleanup()
sys.exit()

