#!/usr/bin/env python3
import RPi.GPIO as GPIO

# Set the GPIO mode to Broadcom SOC channel numbering
GPIO.setmode(GPIO.BCM)

# Define the GPIO pin number you want to read from. For this example, I'm using GPIO 17.
PIN_NUMBER = 17

# Set the pin as an input pin
GPIO.setup(PIN_NUMBER, GPIO.IN)

try:
    while True:
        # Read the value from the GPIO pin
        value = GPIO.input(PIN_NUMBER)
        if value:
            print("GPIO pin {} is HIGH".format(PIN_NUMBER))
        else:
            print("GPIO pin {} is LOW".format(PIN_NUMBER))

except KeyboardInterrupt:
    # If someone presses Ctrl+C, clean up the GPIO settings
    GPIO.cleanup()
