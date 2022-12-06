#!/bin/python3
import RPi.GPIO as GPIO

# BCM-Nummerierung verwenden
GPIO.setmode(GPIO.BCM)

GPIO.setup(12, GPIO.OUT)
GPIO.output(12, False)
