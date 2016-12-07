#!/usr/bin/python
# coding: utf-8
#----------------------------------------------------------
#   Draw Pattern Functions 2 for the Light Painting System
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
import lp_defpattern2
from time import sleep
from lp_sub import *

gamma   =2.8            # gamma correction
gamma_a=(list)          # list of gamma corrections for every brightness 0-255

debugg=0
delay=20
UPDOWN={1:'UP', 0:'DOWN', 2:'CONST'}
DIRECTION={'u':1, 'd':0, 'c':2}
colo1=list()
colo2=list()
colonow=list()
    

# - pattDraw_21 -------------------------------------------
#   light all pixels defined in pattern def
#   parameter pat_type specifies type of pattern in pixpatt1()
#   parameter col_type specifies colors to be used from pixcolor()
#-----------------------------------------------------------        
def draw_pattern_21 (strip, pat_type=0,col_type=0, bright=255 ):

    if lp_defglobal.debug: 
        print "draw_pattern_3  pat %d col %d bright: %d" \
            % (pat_type, col_type, bright)
    
    global colo1, colo2, colonow
    i=0
    colonow=[]      
    loopctr=lp_defpattern2.pixcolor[col_type][0][0] 
    firstcol=lp_defpattern2.pixcolor[col_type][1][0]             # first color
    firstcolum=lp_defpattern2.pixcolor[col_type][1][1]
    firstcol_dir=DIRECTION[ lp_defpattern2.pixcolor[col_type][1][2]]
    seccol=lp_defpattern2.pixcolor[col_type][2][0]               # second color
    seccolum=lp_defpattern2.pixcolor[col_type][2][1]
    seccol_dir=DIRECTION[ lp_defpattern2.pixcolor[col_type][2][2]]
 
# which on goes up ?
    if lp_defglobal.debug: 
        print "loopctr: %d  color1: %d/%d/%s color2: %d/%d/%s" % (loopctr,firstcol, firstcolum, UPDOWN[firstcol_dir], seccol, seccolum, UPDOWN[seccol_dir])
        print "number of groups ", len (lp_defpattern2.pixpatt1[pat_type])  
  
    y1=0             # adjust for round robin
    z1=0
    y2=0
    z2=0
    
# loop for all colors defined by loopctr in color definition 
    for x in range (loopctr+1):

# check direction first color
        if firstcol_dir == 1:               # first color increments
            ctr_colo1=x+firstcol-y1
        elif firstcol_dir ==0:              # first color decrements
            ctr_colo1= firstcol-x+z1 
        else:                               # first color stays constant
            ctr_colo1= firstcol
            pass
# check direction seccond color
        if seccol_dir ==1:                  # second color increments
            ctr_colo2=x+seccol-y2
        elif seccol_dir ==0:                # second color decrements
            ctr_colo2= seccol-x+z2 
        else:                               # second color stay constant
            ctr_colo2=seccol
            pass

#  loop runs for every line in the selected pattern -------    
        for j in range  (0,len(lp_defpattern2.pixpatt1[pat_type])):
            if lp_defglobal.debug: print "--------------- Patt-Index %d --------------------" % j
            
#  loop for all pixels in the current line
            for i in range ( lp_defpattern2.pixpatt1[pat_type][j][1] - lp_defpattern2.pixpatt1[pat_type][j][0]   + 1) :
                i=i+lp_defpattern2.pixpatt1[pat_type][j][0]
                if lp_defglobal.debugg: print ".............. pixel  %d ..............." % i

#   check if line specifies first or second color
                if lp_defpattern2.pixpatt1[pat_type][j][2][0] == 300 :
#    300 means: color1 
                    colo1=color_wheel_r (lp_defglobal.debug, ctr_colo1 ,firstcolum)      # get rgb for this colorwheel position, first color
                    colonow=colo1[1]
                    retu=colo1[0]
                                      
                elif lp_defpattern2.pixpatt1[pat_type][j][2][0] == 400:
#   400 means second color
                    colo2=color_wheel_r (lp_defglobal.debug, ctr_colo2 ,seccolum)       # get rgb for this colorwheel position, second color
                    colonow=colo2[1]   
                    retu=colo2[0]
  
#  color definition defines constant colors   
                else:
                    colonow.append(lp_defpattern2.pixpatt1[pat_type][j][2][0])
                    colonow.append(lp_defpattern2.pixpatt1[pat_type][j][2][1])
                    colonow.append(lp_defpattern2.pixpatt1[pat_type][j][2][2])
                    pass
# set the pixel    
                if lp_defglobal.debug: print "set pixel: %d  loopctr: %d  col1: %d  col2 %d  %d %d %d" % (i, x, ctr_colo1,ctr_colo2,colonow[0],colonow[1],colonow[2])
                pass            
                strip.setPixelColor(i,Color(colonow[0],colonow[1],colonow[2]))
                colonow=[]               
        pass
        strip.setBrightness(bright)
        strip.show()
        if loopctr > 200:
            sleep(5/1000.0)
        else:
            sleep(20/1000.0)
        if lp_defglobal.debug: print "do show ************************************************************** do show ******"

    pass
    if lp_defglobal.debug:
        print "last color 1 " ,colo1
        print "last color 2 ", colo2
#-----------------------------------------------------------   

# - Function prepCol_1  ------------------------------
#   fills savecollist() with rainbow colors with step 35
#------------------------------------------------------
def prepCol_1():

    save=list()
    step=44
    ledcount=4
    for i in range (35):
        necol=1540-(i*step)
        color=color_wheel_r (lp_defglobal.debug, necol ,50)
        if lp_defglobal.debug:
            text='{:<4}'.format(i) + "  " \
            +   '{:>4}'.format(str(necol)) + " "\
            +   '{:>3}'.format(str(color[1][0])) + " "\
            +   '{:>3}'.format(str(color[1][1])) + " "\
            +   '{:>3}'.format(str(color[1][2]))  + "  " \
            +   '{:>3}'.format(str(lp_defglobal.gamma_a[color[1][0]])) + " "\
            +   '{:>3}'.format(str(lp_defglobal.gamma_a[color[1][1]])) + " "\
            +   '{:>3}'.format(str(lp_defglobal.gamma_a[color[1][2]]))

            print text
        for j in range (ledcount-1):
            led=j+(i*ledcount)
            lp_defglobal.savecollist.append(Color(lp_defglobal.gamma_a[color[1][0]],lp_defglobal.gamma_a[color[1][1]],lp_defglobal.gamma_a[color[1][2]]))

        lp_defglobal.savecollist.append(Color(0,0,0))
    
#--------------------------------------------------

# - Function showCol ---------------------------------
#   lights up pixels with colors defined in savecollist()
#------------------------------------------------------
def showCol(strip):

    step=44
    for i in range (len(lp_defglobal.savecollist)):
            strip.setPixelColor(i,lp_defglobal.savecollist[i])
    
    strip.show()  
#--------------------------------------------------


#------------------------------------------------------
def showCol_blink(strip,on=300,off=100):

    for z in range(lp_defglobal.iteration_pattern):
        for z in range (20):
            for i in range (len(lp_defglobal.savecollist)):
                strip.setPixelColor(i,lp_defglobal.savecollist[i])
            strip.show()  
            sleep(on/1000.0)    
            set_led(lp_defglobal.strip,lp_defglobal.BLACKCOL)                      # set all pixels to BLACK
            sleep(off/1000.0)
#--------------------------------------------------

        

#**************************************************************
#  That is the end
#***************************************************************
#


  