#!/usr/bin/python
# coding: utf-8
#----------------------------------------------------------
#   Draw Pattern Functions 1 for the Light Painting System
#
#   Peter K. Boxler, February 2015
#
#   NeoPixel Products here: 
#   ----> https://www.adafruit.com/products/1506
#-----------------------------------------------------------
#
import sys, getopt, os
import time, math
from time import sleep
import RPi.GPIO as GPIO
from neopixel import *
import random
import lp_defglobal
import lp_defpattern
from time import sleep
from lp_sub import *

onoff={1:'ON', 0:'OFF'}

gamma   =2.8            # gamma correction
gamma_a=(list)          # list of gamma corrections for every brightness 0-255

debugg=0
delay=20

BOTTOM=-1
TOP=-1
UP=1
DOWN=0
FULL=-2
UPDOWN={1:'UP', 0:'DOWN'}
#

# ---------------------------------------------------------	
def float_to_hex(f):
    return hex(struct.unpack('<I', struct.pack('<f', f))[0])
#----------------------------------------------------------
  

#--------- Function rainbow-orig (orignal version) -------
#   draw static rainbow, from strandtest script
#----------------------------------------------------------
def rainbow_orig  (strip):
    if lp_defglobal.debug: print "rainbow-orig that fades across all pixels at once."
    for j in range(256*lp_defglobal.iteration_pattern):
        for i in range(lp_defglobal.striplen):
            strip.setPixelColor(i, wheel((i+j) & 255))
        strip.setBrightness(80)
        strip.show()
        time.sleep((lp_defglobal.column_delay_time)/1000.0)        # in Miliseconds
#--------------------------------------------------------    


# --  Function rainbowStatic ----------------------------------
#   generate a static rainbow pattern with lenght len, starting at pos
#   Colorwheel wheel() is used, max. 256 colors.
# ------------------------------------------------------------
def rainbowStatic (strip, start, len, type=0, bright=60):
    if lp_defglobal.debug: 
        print "rainbowStatic  start %d len %d bright %d" % (start,len,bright)    
    #   use pixel start to start+len 
        
    for i in range( 0,len):
        if i < lp_defglobal.striplen:
            strip.setPixelColor(start+i, wheel((i+i*256/len) & 255))
    strip.setBrightness(bright)
    strip.show()
        
    if type:
        while True:
            if GPIO.input(lp_defglobal.red_button):
                sleep(0.2)
                pass
            else: break
    else:
        sleep(5)
        return()
    pass

#--------------------------------------------------------    


# --  Function rainbowMakePatt ----------------------------------
#   return a rainbow pattern with lenght len
#   Colorwheel wheel() is used, max. 256 colors
#---------------------------------------------------------------
def rainbowMakePatt(len):
    if lp_defglobal.debug: print "rainbowMakePatt  pattern lenght %d" % len
    pat=[]
    for i in range( 0,len):
        pat.append(wheel((i+i*256/len) & 255,1))
    return(pat)
#--------------------------------------------------------    

    
# --  Function rainbowCycle ----------------------------------
#   Write a Rainbow that cycles over a number of pixels
#   max. 256 colors    
#-----------------------------------------------    
def rainbowCycle (strip, bright=60,type=0,start=FULL, end=-1  ):
    if start==FULL:
        start=0
        end=lp_defglobal.striplen
    elif end == -1:
        print "rainbow: end not defined"
        return()
    ctr=end-start
    
    if type:
        iter=100
    else:
        iter=lp_defglobal.iteration_pattern
    
    if lp_defglobal.debug: print "rainbowCycle  type %d start %d end %d iter: %d  bright: %d" \
        % (type, start, end, iter, bright)
    
    for j in range(256 * iter):
        for i in range(ctr):
            strip.setPixelColor(i+start, wheel((i+j) & 255))
        strip.setBrightness(bright)
        strip.show()
        time.sleep((lp_defglobal.column_delay_time)/1000.0) 
    
        if type: 
            if GPIO.input(lp_defglobal.red_button):
                pass
            else: break
        pass
