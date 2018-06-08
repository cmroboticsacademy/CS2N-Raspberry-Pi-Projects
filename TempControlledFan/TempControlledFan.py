#This script will control a fan using a temperature sensors so that the fan only runs
#when the temperature is above a certain threshold.

#Import statements
import smbus
import RPi.GPIO as GPIO
import time
import sys

#Newer Pi models use I2C bus on channel 1. If you have an older model, switch this to 0.
I2C_BUS = 1
#Creates a bus "object" with all of needed I2C methods available for use
bus = smbus.SMBus(I2C_BUS)

#Pin assignments for the breadboard
fanSignal = 21
offButton = 26

#The device address is where on the I2C bus the temperature sensor is located. This number
#may need to be changed if the sensor is detected somewhere else. In the Pi command window,
#type "i2cdetect" to scan for where the sensor is on the bus to confirm its at 48.
DEVICE_ADDRESS = 0x48

#This tells the Pi to use the broadcom pin-numbering scheme. GPIO numbers will now match up
#to how they appear on the breakout board.
GPIO.setmode(GPIO.BCM)

#Sets the fanSignal and offButton pins to GPIO outputs and inputs, respectively.
GPIO.setup(fanSignal, GPIO.OUT)
GPIO.setup(offButton, GPIO.IN)

#This is the main program loop. Every second, the loop runs once and calculates the temperature
#reading, and then determines whether to activate the fan or not based on that number. It runs
#until the off button is held down.
x = 1
while (GPIO.input(offButton) == 0):
	#These lines access the tempearture sensor at its device and compute its value.
	#The first line reads the data bytes from the sensor, and the second line converts
	#the bytes into a temperature in bits
 	register_byte = bus.read_i2c_block_data(DEVICE_ADDRESS, 0, 2)
	temp = (register_bytes[0]<<4)|(register_bytes[1]>>4)

	#This if statement ensures that negative temperatures display correctly.
	if temp > 0x7FF:
		temp |= 0xF000

	#Convert the digital reading to analog temperature where 1 bit is equal to 0.0625 C
	temp_C = float(temp) * 0.0625
	temp_F = temp_C * 9/5+32
	print "Sample %3.1f : Temp = %3.1f C -- %3.1f F" % (x,temp_C,temp_F)

	#Here the temperature is actually used for something useful. If the measured temperature
	#is over 80 degress, then the fan is set to turn on, otherwise it is held off. Feel free
	#to experiment with this value a bit.
	if temp_F > 80: #////////CHANGE TEMPERATURE CUTOFF HERE//////////
		GPIO.output(21, GPIO.HIGH)
	else:
	    GPIO.output(21, GPIO.LOW)
	#The delay makes sure that the loop only runs once per second and doesn't tax the Pi too
	#much from overclocking. X counts the number of samples over time.
	time.sleep(1)
	x = x + 1

#The GPIO.cleanup method clears out all pin assignments so they don't conflict with other scripts
#in the future.
GPIO.cleanup()

#Program end
sys.exit()
