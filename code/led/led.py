#!/usr/bin/python
import RPi.GPIO as GPIO
import time

led = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(led,GPIO.OUT)

def Blink():
   for i in range(0,3):
      print "blink #" + str(i+1)
      GPIO.output(led,True)
      time.sleep(1)
      GPIO.output(led,False)
      time.sleep(1)
   print "done!!"
   GPIO.cleanup()

Blink()
