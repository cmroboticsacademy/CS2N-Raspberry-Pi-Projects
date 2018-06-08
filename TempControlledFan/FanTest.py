#This script is to be used for testing the fan wiring to ensure it is working properly.

#Import statements
import RPi.GPIO as GPIO
import time
import sys

#Pin assignments for the breadboard
fanSignal = 21
offButton = 26

#This tells the Pi to use the broadcom pin-numbering scheme. GPIO numbers will now match up
#to how they appear on the breakout board.
GPIO.setmode(GPIO.BCM) 

#Sets the fanSignal and offButton pins to GPIO outputs and inputs, respectively.
GPIO.setup(fanSignal, GPIO.OUT) 
GPIO.setup(offButton, GPIO.IN)

#This is the main program loop. Every 3 seconds, the fan runs at full power, then turns off for 3.
#You will see very quickly if your fan is hooked up correctly through this script. The loop will
#run until the off button is held down. 
while (GPIO.input(offButton) == 0):		
	GPIO.output(21, GPIO.HIGH)
  	time.sleep(3)
	GPIO.output(21, GPIO.LOW)
	time.sleep(3)
     
#The GPIO.cleanup method clears out all pin assignments so they don't conflict with other scripts
#in the future.         
GPIO.cleanup()

#Program end
sys.exit()
