#!/usr/bin/python
# coding: utf-8
#----------------------------------------------------------
#
#   Light Painting Programm for NeoPixel Strip
#
#   Based on several examples found on the Adafruit Learning System
#   Thanks to Tony DiCola , Phillip Burgess and others
#
#   This version adapted and expanded by Peter K. Boxler, Switzerland
#   January 2015
#
#   NeoPixel Products here: 
#   ----> https://www.adafruit.com/products/1506
#-----------------------------------------------------------
#
import sys, getopt, os
import time, math
from time import sleep

import RPi.GPIO as GPIO
from PIL import Image
import struct
from neopixel import *

#Button handling:
red_button = 4
black_button = 17
BLACK=1
REDSHORT=2
REDLONG=3
but={1:'Black', 2:'Red-short', 3:'Red-long'}
led_rot=23
led_green=25

striplen=144

# LED strip configuration:
LED_COUNT      = striplen     # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)

# Configurable values
column_delay_time = 0.100

xmlfile="a.xml"	#default input file name	
onoff={1:'ON', 0:'OFF'}

debug=0                 # debug print out
do_term=0               # term signal in mainloop

gamma   =2.8            # gamma correction
gamma_a=(list)          # list of gamma corrections for every brightness 0-255

debugg=0
delay=20

pattern1=[0,50,80,120,180,220,250,250,250,250,250,250,220,180,120,80,50,0]
pattern2=[0,50,60,80,100,120,180,220,250,250,250,250,250,250]
pattern3=[  [32,0,194],
            [0,97,255],
            [0,255,212],
            [90,160,40],
            [127,125,20],
            [177,195,10],
            [255,133,0],            
            [255,34,0],
            [255,0,0],
            [144,0,0]
            ]

pattern4=[  [32,0,194],
            [0,97,255],
            [0,255,212],
            [90,160,40],
            [127,125,20],
            [177,19,10],
            ]

pattern5=[  [32,0,194],
            [0,97,255],
            [0,255,212],
            [200,30,20]
            ]
BLACK=[0,0,0]
BOTTOM=-1
TOP=-1
UP=1
DOWN=0
FULL=-2
UPDOWN={1:'UP', 0:'DOWN'}
#
# ***** Function Parse commandline arguments ***********************
# get and parse commandline args

def arguments(argv):
    global debug,file_path
    try:
        opts, args=getopt.getopt(argv,"hdDp:")
    except getopt.GetoptError:
        myPrint ("Parameter Error")
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print ("App neopix1 Actions -----------------------------------")
            print ("usage: neopix1 [-d ]")
            sys.exit(2)
        elif opt == '-d': 	debug = 1
        elif opt == '-D': 	
            debug = 1
            debugg = 1
        elif opt == '-p': 	file_path = arg

	
# ***********************************************



#------- Funktion initpgm ---------------------------------
#
def initpgm():
    global gamma_a, gamma
    g_maxin =   255.0
    g_maxout  = 255.0



#   setup General Input/Output-Pins of Raspberry    
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False) 
    GPIO.setup(red_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)          # red
    GPIO.setup(black_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)          # black
    GPIO.setup (led_rot, GPIO.OUT)   # rote Led
    GPIO.setup (led_green, GPIO.OUT)   # rote Led
    GPIO.output(led_rot, False)
    GPIO.output(led_green, False)

# Calculate gamma correction table based on variable gamma
# Gamma correction ist used for all pixels in the image
    gamma_a = bytearray(256)
    for i in range(256):
        gamma_a[i] = int(pow(i / g_maxin, gamma) * 255.0 + 0.5)

#    if debug:
 #       for z in range(256):
  #          print "gamma_a %d %d" % (z,gamma_a[z])


# ----------	
def float_to_hex(f):
    return hex(struct.unpack('<I', struct.pack('<f', f))[0])
#------------



#------Wait for button Press (Black or Red) --------------------------------    
def button_pressed():
    print "Waiting for Tastendruck..."
    
    while True:
        inpblack=1
        inpred=1
        inpblack=GPIO.input(black_button)       # high if NOT pressed !
        inpred=GPIO.input(red_button)
#        print "Button %d %d" % (inpblack, inpred)
        sleep(0.2)
        if not inpblack:  return(BLACK)         # black button went to low
        if not inpred:                          # red button went to low
            sleep(1)                            # check if red is pressed long or short
            inpred=GPIO.input(red_button)
            sleep(0.1)
            if inpred: return(REDSHORT)
            else: return(REDLONG)

    pass
