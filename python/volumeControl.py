#!/usr/bin/env python3
import serial
import pulsectl
import subprocess
import sys
import time
import impulse
from datetime import datetime
from os.path import exists

lastVolumeUpdate = datetime.now()
lastSound = datetime.now()

def showVolume(ser, volume) :
  # print(volume)
  leds = 0
  if (volume > 1/16) :
    leds = leds + 1
  if (volume > 3/16) :
    leds = leds + 2
  if (volume > 5/16) :
    leds = leds + 4
  if (volume > 7/16) :
    leds = leds + 8
  if (volume > 9/16) :
    leds = leds + 16
  if (volume > 11/16) :
    leds = leds + 32
  if (volume > 13/16) :
    leds = leds + 64
  if (volume > 15/16) :
    leds = leds + 128

  ser.write(bytes([leds]))

lastValues = [0, 0, 0]
def vuMeter(ser) :
  global lastSound
  global lastValues

  audio_sample_array = impulse.getSnapshot(True)[:128]
  sum = 0
  for x in audio_sample_array :
    sum = sum + x
  
  val = sum
  for i in range(1, len(lastValues)-1) :
    lastValues[i-1] = lastValues[i]
    val = max(val, lastValues[i])
  lastValues[len(lastValues)-1] = sum
  
  if(val > 0.0) :
    lastSound = datetime.now()

  if((datetime.now() - lastSound).total_seconds() < 10) :
    showVolume(ser, val/20)
  elif((datetime.now() - lastSound).total_seconds() < 270) :
    ser.write(bytes([128]))
  elif((datetime.now() - lastSound).total_seconds() < 300) :
    if(int((datetime.now() - lastSound).total_seconds()*2) % 2 == 0) : 
      ser.write(bytes([255]))
    else :
      ser.write(bytes([0]))
  else :
    p = subprocess.Popen('/usr/sbin/poweroff', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    quit()

########################################################33
# Initialize Volume Control
volumeCtrl = pulsectl.Pulse('volume-increaser')
sink = volumeCtrl.sink_list()[0]

# Init serial monitor
while(not exists('/dev/ttyUSB0')) :
  print('wait for usb')
  time.sleep(1)

ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
# Read Arduino welcome message
time.sleep(2)
while(ser.in_waiting != 0) :
  ser.read(ser.in_waiting)
  time.sleep(0.5)

# Initialize impulse for vu meter
impulse.setup(0)
impulse.start()

print("ready")

########################################################33
# Main loop
while(True) :
  time.sleep(0.05)
  
  # read input from arduino
  while(ser.in_waiting != 0) :
    x = ser.read().decode()
    print(x)
    if(x == "+") :
      increaseBy = min(0.025, 1.0 - volumeCtrl.volume_get_all_chans(sink))
      volumeCtrl.volume_change_all_chans(sink, increaseBy)
      lastVolumeUpdate = datetime.now()
    else :
      volumeCtrl.volume_change_all_chans(sink, -0.025)
      lastVolumeUpdate = datetime.now()

  if((datetime.now() - lastVolumeUpdate).total_seconds() < 2) :
    showVolume(ser, volumeCtrl.volume_get_all_chans(sink))
  else :
    vuMeter(ser)