#--------------------------------------------------------    


#---Function rainbowTime ----------------------
#   write rainbow over time, all pixels change   
#   max. 256 colors    
#-----------------------------------------------    
def rainbowTime(strip, type=0, startcol=0,start=FULL,bright=150  ):
    if lp_defglobal.debug: print "rainbowTime  type %d start %d  iter: %d  bright: %d" \
        % (type, start,  lp_defglobal.iteration_pattern, bright)
    
    start=startcol
    i=0
    z=start
    while True:
        if z>255:
            z=0
            start=0           
#        print "z %d i %d" % (z,i)
        colo=wheel(z,1)
        set_led(lp_defglobal.strip,colo,bright) 
                    # set all pixels to BLACK
        time.sleep((lp_defglobal.column_delay_time)/1000.0)        # in Miliseconds
        i=i+1
        z=z+1
        if type: 
            if GPIO.input(lp_defglobal.red_button):
                pass
            else: break
        else:
            if i > (255 * lp_defglobal.iteration_pattern) : break
 
        pass

    pass
#-----------------------------------------------------------        

#---Function rainbowTime2 ----------------------
#   write rainbow over time, all pixels change   
#   max. 1056  colors    
#-----------------------------------------------    
def rainbowTime2 (strip, fro, to,type=0,bright=60  ):
    if lp_defglobal.debugg: print "rainbowTime2  type %d start %d  iter: %d  bright: %d" \
        % (type,start,  lp_defglobal.iteration_pattern, bright)
    
    i=0
    luminace=50
    lp_defglobal.set_led_parm[0]=fro
    lp_defglobal.set_led_parm[1]=to
    lp_defglobal.set_led_parm[3]=bright

    while True:          
#        print "z %d i %d" % (z,i)
        colo=color_wheel_r (lp_defglobal.debug,i , luminace)     # get rgb values
        if colo[0] == -99:
            if type: 
                i=0
                continue
            else: break
        lp_defglobal.set_led_parm[2]=colo[1]
#        print i,lp_defglobal.set_led_parm

        set_led2(lp_defglobal.strip,lp_defglobal.set_led_parm) 
                    # set all pixels to BLACK
        time.sleep((lp_defglobal.column_delay_time)/1000.0)        # in Miliseconds
        i=i+1
        if type: 
            if GPIO.input(lp_defglobal.red_button):
                pass
            else: break 
        pass
    pass
#-----------------------------------------------------------   

# - pattDraw_11 -------------------------------------------
#   light all pixels defined in def pixpatt2: block of pixels are defined
#   color the blocks round the wheel
#   Parameter patt defines pattern in pixpatt2[]
#   parameter type specifies termination: 1: wait for red button,  0: iterate
#-----------------------------------------------------------        
def pattDraw_11 (strip, patt, color, type , bright=50):
    if lp_defglobal.debug: print "pattDraw_11 type %d iter: %d  bright: %d" \
        % (type, lp_defglobal.iteration_pattern, bright)

    anzstripe = len (lp_defpattern.pixpatt2[patt])         # number of blocks of pixels
  
    if lp_defglobal.debug: print "number of blocks %d" % anzstripe

    for i in range (anzstripe):
        color=wheel(i*(255/anzstripe),1)
        for y in lp_defpattern.pixpatt2[patt][i]:          # pixels in block i
            strip.setPixelColor(y, Color(color[0],color[1],color[2]))
    strip.setBrightness(bright)
    strip.show()
    
    if type:                # 1= wait for red button
        while True:
            if GPIO.input(lp_defglobal.red_button):
                sleep(0.4)
            else: 
                return(0)
    else:                   #  iterate
        sleep( 7 * lp_defglobal.iteration_pattern)
 
        pass

    return(0)
#--------------------------------------------------------    
     