#-------------------------------------------

# ***** Function blink-led **************************
def blink_led(pin,anzahl):  # blink led 3 mal bei start und bei shutdown
        for i in range(anzahl):
            GPIO.output(pin, True)
            sleep(0.1)
            GPIO.output(pin, False)
            sleep(0.1)


# -------------------------

def draw() :
    print"Zeichnen................"  
    sleep (1) 
    return(0)
#-------------------------    
    
# ----- set all pixel to dark    
def clearled(color):
    for i in range (striplen):
        strip.setPixelColor(i, (Color(color[0],color[1],color[2])))
    strip.show()
    return(0)
#--------------------------

#---------------------------------------------
def wheel2(pos,how=0):
#    Generate rainbow colors within 0-255.
    if pos < 85:
        if how:
            return (pos * 3, 255 - pos * 3, 0)
        else:
            return Color(pos * 3, 255 - pos * 3, 0)

    elif pos < 170:
        pos -= 85
        if how:
            return (255 - pos * 3, 0, pos * 3)
        else:
            return Color(255 - pos * 3, 0, pos * 3)

    else:
        pos -= 170
        if how:
            return (0, pos * 3, 255 - pos * 3)
        else:
            return Color (0, pos * 3, 255 - pos * 3)
  #--------------------------------------------  

#---------------------------------------------
def wheel (start , how=0, gamma=0):
#    Generate rainbow colors within 0-255.
    global gamma_a
    if start < 85:
#        print "%d:  %d  %d  %d" % (start, start * 3, 255 - start * 3, 0)

        if how: 
            if gamma:
                return (gamma_a[start * 3],gamma_a [ 255 - start * 3], 0)
            
            else:           # forward
                return (start * 3, 255 - start * 3, 0)
        else:
            if gamma:
                return Color(gamma_a[start * 3],gamma_a [ 255 - start * 3], 0)
            else:
                return Color(start * 3, 255 - start * 3, 0)

    elif start < 170:
 #       print "%d:  %d  %d  %d" % (start, 255- (start-85) * 3, 0, (start-85)*3 )

        start -= 85

        if how: 
            if gamma:
                return (gamma_a[255 - start * 3], 0, gamma_a[start * 3])
            else:            #forward
                return (255 - start * 3, 0, start * 3)
        else:
        
            if gamma:
                return Color(gamma_a[255 - start * 3], 0, gamma_a[start * 3])
        
            else:
                return Color(255 - start * 3, 0, start * 3)

    else:
  #      print "%d:  %d  %d  %d" % (start, 0, (start-170) * 3, 255 - (start-170) * 3)

        start -= 170

        if how:
            if gamma:
                return (0, gamma_a[start * 3], gamma_a[255 - start * 3])
            else:
                return (0, start * 3, 255 - start * 3)
        else:
            if gamma:
                return Color (0, gamma_a[start * 3], gamma_a[255 - start * 3])
            else:
                return Color (0, start * 3, 255 - start * 3)
  #--------------------------------------------  


def rainbow_alt(strip, wait_ms=20, iterations=1):
    if debug: print "Draw rainbow that fades across all pixels at once."
    for j in range(256*iterations):
        for i in range(striplen):
            strip.setPixelColor(i, wheel((i+j) & 255))
        strip.setBrightness(80)
        strip.show()
        time.sleep(wait_ms/1000.0)

# --  Function write_rainbow ----------------------------------
#   generate a rainbow pattern with lenght len, starting at pos
def write_rainbow(strip, start, len, gamma=0,bright=60):
    if debug: print "write_rainbow start %d len %d gamma %d" % (start,len,gamma)
    #   use pixel start to start+len 
    stripl=strip.numPixels()
    for i in range( 0,len):
        if i < stripl:
            strip.setPixelColor(start+i, wheel((i+i*256/len) & 255,0,gamma))
    strip.setBrightness(bright)
    strip.show()

# --  Function make_rainbow ----------------------------------
# return a rainbow pattern with lenght len
def make_rainbow(len, gamma=0):
    if debug: print "return a rainbow pattern with lenght %d" % len
    pat=[]
    for i in range( 0,len):
        pat.append(wheel((i+i*256/len) & 255,1,gamma))
    return(pat)
    
