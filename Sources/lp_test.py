#!/usr/bin/python
# coding: utf-8
#----------------------------------------------------------
#   Test Function  Light Painting System
#   Draws some pattern on the pixelsick
#
#   Based on several examples found on the Adafruit Learning System
#   
#   Peter K. Boxler, February 2015
# ------------------------------------------------------

import lp_defglobal
from time import sleep
from lp_sub import *
from lp_patt import *

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

#------------------------------------------------
def do_test(strip,GPIO):

    while True:
        msg_type=list()
        if lp_defglobal.debug: print "Do_test"
        msg_type.append("--- Test Led ---")
        msg_type.append("Black:No Red:Yes")
        showmsg(msg_type)
        sleep(0.5)
        ret=button_pressed(GPIO)
        if lp_defglobal.debug: print "Test Return: %s" % lp_defglobal.but[ret]
        sleep(0.1)                          # for testing
        if (ret==lp_defglobal.SETUP or ret==lp_defglobal.BLACK):
            sleep(0.5)
            return(0)
        
        msg_type[1]="-> Doing Test <-" 
        showmsg(msg_type)
        colorWipe2(strip)  # Red wipe
        sleep(2)
        set_led(strip,lp_defglobal.BLACKCOL)
        patt=rainbowMakePatt(40)
        if lp_defglobal.debugg: print patt
        startpos=20
        for i in range(len(patt)):
            strip.setPixelColor(i+startpos, Color(patt[i][0],patt[i][1],patt[i][2]))
            strip.setBrightness(60)
        strip.show()
        sleep(0.1)
        
        rainbowStatic(strip,120, 40)     # paint rainbow at pos 90 in length 20
        rainbowStatic(strip,70,15)
        sleep(1)
        set_led(strip,lp_defglobal.BLACKCOL)
        pattRun(strip,lp_defglobal.brightness,patt,UP,UP,60,BOTTOM,lp_defglobal.BLACKCOL)  # Red wipe
        sleep(0.2)
        set_led(strip,lp_defglobal.BLACKCOL)
        pattRun(strip,lp_defglobal.brightness,patt,DOWN,UP,60,BOTTOM,lp_defglobal.BLACKCOL)  # Red wipe
        sleep(0.4)
        pattRun(strip,lp_defglobal.brightness,patt,DOWN,DOWN,TOP,60,lp_defglobal.BLACKCOL)  # Red wipe
        sleep(0.2)
        set_led(strip,lp_defglobal.BLACKCOL)
        pattRun(strip,lp_defglobal.brightness,patt,UP,DOWN,TOP,40,lp_defglobal.BLACKCOL)  # Red wipe
        set_led(strip,[30,10,20])
        pattRun(strip,lp_defglobal.brightness,pattern3,DOWN,UP,TOP,19,[30,10,20])  # Red wipe
        sleep(0.3)
        set_led(strip,lp_defglobal.BLACKCOL)
        savedelay=lp_defglobal.column_delay_time
        lp_defglobal.column_delay_time=10
        mytheaterChase(lp_defglobal.strip,20,0,lp_defglobal.brightness )  # Red theater chase
        lp_defglobal.column_delay_time=savedelay
        set_led(lp_defglobal.strip,lp_defglobal.BLACKCOL)                      # set all pixels to BLACK


        
        sleep(3)
        set_led(strip,lp_defglobal.BLACKCOL)

    pass
#------------------------------------------------------------
    
    
