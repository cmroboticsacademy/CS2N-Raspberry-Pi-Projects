#This script should be used to test the pulse sensor on its own so that it can
#be used later in the PulseController script accurately

#Import statements
import time
import threading
import sys
import RPi.GPIO as GPIO
from spidev import SpiDev
from MCP3008 import MCP3008
from pulsesensor import Pulsesensor

#This creates a Pulse sensor object, p, and starts its measurements as a
#background process.
p = Pulsesensor()
p.startAsyncBPM()

#Pin assignments for the breadboard
offButton = 26

#This tells the Pi to use the broadcom pin-numbering scheme. GPIO numbers will
#now match up to how they appear on the breakout board.
GPIO.setmode(GPIO.BCM)
GPIO.setup(offButton, GPIO.IN)

#This loop runs every second until the off button is held down. Within the loop,
#The heart rate is obtained from the pulse sensor object. This value is then
#filtered a bit. Values that are too high or low are ignored. Additionally, when
#values vary too much from one loop to the next, the filler text "Calculating"
#is printed on screen.
bpm = p.BPM
while (GPIO.input(offButton) == 0):
    bpmLast = bpm
    bpm = p.BPM
    
    if bpm > 40 and bpm < 210:
        if(abs(bpmLast - bpm) <= 5):
            print("BPM: %d" % bpm)
        else:
            print("Calculating")
    else:
        print("No Heartbeat found")
    time.sleep(1)

#Everything is cleaned up and the program is ended.
p.stopAsyncBPM()
GPIO.cleanup()
sys.exit()
