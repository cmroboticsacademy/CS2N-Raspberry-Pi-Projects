#This script will control an LED strip and vary the intensity of the LED 
#strip based upon the measured ambient light in a room. 

#Import statements
import RPi.GPIO as GPIO
import time
from gpiozero import LightSensor
import sys

#Pin assignments for the breadboard
signal = 21
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

#DC, or duty cycle, is a percentage that determines how much of a pulse in a pwm
#signal is powered (i.e. on vs off). This value is what changes the intensity of
#the lights, as a dc of 0 means they are 100% off all the time, and a dc of 100 
#means they are on all the time at full power. DC must be between 0 and 100. As 
#is a an increment value that is either 1 or -1 depending on whether the LEDs are
#getting brighter or dimmer. It is used in the loop below.
dc = 0
change = 1

#The LED switch is started with a dc of 0. This means that the lights will be off,
#but the puslses have started at the specified frequency. Once dc is above 0, the 
#physical transistor will begin switching on and off rapidly.
LED.start(dc)

#This loop tests the LEDs for by dimming them up and down contiuously. It runs until 
#the off button is held down. 
while (GPIO.input(offButton) == 0):
    if(dc <= 99 and change == 1):
        change = 1
    else:
	change = -1
        if(dc >= 1 and change == -1):
            change = -1
	else:
            change = 1
    dc = dc + change
	#This new dc value is fed into the LED switch to change its intensity. The loop runs every
	#.05 seconds, so the LEDs quickly dim or brighten to the level they are supposed to be at.
    LED.ChangeDutyCycle(dc)
    time.sleep(.05)

#Everything is cleaned up and the program is ended.
LED.stop()    
GPIO.output(signal,0)
GPIO.cleanup()
sys.exit()

