#!/bin/python3
import serial
import pulsectl
import time
import impulse
from datetime import datetime

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
  audio_sample_array = impulse.getSnapshot(True)[:128]
  sum = 0
  for x in audio_sample_array :
    sum = sum + x
  
  val = sum
  for i in range(1, len(lastValues)-1) :
    lastValues[i-1] = lastValues[i]
    val = max(val, lastValues[i])
  lastValues[len(lastValues)-1] = sum

  showVolume(ser, val/20)

########################################################33
# Initialize Volume Control
volumeCtrl = pulsectl.Pulse('volume-increaser')
sink = volumeCtrl.sink_list()[0]

# Init serial monitor
time.sleep(2)
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
lastUpdate = datetime.now()
while(True) :
  time.sleep(0.05)
  
  # read input from arduino
  while(ser.in_waiting != 0) :
    x = ser.read().decode()
    print(x)
    if(x == "+") :
      volumeCtrl.volume_change_all_chans(sink, 0.025)
      lastUpdate = datetime.now()
    else :
      volumeCtrl.volume_change_all_chans(sink, -0.025)
      lastUpdate = datetime.now()

  if((datetime.now() - lastUpdate).total_seconds() < 2) :
    showVolume(ser, volumeCtrl.volume_get_all_chans(sink))
  else :
    vuMeter(ser)
