#!/usr/bin/python
# coding: utf-8
#-------------------------------------------------
# NeoPixel rainbow example, 1536 colors max
# with gamma correction (if needed)
# Author: Peter K. Boxler
#
#--------------------------------------------------
from time import sleep
import sys, os
from neopixel import *
import RPi.GPIO as GPIO
from colorwheel import *

striplen=144

# LED strip configuration:
LED_COUNT   = striplen      # Number of LED pixels.
LED_PIN     = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA     = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_INVERT  = False   # True to invert the signal (when using NPN transistor level shift)

# Button and Led's Definiton
red_button = 23

debug=0                 # 0: no output, 1: debug print
debugg=0
gamma   =1.0            # gamma correction, adjust to 2 or 2.4 if needed
gamma_a=(list)          # list of gamma corrections values
g_maxin =   255.0
g_maxout  = 255.0
delay=20

# ----- set all pixel to dark --------------  
def clearled():
    for i in range (striplen):
        strip.setPixelColor(i, (Color(0,0,0) ))
    strip.show()
    return(0)
#-------------------------------------------
#-------------------------------------------
def waitaste():
    global debug
    print "wait for rote taste..."
    while True:
        if GPIO.input(red_button):
            sleep(0.3)
        else: 
            return(0)

#------------------------------------------
def initpgm():
    global gamma_a
# Establish gamma correction table based on variable gamma
# Gamma correction ist used for all pixels in the image
    gamma_a = bytearray(256)
    for i in range(256):
        gamma_a[i] = int(pow(i / g_maxin, gamma) * g_maxout + 0.5)

#   SETUP General Input/Output-Pins of Raspberry    
    GPIO.setmode(GPIO.BCM) 
    GPIO.setwarnings(False)
    GPIO.setup(red_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)          # red button

#------------------------------------------


#-------------------------------------------------------------
#   generate a rainbow across all pixels
def write_rainbow2 (strip, luminace=50, bright=255):
    global gamma_a
    colog=list()
    i=0
    while True:                             # function color_wheel signals termination     
        colo=color_wheel_r (debug,i , luminace)     # get rgb values
        if colo[0] < 0:                        # loop terminates, all colors done
            break   
        colog.append(gamma_a[colo[1][0]])      # gamma correction
        colog.append(gamma_a[colo[1][1]])
        colog.append(gamma_a[colo[1][2]])
        
        for j in range(strip.numPixels()):  
            strip.setPixelColor(j,Color(colog[0],colog[1],colog[2]))
        strip.setBrightness(bright)
        strip.show()
        sleep(delay/1000.0)
        colog=[]
        if debug:           # print color values
            text='{:<4}'.format(i) + "  " \
            +   '{:>3}'.format(str(colo[1][0])) + " "\
            +   '{:>3}'.format(str(colo[1][1])) + " "\
            +   '{:>3}'.format(str(colo[1][2]))
            print text
      
        i=i+1
    if debug: print "Number of shows %d" % i
#---------------------------------------------------------


#---------------------------------------------------------
# Main program here
#----------------------------------------------------------
if __name__ == '__main__':

    # Create NeoPixel object
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT,LED_BRIGHTNESS)
    # Intialize the library 
    strip.begin()
    striplen=strip.numPixels()
    
    print "Number of Pixels in strip %d" % striplen
    clearled()                  # set all pixels to black
    initpgm()
    waitaste()
    write_rainbow2(strip,50)       # rainbow with luminace 50 / 1536 colors
    clearled()
    sleep(0.1)
    waitaste()
    write_rainbow2(strip,40)    # rainbow with luminace 70 / 924 colors
    clearled()
    sleep(0.1)
    waitaste()
    write_rainbow2(strip,30)   # rainbow with luminace 70 / 924 colors, brightness 70%
    clearled()
    waitaste()
    write_rainbow2(strip,20)    # rainbow with luminace 70 / 924 colors
    clearled()
    sleep(0.1)
    waitaste()
    write_rainbow2(strip,10)    # rainbow with luminace 70 / 924 colors
    clearled()
    sleep(0.1)
    waitaste()
    write_rainbow2(strip,60)    # rainbow with luminace 70 / 924 colors
    clearled()
    sleep(0.1)
    waitaste()
    write_rainbow2(strip,70)    # rainbow with luminace 70 / 924 colors
    clearled()
    sleep(0.1)
    waitaste()
    write_rainbow2(strip,80)    # rainbow with luminace 70 / 924 colors
    clearled()
    sleep(0.1)
    waitaste()
    write_rainbow2(strip,90)    # rainbow with luminace 70 / 924 colors
    clearled()
    sleep(0.1)
    waitaste()
    write_rainbow2(strip,90,100)    # rainbow with luminace 70 / 924 colors
    clearled()
    sleep(0.1)


    sys.exit(0)
#--------------------------------------------------------
# The END        
#---------------------------------------------------------
