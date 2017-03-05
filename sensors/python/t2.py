#!/usr/bin/python
import webiopi
import datetime
import json
import datetime
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
DH11 = 11
PIN_DH11 = 4
PIN_MQ2 = 17
PIN_ALARM_GAS = 27
PIN_LIGHT_SWITCH = 22
#==========================================
#
# setup function is automatically called at WebIOPi startup
#
def setup():
    GPIO.setFunction(PIN_DH11, GPIO.IN)
    GPIO.setFunction(PIN_MQ2, GPIO.IN)
    GPIO.setFunction(PIN_ALARM_GAS, GPIO.OUT)
    GPIO.digitalWrite(PIN_ALARM_GAS, GPIO.LOW)
#===========================================
#
# loop function is repeatedly called by WebIOPi
#
def loop():
    # check GAS ALARM and start ALARM SIGNAL
    # I thing this is the open collector!
    bAlarmGAS = GPIO.digitalRead(PIN_MQ2)== GPIO.LOW
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
def getData():
   bAlarmGAS = GPIO.digitalRead(PIN_MQ2)==GPIO.LOW
   print ("GAS=",bAlarmGAS)
   nowDatetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
   humidity, temperature = Adafruit_DHT.read_retry(DH11, PIN_DH11)
   lista = [bAlarmGAS,nowDatetime,humidity,temperature]
   return json.dumps(lista)

   #return json.dumps("{0:0.1f} %0.1f" % (humidity, temperature))

