#!/usr/bin/python
import webiopi
import datetime
from datetime import datetime, timedelta, tzinfo
import json
import sys
import Adafruit_DHT
#
GPIO = webiopi.GPIO
#GPIO.setmode(GPIO.BCM)
#
global  bAlarmGAS,nowDatetime,humidity,temperature
#
# DH11(temp/humidity sensor) connected to pin 04(BMC)
# MQ2(FC-22) (GAS sensor) connected to the pin 17(BMC)
# 27(BMC)illumination if gas ALARM
DH11             = 11
PIN_DH11_SENSOR  = 4
PIN_MQ2_SENSOR   = 17
PIN_ALARM_GAS    = 27
PIN_LIGHT_SWITCH = 22
#
class GMT3(tzinfo):
     def utcoffset(self, dt):
         return timedelta(hours=3)
     def dst(self, dt):
         return timedelta(0)
     def tzname(self,dt):
         return "Europe/Mowscow"
#
def getLocalTime():
     tz = GMT3()
     return datetime.now(tz).strftime("%Y-%m-%d %H:%M")
#
#==========================================
#
# setup function is automatically called at WebIOPi startup
#
def setup():
    GPIO.setFunction(PIN_DH11_SENSOR, GPIO.IN)
    GPIO.setFunction(PIN_MQ2_SENSOR, GPIO.IN)
    GPIO.setFunction(PIN_ALARM_GAS, GPIO.OUT)
    GPIO.digitalWrite(PIN_ALARM_GAS, GPIO.LOW)
#===========================================
#
# loop function is repeatedly called by WebIOPi
#
def loop():
    # check GAS ALARM and start ALARM SIGNAL
    # I thing this is the open collector!
    bAlarmGAS = GPIO.digitalRead(PIN_MQ2_SENSOR)== GPIO.LOW
    if bAlarmGAS:
        GPIO.digitalWrite(PIN_ALARM_GAS,GPIO.HIGH)
    else:
        GPIO.digitalWrite(PIN_ALARM_GAS, GPIO.LOW)
    webiopi.sleep(1)
    print("Loop",bAlarmGAS)
# destroy function is called at WebIOPi shutdown
def destroy():

    GPIO.digitalWrite(PIN_ALARM_GAS, GPIO.LOW)

@webiopi.macro
def getData_DH11():
   nowDatetime = getLocalTime()
   humidity, temperature = Adafruit_DHT.read_retry(DH11, PIN_DH11_SENSOR)
   lista = [nowDatetime,humidity,temperature]
   return json.dumps(lista)

   #return json.dumps("{0:0.1f} %0.1f" % (humidity, temperature))

@webiopi.macro
def getData_MQ2():
   bAlarmGAS = GPIO.digitalRead(PIN_MQ2_SENSOR)==GPIO.LOW
   print ("GAS=",bAlarmGAS)
   nowDatetime = getLocalTime()
   lista = [nowDatetime,bAlarmGAS]
   return json.dumps(lista)

