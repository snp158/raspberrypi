#!/usr/bin/python
import webiopi
import datetime
import json
import datetime
import sys
import Adafruit_DHT

GPIO = webiopi.GPIO

global nowDatetime, humidity, temperature

DH11 = 11
PIN = 4

# setup function is automatically called at WebIOPi startup
def setup():
    # set the GPIO used by the light to output
    GPIO.setFunction(PIN, GPIO.IN)
	
# loop function is repeatedly called by WebIOPi
def loop():
    # retrieve current datetime
    #nowDatetime = datetime.datetime.now()
    #humidity, temperature = Adafruit_DHT.read_retry(DH11, PIN)
    # gives CPU some time before looping again
    #print(temperature, humidity)

    webiopi.sleep(1)

# destroy function is called at WebIOPi shutdown
def destroy():
    GPIO.digitalWrite(PIN, GPIO.IN)

@webiopi.macro
def getData():
   global  nowDatetime,humidity,temperature
   nowDatetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
   humidity, temperature = Adafruit_DHT.read_retry(DH11, PIN)
   lista =nowDatetime,humidity,temperature 
   return json.dumps(lista)
   #return json.dumps("{0:0.1f} %0.1f" % (humidity, temperature))



