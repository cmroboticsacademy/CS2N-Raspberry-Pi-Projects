#This script will control a strand of LED lights, matching the pulse rate of the
#lights to that of a user's measured heartbeat.

#Import statements
import time
import threading
from spidev import SpiDev
from MCP3008 import MCP3008
from pulsesensor import Pulsesensor
import RPi.GPIO as GPIO
import sys

#This creates a Pulse sensor object, p, and starts its measurements as a
#background process. 
p = Pulsesensor()
p.startAsyncBPM()

#Pin assignments for the breadboard
signalBlue = 21
signalRed = 16
offButton = 26


#This tells the Pi to use the broadcom pin-numbering scheme. GPIO numbers will 
#now match up to how they appear on the breakout board.
GPIO.setmode(GPIO.BCM) 

#The light sensor line and off button are configured as outputs and inputs,
#respectively.
GPIO.setup(signalRed, GPIO.OUT)
GPIO.setup(signalBlue, GPIO.OUT)
GPIO.setup(offButton, GPIO.IN)

#Starts the control pwm signal, called LED, at 150 hz frequency. This may seem 
#low for a pwm signal, but for LED lights higher frequencies have no visible 
#effect on the lighting.
LEDB = GPIO.PWM(signalBlue, 100)
LEDR = GPIO.PWM(signalRed, 100) 

#DC, or duty cycle, is a percentage that determines how much of a pulse in a pwm
#signal is powered (i.e. on vs off). This value is what changes the intensity of
#the lights, as a dc of 0 means they are 100% off all the time, and a dc of 100 
#means they are on all the time at full power. DC must be between 0 and 100.
dc = 0

#The LED switch is started with a dc of 0. This means that the lights will be off,
#but the puslses have started at the specified frequency. Once dc is above 0, the 
#physical transistor will begin switching on and off rapidly.
LEDB.start(dc)
LEDR.start(dc)

beat = 0

#This defines updateBeat as a function that grabs and returns a value from the
#heart rates sensor when it is called. This will allow the main program loop to
#run faster without having to check the pulse value constantly.
def updateBeat(beat):
    bpm = p.BPM
    #print(bpm)
    if bpm > 40 and bpm < 150:
        bpm = bpm
    else:
        bpm = 0
    return bpm

#This is the main program loop. The variable x simply keeps track of how many
#iterations the loop goes through. The loop is responsible for having the LEDs
#power up and then down quickly. The speed of the loop is controlled by the
#heart rate value obtained from the updateBeat function. It runs until the
#offButton is held down. 
x = 1
change = 10
while (GPIO.input(offButton) == 0):
    #If there is no measured heart beat, then the lights are solid red.
    if beat == 0:
        LEDB.ChangeDutyCycle(0)
        LEDR.ChangeDutyCycle(100)
        time.sleep(.1)
        
    #When there is a measured heart beat, then the blue lights are turned up or
    #down by 10%. The loop doing this repeatedly is what causes them to pulse
    #completely on and off
    else:
        if(dc <= 99 and change == 10):
            change = 10
        else:
            change = -10
            if(dc >= 1 and change == -10):
                change = -10
            else:
                change = 10
        dc = dc + change
        LEDR.ChangeDutyCycle(0)
        LEDB.ChangeDutyCycle(dc)

        #The rate is calculated to determine how many flashes per second need to
        #occur with the lights. This value is fed directly into the loop sleep
        #control statment. A faster rate means that the loop delay is smaller,
        #and vice versa.
        rate = float(beat/60.0)
        time.sleep(1.0/(20.0*rate))

    #Loop count
    x = x + 1

    #Every 100 cycles through the loop, the heart beat is updated. Doing this
    #prevents the Pi from being taxed too greatly, and also helps a bit with
    #maintaing a consistent measurement.
    if((x/100.0)%1 == 0):
        beat = updateBeat(beat)
        print(beat)
        x = 1



    

#Everything is cleaned up and the program is ended.
p.stopAsyncBPM()
LEDB.stop()
LEDR.stop()
GPIO.cleanup()
sys.exit()


