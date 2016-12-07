#!/usr/bin/python
# coding: utf-8
#----------------------------------------------------------------
# Pi Soft Shutdown Script
# reagiert auf soft_shutdown_pin und leitet halt oder reboot ein, je nach Stellung des Kippschalters
# shutdown_type_pin in diesem moment
#----------------------------------------------------------------
# angepasst by Peter Boxler
#------------------------------------------------------------------

# Import the modules to send commands to the system and access GPIO pins
from subprocess import call
import RPi.GPIO as gpio
from time import sleep

# Define variables to store the pin numbers

soft_shutdown_pin = 27      # Pion fur Shutdown Drucktaste
led_shutdown_pin = 9        # Default pin for grüne LED
shutdown_type_pin = 17      # Kippschalter definiert halt oder reboot
#
#from time import sleep
import RPi.GPIO as GPIO
var=1
GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)
GPIO.setup(soft_shutdown_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup (led_shutdown_pin, GPIO.OUT)   # Port schaltet LED ein, diese zeigt, dass Programm läuft
GPIO.setup(shutdown_type_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

sleep(5)

# Define a function to run when an interrupt is called
def shutdown():
#    call(['shutdown', '-hP','+0.5'], shell=False)
    sleep(2)        # zeit geben den prozessen
    if not GPIO.input(shutdown_type_pin):       # frage kippschalter ab.
        call('halt', shell=False)
 #       print "halt gewählt"
    else:
        call ('reboot', shell=False)
 #       print "reboot gewählt"
             
def blink_led():  # blink led 3 mal bei start und bei shutdown
        for i in range(3):
            GPIO.output(led_shutdown_pin, True)
            sleep(0.3)
            GPIO.output(led_shutdown_pin, False)
            sleep(0.2)
    

def my_callback(channel):
    print "Pin Falling: %d" % channel
    sleep(1)  # confirm the movement by waiting 1 sec 
    if not GPIO.input(soft_shutdown_pin): # and check again the input
        print("ok, pin ist tief!")
        blink_led()
        shutdown()

blink_led()
#
GPIO.add_event_detect(soft_shutdown_pin, GPIO.FALLING, callback=my_callback, bouncetime=300)

# you can continue doing other stuff here
while True:
    sleep(1)
    pass    # pass ist leer statement