# - pattDraw_12 -------------------------------------------
#   light all pixels defined in pixpatt[n]
#   type specifies type of action
#   1: blink (reverse pixel)
#   2: blink (same pixels) interate, then quit
#   3: blink (same pixels), iterate until red button pressed
#-----------------------------------------------------------        
def pattDraw_12 (strip, color, patt=0 , type=0, bright=50,ontime=500):
    pix1=list()             # lit pixels are store as 1 - so we can light up the zeros later
                            # for blinking inverse pattern
    
    if lp_defglobal.debug: print "pattDraw_1x patt: %d type: %d  iter: %d  bright: %d" \
        % (patt, type,  lp_defglobal.iteration_pattern, bright)
    for z in range (lp_defglobal.striplen):
        pix1.append(0)
    loopctr=8 * lp_defglobal.iteration_pattern
    if type==2: loopctr=50          # set loopctr for manual off
    first=1
#
# for all types: light up the pixels specified in pixpatt[patt]
#
    for x in range (loopctr):             #  8 times is 19 seconds
        if lp_defglobal.debugg: print "x %d" % x
        i=1
        for j in lp_defpattern.pixpatt[patt]:
            if lp_defglobal.debugg: print "---- j  %d" % j
            if first:
                pix1[j]=1           # this pixel lit - save this info
            strip.setPixelColor(j, Color(color[0],color[1],color[2]))
        strip.setBrightness(bright)
        strip.show()
        first=0
        sleep(ontime/1000.0)    # keep them on for ontime ms
        
        set_led(lp_defglobal.strip,lp_defglobal.BLACKCOL)    # set all pixels to BLACK
                
#   pattern cleared again - check what to do next

        if type==0:                 # blink with inverse pixels
        
            for z in range (lp_defglobal.striplen):
                if pix1[z]==0:              # only light up pixels not previously lit (inverse pattern)
                    if lp_defglobal.debugg: print "---- j  %d" % j
                    strip.setPixelColor(z, Color(color[0],color[1],color[2]))
            strip.setBrightness(bright)
            strip.show()
            sleep(0.5)
            set_led(lp_defglobal.strip,lp_defglobal.BLACKCOL)                      # set all pixels to BLACK
  #          sleep(0.3)

        elif type==1:               # blink with same pixels
            sleep(0.2)
            pass

        elif type==2:                # stay until red button
            sleep(0.1)
            if GPIO.input(lp_defglobal.red_button):
                sleep(0.1)
                pass
            else:                     # clear all and return
#                set_led(lp_defglobal.strip,lp_defglobal.BLACKCOL)                      # set all pixels to BLACK
                sleep(0.1)
                return(0)
              
    pass
    if lp_defglobal.debug: print "pix1-array cleared"
    pix1=[]
    pass
#-----------------------------------------------------------------

# - pattDraw_13 -------------------------------------------
#   light all pixels defined in pattern pixpatt3(i)[n]
#   color is defined in pixpatt3[i][n+1] 
#   wait for red button
#-----------------------------------------------------------        
def pattDraw_13 (strip, patt, bright=50):
    if lp_defglobal.debug: print "pattDraw_13  iter: %d  bright: %d" \
        % (  lp_defglobal.iteration_pattern, bright)

        
    for x in range (7 * lp_defglobal.iteration_pattern):             #  7 times is 19 seconds
        if lp_defglobal.debugg: print "x %d" % x
        i=0
        for j in lp_defpattern.pixpatt3[patt][0]:
            if lp_defglobal.debugg: print "---- j  %d" % j
                
            strip.setPixelColor(j, Color(lp_defpattern.pixpatt3[patt][1][i][0], \
                lp_defpattern.pixpatt3[patt][1][i][1],  \
                lp_defpattern.pixpatt3[patt][1][i][2]))
            i=i+1
        strip.show()
        while True:
            if GPIO.input(lp_defglobal.red_button):
                pass
                sleep(0.2)
            else: break
        pass
        
#    set_led(strip,lp_defglobal.BLACKCOL)
    return(0)
#--------------------------------------------------------    


