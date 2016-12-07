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

numbpix=144            # Number of pixels in strip
# LED strip configuration:
LED_COUNT   = numbpix      # Number of LED pixels.
LED_PIN     = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA     = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_INVERT  = False   # True to invert the signal (when using NPN transistor level shift)

debug=0                # set to 1 to get debug printout

gamma  = 1.0           # gamma correction, adjust to 2 or 2.4 if needed
gamma_a = (list)         # list of gamma corrections values
g_maxin =   255.0
g_maxout  = 255.0
delay = 20              # time in ms for a color to be up
white=[0,1,2,3,4,5,139,140,141,142,143]     # set these pixels to white as a border

# ----- set all pixel to dark --------------  
def clearled():
    for i in range (striplen):
        strip.setPixelColor(i, (Color(0,0,0) ))
    strip.show()
    return(0)
#-------------------------------------------

#---------------------------------------------
def initpgm():
    global gamma_a
# Establish gamma correction table based on variable gamma
# Gamma correction ist used for all pixels in the image
    gamma_a = bytearray(256)
    for i in range(256):
        gamma_a[i] = int(pow(i / g_maxin, gamma) * g_maxout + 0.5)

#------------------------------------------

#-------------------------------------------------
# Generate 1536 rgb Colors around the colorwheel
# Starting with RED
#-------------------------------------------------
#   parameters: 
#   position on colorwheel, luminace 10-90 %
#   loop needs to be outside the function (see example)
#   pos indicates postion on the colorwheel
#   luminance can be 10,20,30,40,50,60,70,80,90 %
#   luminance 50% gives max. number of colors : 1536
#   the loopcounter has to set like this:
#   while True
#
#   returns  (retcode , [ r ,g, b]
#      
#   retcode:
#   0 if colorvalue 
#   -98 wrong luminance
#   -99 max. color reached
# 
#   Peter K. Boxler, February 2015
# ---------------------------------------------------------------  
def color_wheel_r ( posin , lum=50 ):

    colval_min=[255,0,0,0,0, 0 , 51,102,153,204,255]      # rbg values max and min
    colval_max=[0 ,51,102,153,204,255,255,255,255,255,255]      # rbg values max and min

    count=[0,312,618,924,1230,1536,1230,924,618,312,0]  # loop counter limit based on lum
    retu=0                      # returncode init
    
    if lum<10 or lum>90:        # must be between 10 and 90
        return (-98,[0,0,0])
    pos=posin                   # keep colorwheel pos input
    if pos >= count[lum/10]:    # signal that we reached max number of colors for this luminace
        pos=pos-count[lum/10]
        retu=-99                # signal overflow to caller (but continue after correction)
    if pos < 0:
        pos=count[lum/10]-abs(pos)      # allow to run below zero
        if debug: print "colwheel --- pos below zero, new value: %d" % pos
        retu=-99
    min=colval_min[lum/10]    # set min values for r,g and b  based on luminace
    max=colval_max[lum/10]      # set max values for r,g and b  
    z=max-min+1
    if debug:
        print "colwheel --- posin: %d pos: %d  min: %d  max: %d z: %d count: %d ----------" % (posin, pos, min, max, z, count[lum/10])
    
    if pos < z: 
        if debug: print "colwheel --- pos %d doing part 1" % pos
                # first sixth of wheel
        return(retu,[max, pos+min, min])        # red=max, green increases=0, blue=0
    
    elif pos < (2 * z):                             # second sixth of wheel
        pos -= z
        if debug: print "colwheel --- pos %d doing part 2" % pos
        return(retu,[max-pos, max, min])          # red decrases, green=max, blue=0
    elif pos < (3 * z):                             # third sixth of wheel
        if debug: print "colwheel --- pos %d doing part 3" % pos
        pos -= 2 * z
        return(retu,[min, max, pos+min])        # red=0, green max, blue=increases
    elif pos < (4 * z):                             # fourth sixth of wheel
        if debug: print "colwheel --- pos %d doing part 4" % pos
        pos -= 3 * z
        return(retu,[min, max-pos, max])          # red=0, green=decreases, blue=max
    elif pos < (5 * z):                             # fifth sixth of wheel
        if debug: print "colwheel --- pos %d doing part 5" % pos
        pos -= 4 * z
        return(retu,[pos+min, min, max])        # red increases, green=0, blue=max
    else:                                           # last sixth of wheel
        if debug: print "colwheel --- pos %d doing part 6" % pos
        pos -= (5 * z)
        return(retu,[max, min, max-pos])          # red=max, green=0, blue decreases

#--------------------------------------------------------------


#-------------------------------------------------------------
#   Write rainbow  :  generate a rainbow across all pixels with white border
#-------------------------------------------------------------
def write_rainbow (strip, luminace=50, bright=255):
    global gamma_a
    colog=list()
    i=0

#   do 5 pixels white on both end of the strip
    for i in white:
        strip.setPixelColor(i,Color(255,255,255))
    
#   fill pixels with color        
    while True:                             # function color_wheel signals termination     
        colo=color_wheel_r (i , luminace)     # get rgb values
        if colo[0] < 0:                       # loop terminates, all colors done
            break   
        colog.append(gamma_a[colo[1][0]])     # gamma correction
        colog.append(gamma_a[colo[1][1]])
        colog.append(gamma_a[colo[1][2]])
        
        for j in range(strip.numPixels()-len(white)+1):
            pix=j+5  
            strip.setPixelColor(pix,Color(colog[0],colog[1],colog[2]))
        strip.setBrightness(bright)
        strip.show()
        sleep(delay/1000.0)
        colog=[]
        if debug:           # print color values
            text="wheelpos: " \
            + '{:<4}'.format(i) + "  color: " \
            +   '{:>3}'.format(str(colo[1][0])) + " "\
            +   '{:>3}'.format(str(colo[1][1])) + " "\
            +   '{:>3}'.format(str(colo[1][2]))
            print text
      
        i=i+1
    print "Number of shows/colors %d" % i
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
    
    print "Number of pixels in strip %d" % striplen
    clearled()                  # set all pixels to black
    initpgm()
    write_rainbow (strip , 50)       # rainbow with luminace 50 / 1536 colors
    clearled()
#--------------------------------------------------------
# The END        
#---------------------------------------------------------
