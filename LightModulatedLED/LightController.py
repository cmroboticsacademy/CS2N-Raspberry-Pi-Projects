#This script will control an LED strip and vary the intensity of the LED 
#strip based upon the measured ambient light in a room. 

#Import statements
import RPi.GPIO as GPIO
import time
from gpiozero import LightSensor
import sys

#Pin assignments for the breadboard
signal = 21
sensor = 19
offButton = 26

#This tells the Pi to use the broadcom pin-numbering scheme. GPIO numbers will 
#now match up to how they appear on the breakout board.
GPIO.setmode(GPIO.BCM) 

#The light sensor line and off button are configured as outputs and inputs,
#respectively.
GPIO.setup(signal, GPIO.OUT)
GPIO.setup(offButton, GPIO.IN)

#Starts the control pwm signal, called LED, at 150 hz frequency. This may seem 
#low for a pwm signal, but for LED lights higher frequencies have no visible 
#effect on the lighting.
LED = GPIO.PWM(signal, 150) 

#Light is declared as LightSensor object, so it will now have methods that can
#easily called to get the ambient light values in the room.
light = LightSensor(sensor)

#DC, or duty cycle, is a percentage that determines how much of a pulse in a pwm
#signal is powered (i.e. on vs off). This value is what changes the intensity of
#the lights, as a dc of 0 means they are 100% off all the time, and a dc of 100 
#means they are on all the time at full power. DC must be between 0 and 100.
dc = 0

#The LED switch is started with a dc of 0. This means that the lights will be off,
#but the puslses have started at the specified frequency. Once dc is above 0, the 
#physical transistor will begin switching on and off rapidly.
LED.start(dc)

#This loop provides the continous dimming control that enables the LED lights to
#match intensity to the measured light in the environment. It runs until the off
#button is held down. 
while (GPIO.input(offButton) == 0):
	#The raw light level is retrieved from the light object. It will range from 0
	#to 1, with 1 being the brightest.
    lightLevel = light.value
	
	#We want the lights to be bright whenever the environment is measured as dark, so
	#the measured light level must be subtracted from 1 to get a "target" light level.
	#This value is then multipled by 100 to give a target dc value. Ex. Measured light
	#is at .3, this code will convert that number to a target dc light level of 70%.
    lightLevel = 1 - lightLevel
    lightLevel = lightLevel * 100

	#If the target light level is below 20%, this if statement scales it exponentially 
	#downward to a lower level by taking the 1/4 root of the original value. This is done
	#to help make the lights dimmer indoors because the light sensor usually doesn't get
	#above 90 indoors.
    if(lightLevel < 20):
        lightLevel = lightLevel ** (.25)
    
	#If the current duty cycle is below the target light level, then the dc value is 
	#increased slightly, otherwise it is decreased slightly when it is measured as higher
	#than the target level.
    if(((dc - lightLevel) <= -1) and dc <= 99):
        dc = dc + 1
    else:
        if(((dc - lightLevel) >= 1) and dc >= 1):
            dc = dc - 1
	#This new dc value is fed into the LED switch to change its intensity. The loop runs every
	#.05 seconds, so the LEDs quickly dim or brighten to the level they are supposed to be at.
    LED.ChangeDutyCycle(dc)
    time.sleep(.05)

#Everything is cleaned up and the program is ended.
LED.stop()
light.close()
GPIO.output(signal,0)
GPIO.cleanup()
sys.exit()