# Function mytheaterChase  ------------------------------
# lights up pixels as on a Movie Theater Display
# parameter type specifies termination: 1= wait for red button
# -------------------------------------------------------
def mytheaterChase (strip,step,type=0, bright=100):
    
    if lp_defglobal.debug: 
        print "Movie theater light style chaser animation."
    if type:
        iter=100
    else:
        iter=7
        
    for q in range(iter):
        for j in range(5):
            for q in range(3):
                for i in range(0, lp_defglobal.striplen, 3):
                    color=Color(random.randrange(1, 255, step), random.randrange(1, 255, step),random.randrange(1, 255, step) )
                    lp_defglobal.strip.setPixelColor(i+q, color)
                lp_defglobal.strip.setBrightness(bright)
                lp_defglobal.strip.show()
            
                time.sleep(lp_defglobal.column_delay_time/1000.0)
            
                for i in range(0, lp_defglobal.striplen, 3):
                    lp_defglobal.strip.setPixelColor(i+q, 0)
        pass
        if type: 
            if GPIO.input(lp_defglobal.red_button):
                pass
                sleep(0.1)
            else: break
        pass
        
    pass
#    set_led(strip,lp_defglobal.BLACKCOL)
    return(0)
#--------------------------------------------------------    

    
# Function mytheaterChaseRainbow  ------------------------------
# lights up pixels as on a Movie Theater Display
# -------------------------------------------------------
def theaterChaseRainbow(strip, bright=100):
    if lp_defglobal.debug: 
        print "theaterChaseRainbow :Rainbow movie theater light style chaser animation."
    
    stop=0
    while True:
        if stop: break

        for j in range(256):
            if stop: break
            for q in range(3):
                for i in range(0, lp_defglobal.striplen, 3):
                    strip.setPixelColor(i+q, wheel((i+j) % 255))
                strip.setBrightness(bright)
                strip.show()
                time.sleep(lp_defglobal.column_delay_time/1000.0)
                for i in range(0, lp_defglobal.striplen, 3):
                    strip.setPixelColor(i+q, 0)
                if GPIO.input(lp_defglobal.red_button):
                    pass
                else: 
                    stop=1
                    break
        pass
    set_led(strip,lp_defglobal.BLACKCOL)
#--------------------------------------------------------    



#  Function rainbowCycle ----------------------------------
#   draw rainbow and cycle it over all pixels    
#   parameter type specifies termiantion: 1= wait for red button
#-----------------------------------------------------------        
def rainbowCycle_orig(strip, type=0, start=FULL, end=-1, bright=60  ):
    if start==FULL:
        start=0
        end=lp_defglobal.striplen
    elif end == -1:
        print "rainbow: end not defined"
        return()
    ctr=end-start
    
    if type:
        iter=100
    else:
        iter=lp_defglobal.iteration_pattern
        
    if lp_defglobal.debug: print "rainbowCycle  type %d iter: %d  bright: %d" % (type,iter, bright)
    for j in range(256*iter):
        for i in range(ctr):
            strip.setPixelColor(i+start, wheel(((i * 256 / 150) + j) & 255))
        strip.setBrightness(bright)
        strip.show()
        time.sleep((lp_defglobal.column_delay_time)/1000.0)        # in Miliseconds
        
        if type: 
            if GPIO.input(lp_defglobal.red_button):
                pass
            else: break
        pass
#--------------------------------------------------------    
        

#  Function colorWipe ---------------------------
#   original function from strandtest script
#------------------------------------------------
# Define functions which animate LEDs in various ways.
def colorWipe(strip, color):
    if lp_defglobal.debug: print "colorwipe  ----"
    """Wipe color across display a pixel at a time."""
    for i in range(lp_defglobal.striplen):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(delay/1000.0)
#--------------------------------------------------------    



#  Function colorWipe2 ---------------------------
#   original function from strandtest script
#------------------------------------------------
# Define functions which animate LEDs in various ways.
def colorWipe2(strip):

    if lp_defglobal.debug: print "colorwipe2 ----------"

    step=int(255/(lp_defglobal.striplen/3))              # Helligkeits step
    if lp_defglobal.debug: print "step: %d " % step
    
    if lp_defglobal.debug: print "now red"
    max=255
    for i in range(lp_defglobal.striplen/3): 
        color=Color(lp_defglobal.gamma_a[max],0,0)
