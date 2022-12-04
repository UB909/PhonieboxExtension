#!/bin/python3

# executed by /etc/rc.local

# GPIO-Bibliothek laden
import RPi.GPIO as GPIO

# BCM-Nummerierung verwenden
GPIO.setmode(GPIO.BCM)

GPIO.setup(12, GPIO.OUT)
GPIO.output(12, True)
