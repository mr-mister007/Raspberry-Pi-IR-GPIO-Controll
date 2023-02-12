#-----------------------------------------#
# Name - IR-Finalized.py
# Description - The finalized code to read data from an IR sensor and then reference it with stored values
# Author - Lime Parallelogram
# License - Completely Free
# Date - 12/09/2019
#------------------------------------------------------------#
# Imports modules
import RPi.GPIO as GPIO
from datetime import datetime

# Static program vars
pin = 22
light=16
FAN=18 # Input pin of sensor (GPIO.BOARD)
Button1 = [ 0x301fe807f ]
Button2 = [ 0x301fe40bf ]
Button3 = [ 0x301fec03f ]
Button4 = [ 0x301fe20df ]
Button5 = [ 0x301fe50af ]
Button6 = [ 0x301fed827 ]
ButtonsNames = ["RED",   "GREEN",      "BLUE",       "WHITE",]  # String list in same order as HEX list

# Sets up GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin, GPIO.IN)
GPIO.setup(light, GPIO.OUT)
GPIO.setup(FAN, GPIO.OUT)
GPIO.setup(11, GPIO.OUT)



# Gets binary value


def getBinary():
        # Internal vars
        num1s = 0  # Number of consecutive 1s read
        binary = 1  # The binary value
        command = []  # The list to store pulse times in
        previousValue = 0  # The last value
        value = GPIO.input(pin)  # The current value

        # Waits for the sensor to pull pin low
        while value:
                #sleep(0.0001) # This sleep decreases CPU utilization immensely
                value = GPIO.input(pin)

        # Records start time
        startTime = datetime.now()

        while True:
                # If change detected in value
                if previousValue != value:
                        now = datetime.now()
                        pulseTime = now - startTime #Calculate the time of pulse
                        startTime = now #Reset start time
                        command.append((previousValue, pulseTime.microseconds)) #Store recorded data

                # Updates consecutive 1s variable
                if value:
                        num1s += 1
                else:
                        num1s = 0

                # Breaks program when the amount of 1s surpasses 10000
                if num1s > 10000:
                        break

                # Re-reads pin
                previousValue = value
                value = GPIO.input(pin)

        # Converts times to binary
        for (typ, tme) in command:
                if typ == 1: #If looking at rest period
                        if tme > 1000: #If pulse greater than 1000us
                                binary = binary *10 +1 #Must be 1
                        else:
                                binary *= 10 #Must be 0

        if len(str(binary)) > 34: #Sometimes, there is some stray characters
                binary = int(str(binary)[:34])

        return binary

# Convert value to hex
def convertHex(binaryValue):
        tmpB2 = int(str(binaryValue),2) #Temporarely propper base 2
        return hex(tmpB2)

while True:
        inData = convertHex(getBinary()) #Runs subs to get incoming hex value
        for button in range(len(Button1)):#Runs through every value in list
                if hex(Button1[button]) == inData: #Checks this against incoming
                        print("ON") #Prints corresponding english name for button
                        GPIO.output(light, GPIO.HIGH)
                elif hex(Button2[button]) == inData: #Checks this against incoming
                         print("OFF") #Prints corresponding english name for button
                         GPIO.output(light, GPIO.LOW)
                elif hex(Button3[button]) == inData: #Checks this against incoming
                         print("ON") #Prints corresponding english name for button
                         GPIO.output(FAN, GPIO.HIGH)
                elif hex(Button4[button]) == inData: #Checks this against incoming
                         print("OFF") #Prints corresponding english name for button
                         GPIO.output(FAN, GPIO.LOW)
				elif hex(Button5[button]) == inData: #Checks this against incoming
                         print("OFF") #Prints corresponding english name for button
                         GPIO.output(11, GPIO.LOW)		 
				elif hex(Button6[button]) == inData: #Checks this against incoming
                         print("ON") #Prints corresponding english name for button
                         GPIO.output(11, GPIO.HIGH)		 