#        print max, gamma_a[max]
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep((lp_defglobal.column_delay_time)/1000.0)        # in Miliseconds
        max=255-(i*step)
#        print "i: %d max: %d" % (i,max)    
        
    max=255
    y=0
    if lp_defglobal.debug: print "now blue"
    for i in range(lp_defglobal.striplen/3,2*lp_defglobal.striplen/3): 
        
        color=Color(0,0,lp_defglobal.gamma_a[max])
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep((lp_defglobal.column_delay_time)/1000.0)        # in Miliseconds
        max=255-(y*step)
        y=y+1
#    print i,max

    max=255
    y=0
    if lp_defglobal.debug: print "now green"
    for i in range(2*lp_defglobal.striplen/3,lp_defglobal.striplen): 
        
        color=Color(0,lp_defglobal.gamma_a[max],0)
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep((lp_defglobal.column_delay_time)/1000.0)        # in Miliseconds
        max=255-(y*step)
        y=y+1
#        print "i: %d max: %d" % (i,max)    
#
    set_led(strip,lp_defglobal.BLACKCOL)

    if lp_defglobal.debug: print "now red umgekehrt"
    i=0
    max=0
    for i in range(lp_defglobal.striplen/3): 

        color=Color(lp_defglobal.gamma_a[max],0,0)
#        print max, gamma_a[max]

        strip.setPixelColor(i, color)
        strip.show()
        i=i+1
        time.sleep((lp_defglobal.column_delay_time)/1000.0)        # in Miliseconds
        max=0+(i*step)
        time.sleep((lp_defglobal.column_delay_time)/1000.0)        # in Miliseconds

     #   print "i: %d max: %d" % (i,max)    
    if lp_defglobal.debug: print "Anzahl show %d: " % i                
    return(0)    
#--------------------------------------------------------    


#  function pattFade  ----------------------------------
#   light up all pixels to brightness 255 and then fade
#   colo specifies color [r,g,b]
#   parameter type specifies fade type: 0=fade down / 1=fade up
# ------------------------------------------------------
def pattFade (strip,colo, type=0):

    if lp_defglobal.debug: print "pattFade, type %d" % type

    bright=255
    for j in range(lp_defglobal.iteration_pattern):

        for y in range(4):
            max=255
            for i in range(lp_defglobal.striplen): 
                color=Color(colo[0],colo[1],colo[2])
#        print max, gamma_a[max]
                strip.setPixelColor(i, color)

            if type==0:         # fade down
                bright=255
                for z in range (15):
 #       if lp_defglobal.debug: print "bright %d" % bright
                    strip.setBrightness(bright)
                    strip.show()
                    bright=255-(z*255/15)    
                    sleep(0.2)
            else:               # fade up
                bright=0
                for z in range (15):
                    if lp_defglobal.debugg: print "bright %d" % bright
                    strip.setBrightness(bright)
                    strip.show()
                    bright=0+(z*255/15)    
                    sleep(0.2)
        pass
    pass
#--------------------------------------------------------    
    

