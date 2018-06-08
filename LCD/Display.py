#This script demonstrates the messaging capability of a basic LCD screen. It will
#display the time and IP address from the Pi, with a refresh rate of once every
#second.

#Import statements
from LCDScreen import LCD
from subprocess import *
from time import sleep, strftime
from datetime import datetime
import RPi.GPIO as GPIO
import sys

#Pin assignments
#Note that the LCD pin assignments are not listed here. If you wire your screen
#up other than the layout provided, you MUST change the pin assignments for the
#LCD class to match as well. This can be done within the LCDScreen.py file.
offButton = 26
lcd = LCD()

#Sets up GPIO in the Broadcom numbering scheme, and assigns the off button to be
#an input on the GPIO.
GPIO.setmode(GPIO.BCM)
GPIO.setup(offButton,GPIO.IN)

#This string is a bunch of bash commands piped together. It is used in the
#run_cmd method below
cmd = "ip addr show wlan0 | grep inet | awk '{print $2}'"

#This starts the LCD object that was declared before. You must do this step before
#trying to write anything to the LCD.  
lcd.start()

#This method takes in a string, cmd, and feeds it into the Pi console directly.
#For this program, the string commands grab the wlan0 information from the Pi,
#then cut out all the lines except for the IP address.
def run_cmd(cmd):
        p = Popen(cmd, shell=True, stdout=PIPE)
        output = p.communicate()[0]
        return output

#This is the main program loop. It runs until the off button is held down. The
#loop runs every second, and each iteration the lcd screen is cleared, and the
#run_cmd method is used to grab the IP address. The string is then formatted
#and displayed on the screen. The time is also displayed.
while (GPIO.input(offButton) == 0):
        #Clear display
        lcd.clear()
		
		#These python commands get the IP address text, then remove the MAC address
		#so that everything fits on one line. 
        ipaddr = run_cmd(cmd)
        ipaddr = ipaddr.split('\n')
        ipaddr = ipaddr[0]
        ipaddr = ipaddr.split('/')
        ipaddr = ipaddr[0]
        
		#The LCD.message command is what writes to the screen.
        lcd.message(datetime.now().strftime('%b %d  %H:%M:%S\n'))
        lcd.message('IP %s' % ( ipaddr ) )
        sleep(1)

#Clean up and end program.
lcd.clear()
GPIO.cleanup()
sys.exit()
