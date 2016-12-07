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
import time, math
from colorwheel import *
striplen=64

# LED strip configuration:
LED_COUNT   = striplen      # Number of LED pixels.
LED_PIN     = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA     = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_INVERT  = False   # True to invert the signal (when using NPN transistor level shift)

BLACK=[0,0,0]
debug=1                 # 0: no output, 1: debug print
gamma1   =2.4          # gamma correction, adjust to 2 or 2.4 if needed
gamma2 = 3.0
gammatab1=(list)          # list of gamma corrections values
gammatab2=(list)          # list of gamma corrections values
g_maxin =   255.0
g_maxout  = 255.0
delay=20

# ----- set all pixel to dark    
def clearled(color=BLACK):
    for i in range (striplen):
        strip.setPixelColor(i, (Color(color[0],color[1],color[2])))
    strip.show()
    return(0)
#--------------------------

#------------------------------------------
def initpgm():
    global gammatab1, gammatab2
# Establish gamma correction table based on variable gamma
# Gamma correction ist used for all pixels in the image
    gammatab1 = bytearray(256)
    for i in range(256):
        gammatab1[i] = int(pow(i / g_maxin, gamma1) * g_maxout + 0.5)

    gammatab2 = bytearray(256)
    for i in range(256):
        gammatab2[i] = int(pow(i / g_maxin, gamma2) * g_maxout + 0.5)

#------------------------------------------

# ------------------------------------------------------
def patt_fade(strip,color, von,bis,mitgamma=0):
    global  debug
    if debug: print "Draw patt_fade, mitgamma %d, color %d" % (mitgamma, color)
    
    brightstart=0
    bright=brightstart
    for i in range(bis-von+1): 
        brightstep=255/8
        pix=i+von
        bright=(bright+25) & 255
        if mitgamma==1:

            if debug:           # print color values
                text='{:<3}'.format(i) + " " \
                +   '{:>3}'.format(str(pix)) + " "\
                +   '{:>3}'.format(str(bright)) + " "\
                +   '{:>3}'.format(str(gammatab1[bright]))
            print text
            if color==0:
                color1=Color(gammatab1[bright],gammatab1[bright],gammatab1[bright])
            elif color==1:          # red
                color1=Color(gammatab1[bright],0,0)
            elif color==2:      # green
                color1=Color(0,gammatab1[bright],0)
            else:           # blue
                color1=Color(0,0,gammatab1[bright])
                  
        elif mitgamma==2:
            if debug:           # print color values
                text='{:<3}'.format(i) + " " \
                +   '{:>3}'.format(str(pix)) + " "\
                +   '{:>3}'.format(str(bright)) + " "\
                +   '{:>3}'.format(str(gammatab2[bright]))
            print text
            if color==0:
                color1=Color(gammatab2[bright],gammatab2[bright],gammatab2[bright])
            elif color==1:          # red
                color1=Color(gammatab2[bright],0,0)
            elif color==2:      # green
                color1=Color(0,gammatab2[bright],0)
            else:           # blue
                color1=Color(0,0,gammatab2[bright])
        else:
            if debug:           # print color values
                text='{:<3}'.format(i) + " " \
                +   '{:>3}'.format(str(pix)) + " "\
                +   '{:>3}'.format(str(bright)) 
            print text
            if color==0:
                color1=Color(bright,bright,bright)
            elif color==1:          # red
                color1=Color(bright,0,0)
            elif color==2:      # green
                color1=Color(0,bright,0)
            else:           # blue
                color1=Color(0,0,bright)

        strip.setPixelColor(pix, color1)
        strip.show()
        time.sleep(delay/1000.0)
        bright=brightstart+((i+1)*255/8) & 255   
        
#-------------------------------------------------    
# Define functions which animate LEDs in various ways.
def colorWipe2(strip):
    global gamma_a
    if debug: print "Draw colorwipe2"

    step=int(255/(striplen/3))              # Helligkeits step
    if debug: print "step: %d " % step
    
    if debug: print "now red"
    max=255
    for i in range(striplen/3): 
        color=Color(gamma_a[max],0,0)
#        print max, gamma_a[max]
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(delay/1000.0)
        max=255-(i*step)
#        print "i: %d max: %d" % (i,max)    
        
    max=255
    y=0
    if debug: print "now blue"
    for i in range(striplen/3,2*striplen/3): 
        
        color=Color(0,0,gamma_a[max])
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(delay/1000.0)
        max=255-(y*step)
        y=y+1
#    print i,max

    max=255
    y=0
    if debug: print "now green"
    for i in range(2*striplen/3,striplen): 
        
        color=Color(0,gamma_a[max],0)
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(delay/1000.0)
        max=255-(y*step)
        y=y+1
#        print "i: %d max: %d" % (i,max)    
#
    clearled(BLACK)

    if debug: print "now red umgekehrt"
    i=0
    max=0
    for i in range(striplen/3): 

        color=Color(gamma_a[max],0,0)
#        print max, gamma_a[max]

        strip.setPixelColor(i, color)
        strip.show()
        i=i+1
        time.sleep(delay/1000.0)
        max=0+(i*step)
        time.sleep(delay/1000.0)

     #   print "i: %d max: %d" % (i,max)    
    if debug: print "Anzahl show %d: " % i                
    return(0)    

      
#---------------------------------------------------------------
def mainloop (strip):
    global debug
#    colorWipe2(strip)
    
 #   sleep(6)

#    patt_fade ( strip, 0, 0,7)          # ohne gamma, weiss
    patt_fade ( strip, 0, 0,7,1)       # gamma 1
    patt_fade ( strip, 0,8,15,2)       # gamma 2
    
#    patt_fade ( strip, 1, 24,31)        # ohne gamma rot
    patt_fade ( strip, 1,16,23,1)       # gamma 1 rot
    patt_fade ( strip, 1,24,31,2)       # gamma 2 rot
 #   patt_fade ( strip, 2, 48,55)        # ohne gamma grün
    patt_fade ( strip, 2,32,40,1)       # gamma 1 grün
    patt_fade ( strip, 2,40,48,2)       # gamma 1 grün
    patt_fade ( strip, 3,48,55,1)       # gamma 1 grün
    patt_fade ( strip, 3,56,64,2)       # gamma 1 grün

    sleep(7)


#---------------------------------------------------------
# Main program here
#----------------------------------------------------------
if __name__ == '__main__':

    # Create NeoPixel object
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT,LED_BRIGHTNESS)
    # Intialize the library 
    strip.begin()
    clearled()                  # set all pixels to black
    initpgm()
    
    mainloop (strip )
    sleep(1)
    clearled()                  # set all pixels to black


    
    sys.exit(0)
#--------------------------------------------------------
# The END        
#---------------------------------------------------------