#  Function pattRun  ---------------------------------
# run a pattern up/down the pixels strip
#   parameter pattern defines pattern to be used
#   parameter dir specifies direction up/down
#   parameter colorback specifies color to set after pattern passed
#---------------------------------------------------------------        
def pattRun (strip, bright, pattern, dir, patdir, oben, unten, colorback):


    i=0                     # count for number of show() calls
    lenpat=len(pattern)     # length of pattern
    
    if (unten > oben and oben !=TOP) or (oben > lp_defglobal.striplen):
        if lp_defglobal.debug: print "Error - unten/oben fehlerhaft (lp_defglobal.striplen %d %s/%s)" % (lp_defglobal.striplen, unten,oben)
        return(2)
      
    # setup    
    # define startposition
    if dir==DOWN:               # direction Down
        if oben == TOP:         # the full lenght
            startpos=lp_defglobal.striplen-1               # start here
        else:
            startpos=oben-lenpat   # not at bottom
    # setup
    # define loop counts   
        if oben == TOP and unten != BOTTOM:
            anzahl = startpos-unten+2
        elif oben == TOP and unten == BOTTOM:
            anzahl=lp_defglobal.striplen+lenpat
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
            anzahl = (lp_defglobal.striplen-unten+1) +1
        elif oben == TOP and unten == BOTTOM:
            anzahl= (lp_defglobal.striplen+lenpat-1) +1
        elif  oben != TOP and unten == BOTTOM:
            anzahl= (oben-1) +1
        elif  oben != TOP and unten != BOTTOM:
            anzahl=oben-unten-lenpat+2
            
        
    if lp_defglobal.debug: print "pattRun %s startpos %d loopcount %d lenpat %d" % (UPDOWN[dir],startpos, anzahl, lenpat)

     
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
                
            if (pos1 >= 0) and (pos1 < lp_defglobal.striplen):
                if lp_defglobal.debugg: print "z: %d  position: %d patternindex: %d" % (z,pos1, pattindex)
                color=Color( pattern[pattindex][0] , pattern[pattindex][1], pattern[pattindex][2])
                strip.setPixelColor(pos1, color)
                set=1
        if (pos1+1) < lp_defglobal.striplen and dir==DOWN:           # set trailing led to black            
            strip.setPixelColor(pos1+1, Color(colorback[0],colorback[1],colorback[2]))
            if lp_defglobal.debugg: print "black at %d" % (pos1+1)
            set=1
        elif dir==UP and pos1-lenpat>=0:
            strip.setPixelColor(pos1-lenpat, Color(colorback[0],colorback[1],colorback[2]))
            if lp_defglobal.debugg: print "black at %d" % (pos1-lenpat)
            set=1
             
        if set:             # if a pixel was set
            if bright<90:
                strip.setBrightness(bright)

            strip.show()    # light them up
            i=i+1           # increment show counter
            set=0
       
        if lp_defglobal.debugg: print "show"
        time.sleep((lp_defglobal.column_delay_time)/1000.0)        # in Miliseconds
   
       #     sleep(1)  
    if lp_defglobal.debugg: print "Anzahl show %d: " % i 
    if lp_defglobal.debug: print "pattRun %s startpos %d loopcount %d lenpat %d" % (UPDOWN[dir],startpos, anzahl, lenpat)
               
    return()            
#--------------------------------------------------------    


# --  Function rainbowStatic2 OLD OLD-------------------------
# replaced by rainbowTime2  <<-----------------------
#   generate a static rainbow across all pixels
#   Colorwheel with 1536 is used
#---------------------------------------------------------------
def rainbowStatic2 (strip, bright=255,luminace=50):
    colog=list()
    i=0
    if lp_defglobal.debug: 
        print "rainbowStatic2  lumi %d bright: %d" % (luminace, bright)
    
    while True:                             # function color_wheel signals termination     
        colo=color_wheel_r (lp_defglobal.debug,i , luminace)     # get rgb values
        if colo[0] < 0:                        # loop terminates, all colors done
            break   
        colog.append(lp_defglobal.gamma_a[colo[1][0]])      # gamma correction
        colog.append(lp_defglobal.gamma_a[colo[1][1]])
        colog.append(lp_defglobal.gamma_a[colo[1][2]])
        
        for j in range(strip.numPixels()):  
            strip.setPixelColor(j,Color(colog[0],colog[1],colog[2]))
        strip.setBrightness(bright)
        strip.show()
        colog=[]
        if lp_defglobal.debug:           # print color values
            text='{:<4}'.format(i) + "  " \
            +   '{:>3}'.format(str(colo[1][0])) + " "\
            +   '{:>3}'.format(str(colo[1][1])) + " "\
            +   '{:>3}'.format(str(colo[1][2]))
            print text
      
        i=i+1
    if lp_defglobal.debug: print "Number of shows %d" % i
#---------------------------------------------------------


#**************************************************************
#  That is the end
#***************************************************************
#


  