#-----------------------------------------------    
def rainbow(strip, start=FULL, end=-1, bright=60, iterations=1, wait_ms=20  ):
    if start==FULL:
        start=0
        end=strip.numPixels()
    elif end == -1:
        print "rainbow: end not defined"
        return()
    ctr=end-start
    if debug: print "Draw rainbow  start %d end %d iter: %d  bright: %d" % (start, end, iterations, bright)
    
    for j in range(256*iterations):
        for i in range(ctr):
            strip.setPixelColor(i+start, wheel((i+j) & 255))
        strip.setBrightness(bright)
        strip.show()
        time.sleep(wait_ms/1000.0)
 #--------------------------------------------------       
def rainbowCycle(strip, start=FULL, end=-1, bright=60, iterations=1, wait_ms=20  ):
    if start==FULL:
        start=0
        end=strip.numPixels()
    elif end == -1:
        print "rainbow: end not defined"
        return()
    ctr=end-start
    
    if debug: print "Draw rainbowCycle  anzahl: %d  bright: %d" % (iterations, bright)
    for j in range(256*iterations):
        for i in range(ctr):
            strip.setPixelColor(i+start, wheel(((i * 256 / 150) + j) & 255))
        strip.setBrightness(bright)
        strip.show()
        time.sleep(wait_ms/1000.0)
   #     sleep(0.4)
#----------------------------------------------------
# Define functions which animate LEDs in various ways.
def colorWipe(strip, color):
    global gamma_a
    if debug: print "now in colorwipe"
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(delay/1000.0)
#------------------------------------------------------
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

# ---------------------
def colorWipe3(strip):
    global gamma_a
    if debug: print "Draw colorwipe3, color and then fade"

    max=255
    for i in range(striplen): 
        color=Color(max,0,0)
#        print max, gamma_a[max]
        strip.setPixelColor(i, color)
    
    bright=255
    for z in range (15):
 #       if debug: print "bright %d" % bright
        strip.setBrightness(bright)
        strip.show()
        bright=255-(z*255/15)    

        sleep(0.2)

    


#------------------------------------------------------        
def colorWipe6(strip, pattern, dir, patdir, oben, unten, colorback, bright=60):
    global gamma_a, debug

    i=0                     # count for number of show() calls
    lenpat=len(pattern)     # length of pattern
    
    if (unten > oben and oben !=TOP) or (oben > striplen):
        if debug: print "Error - unten/oben fehlerhaft (striplen %d %s/%s)" % (striplen, unten,oben)
        return(2)
      
    # setup    
    # define startposition
    if dir==DOWN:               # direction Down
        if oben == TOP:         # the full lenght
            startpos=striplen-1               # start here
        else:
            startpos=oben-lenpat   # not at bottom
    # setup
    # define loop counts   
        if oben == TOP and unten != BOTTOM:
            anzahl = startpos-unten+2
        elif oben == TOP and unten == BOTTOM:
            anzahl=striplen+lenpat
        elif  oben != TOP and unten == BOTTOM:
            anzahl=oben+1
        elif  oben != TOP and unten != BOTTOM:
            anzahl=oben-unten-lenpat+2
        
    else:       # direction is Up
    # define startposition
        if unten == BOTTOM:       # the full lenght
            startpos=-lenpat+1              # start here
        else:
            startpos=unten-1  # not at bottom
 
   # define loop counts   
        if oben == TOP and unten != BOTTOM:
            anzahl = (striplen-unten+1) +1
        elif oben == TOP and unten == BOTTOM:
            anzahl= (striplen+lenpat-1) +1
        elif  oben != TOP and unten == BOTTOM:
            anzahl= (oben-1) +1
        elif  oben != TOP and unten != BOTTOM:
            anzahl=oben-unten-lenpat+2
            
        
    if debug: print "colorwipe6 %s startpos %d loopcount %d lenpat %d" % (UPDOWN[dir],startpos, anzahl, lenpat)
     
    for z in range( 0, anzahl) :
        set=0
            
        if dir==DOWN:
            pos=startpos-z
        else:
            pos=startpos+z                # count backwards
 #           if pos1== 130: sleep(3)
        for pattind in range(lenpat): 
            if patdir==UP:
                pattindex=lenpat-pattind-1
            else:
                pattindex=pattind     
            pos1=pos+pattind
                
            if (pos1 >= 0) and (pos1 < striplen):
                if debugg: print "z: %d  position: %d patternindex: %d" % (z,pos1, pattindex)
                color=Color( pattern[pattindex][0] , pattern[pattindex][1], pattern[pattindex][2])
                strip.setPixelColor(pos1, color)
                set=1
        if (pos1+1) < striplen and dir==DOWN:           # set trailing led to black            
            strip.setPixelColor(pos1+1, Color(colorback[0],colorback[1],colorback[2]))
            if debugg: print "black at %d" % (pos1+1)
            set=1
        elif dir==UP and pos1-lenpat>=0:
            strip.setPixelColor(pos1-lenpat, Color(colorback[0],colorback[1],colorback[2]))
            if debugg: print "black at %d" % (pos1-lenpat)
            set=1
             
        if set:             # if a pixel was set
            if bright<90:
                strip.setBrightness(bright)

            strip.show()    # light them up
            i=i+1           # increment show counter
            set=0
       
        if debugg: print "show"
        time.sleep(delay/1000.0)    # delay
   
       #     sleep(1)  
    if debugg: print "Anzahl show %d: " % i 
    if debug: print "colorwipe6 %s startpos %d loopcount %d lenpat %d" % (UPDOWN[dir],startpos, anzahl, lenpat)
               
    return()            
   

