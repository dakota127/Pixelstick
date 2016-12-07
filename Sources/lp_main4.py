#!/usr/bin/python
# coding: utf-8
#----------------------------------------------------------
#   Draw Text Main Loop for the Light Painting System
#
#   Peter K. Boxler, February 2015
#
#   NeoPixel Products here: 
#   ----> https://www.adafruit.com/products/1506
#-----------------------------------------------------------
#

import sys, getopt, os
from time import sleep
import time, datetime
import lp_defglobal
from neopixel import *
import random
from lp_sub import *
from lp_setup import *
from PIL import Image
import struct
from neopixel import *
from threading import Thread
from PIL import ImageDraw
from PIL import ImageFont
import cStringIO
from math import floor

charsbelow = set('gjpqpy')   # char that go below baseline

# ---------------------------------------------------------

def getSize(txt, font):
    testImg = Image.new('RGB', (1, 1))
    testDraw = ImageDraw.Draw(testImg)
    return testDraw.textsize(txt, font)

#-----------------------------------
def dirstring():        # second line of display
    if lp_defglobal.direction_flag==1:
            ab='{:^5}'.format(str(lp_defglobal.waitdraw) + lp_defglobal.direction[lp_defglobal.direction_flag])
    else:
        ab='{:^5}'.format( lp_defglobal.direction[lp_defglobal.direction_flag] + str(lp_defglobal.waitdraw) )
    return (ab)
#--------------------------------

    
##----------------------------------------------
# Main Loop Typ 3
#---------------------------------------------
def main_loop_type4(GPIO):
    global images
    
    while True:         # run forever - ctrl-C interrupts
                        # check termination in variable lp_defglobal.do_term    
        if lp_defglobal.debug:
            print "Type 3 starting while loop"
        if  lp_defglobal.do_term: break             # break from main Loop
        if  lp_defglobal.type_switch: break             # break from main Loop

        if lp_defglobal.debug: print "doing type 3"
        sleep(0.5)
        fontname = "Optima.ttc"   
        text = "Hello World"

        colorText = "white"
        colorOutline = "black"
        colorBackground = "black"
        lp_defglobal.msg_line[0]=" Enter Text"            
        lp_defglobal.msg_line[1]=" "
        showmsg( lp_defglobal.msg_line)                 # show  on led display
        sleep(0.5)

        text = raw_input("Give me some text ")
    
        if any((c in charsbelow) for c in text):
            fontsize=122                # found characters the go below baseline
        else:
            fontsize=154                # only chars above baseline
        font = ImageFont.truetype(fontname, fontsize)

        width, height = getSize(text, font)
                
        print "Image from text is: width: %d height:%d" % (width, height)
        img = Image.new('RGB', (width, height), colorBackground)
        d = ImageDraw.Draw(img)
        d.text((0, -5), text, fill=colorText, font=font)
 #           d.rectangle((0, 0, width+3, height+3), outline=colorOutline)
        img.save("image2.png")


        imgret=prepare_image(img)       # prepare image, return list(numberpixels, width,height)
        if lp_defglobal.debug: print imgret
        drawtime=imgret[2] * lp_defglobal.column_delay_time / float(1000)  # forcing float division
        if lp_defglobal.debug: print "time: %3.2f" % drawtime
        dt="%3.1f" % drawtime
        msg1=text[:8]+".."
        lp_defglobal.msg_line[0]='{:<11}'.format(msg1)  + '{:>5}'.format(dt)    # format first line of display
        lp_defglobal.msg_line[1]='{:<6}'.format(str(lp_defglobal.column_delay_time) + "ms")  \
            + dirstring()     # format second line of display


        showmsg( lp_defglobal.msg_line)                 # show image number on led display
        ret=button_pressed(GPIO)                # wait for button Press
        if lp_defglobal.debug: print "Return: %s" % lp_defglobal.but[ret]
        sleep(0.1)                          # for testing
            
            # process button press
            # is either RED, lp_defglobal.BLACK or lp_defglobal.SETUP
            
        if ret==lp_defglobal.BLACK:      # user wants next image
            continue        # continue loop with next image
            
        elif ret==lp_defglobal.SETUP:
            if do_setup(GPIO):
                if lp_defglobal.debug: 
                    print "Return from do_setup %d Type Change" % ret 
                break
                
            
        elif ret==lp_defglobal.REDSHORT:       # user wants to paint current image
            GPIO.output(lp_defglobal.led_green, True) # give the green light, ready to draw, wait for red key
            lp_defglobal.msg_line[1]='{:<6}'.format(str(lp_defglobal.column_delay_time) + "ms")  \
                + '{:^4}'.format(lp_defglobal.direction[lp_defglobal.direction_flag])  \
                + '{:>6}'.format("ready")    # format second line of display

            showmsg( lp_defglobal.msg_line)   # display ready message

#               now we are ready to paint
            ret=button_pressed(GPIO)                # ready to draw, wait for user input
            if ret==lp_defglobal.BLACK:                      # user wants next image
                GPIO.output(lp_defglobal.led_green, False)   # switch off green led
                continue                        # continue loop with next imagew
            elif ret==lp_defglobal.REDSHORT or ret==lp_defglobal.REDLONG:      # user wants to paint current image, stay with this image after paint
                if lp_defglobal.debug: print "bei lp_defglobal.REDSHORT"
                GPIO.output(lp_defglobal.led_green, False)   # green led off
                lp_defglobal.msg_line[1]='{:<6}'.format(str(lp_defglobal.column_delay_time) + "ms") \
                + '{:^4}'.format(lp_defglobal.direction[lp_defglobal.direction_flag])  \
                + '{:>6}'.format("paint")    # format second line of display
                showmsg( lp_defglobal.msg_line)   # display ready message 
# -------------------------------------------------
                draw2()                         # draw image i
# -------------------------------------------------                
                set_led(lp_defglobal.strip,lp_defglobal.BLACKCOL)                     # set all pixels to lp_defglobal.BLACK                        
       
    pass                        

    return(0)    
#---- End Main Loop Typ2-------------------------------------------------------------