#----------------------------------------------
# Main Loop
#---------------------------------------------
def main_loop():
    global  do_term

    i=0             # i contains image number
                    # images are in list images
    background=[0,0,0]
    
#  der loop läuft, bis ein Keyboard interrupt kommt, ctrl-c ----
    try:

        patt=make_rainbow(40)
        if debugg: print patt
        startpos=20
        for i in range(len(patt)):
            strip.setPixelColor(i+startpos, Color(patt[i][0],patt[i][1],patt[i][2]))
            strip.setBrightness(60)
        strip.show()
        sleep(0.1)

        sleep(2)
        clearled(BLACK)
        write_rainbow(strip,100, 30,0)     # paint rainbow at pos 90 in length 20
        write_rainbow(strip,20,30)
        sleep(10)
        clearled(BLACK)
        colorWipe2(strip)  # Red wipe
        sleep(2)
        clearled(BLACK)
        colorWipe3(strip)  # Red wipe
        sleep(2)
        strip.setBrightness(80)

        clearled(BLACK)
        colorWipe6(strip,patt,UP,UP,60,BOTTOM,background)  # Red wipe
        sleep(0.2)
        clearled(BLACK)
        colorWipe6(strip,patt,DOWN,UP,60,BOTTOM,background)  # Red wipe
        sleep(0.4)
        colorWipe6(strip,patt,DOWN,DOWN,TOP,60,background)  # Red wipe
        sleep(0.2)
        clearled(BLACK)
        colorWipe6(strip,patt,UP,DOWN,TOP,40,background)  # Red wipe

        sleep(0.1)
        clearled(BLACK)
        background=[0,0,0]


        background=[30,10,20]
        clearled(background)
        colorWipe6(strip,pattern3,DOWN,UP,TOP,19,background)  # Red wipe
        sleep(0.3)
        clearled(BLACK)
    

        rainbow(strip,20,100)
        sleep(3)

        clearled(BLACK)
        rainbowCycle(strip)
        sleep(1)
        clearled(BLACK)
        
        rainbowCycle(strip,80,130)
        sleep(1)


        clearled(BLACK)
    except KeyboardInterrupt:
    # aufräumem
        print ("\nKeyboard Interrupt in butest")
        do_term=1
    pass                        
    clearled(BLACK)

    return(0)    
#---- End Main Loop -------------------------------------------------------------


# *************************************************
# Program starts here
# *************************************************

if __name__ == '__main__':
#
    arguments(sys.argv[1:])  # get commandline arguments
    if debug: print "Run with debug"
    initpgm()
    
    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
    # Intialize the library (must be called once before other functions).
    strip.begin()

    blink_led(led_green,2)      # blink led 2 mal while waiting
    

    main_loop()                 # work is done in main_loop()
                                # return from mainloop if Ctrl-C on Keyboard

# 
#  Clean-Up and terminate

    GPIO.cleanup(led_rot)
    GPIO.cleanup(led_green)
    GPIO.cleanup(red_button)
    GPIO.cleanup(black_button)

    print ("Program terminated....")
    sys.exit(0)
    
#**************************************************************
#  That is the end
#***************************************************************
#


  