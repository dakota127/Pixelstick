#!/usr/bin/python
# coding: utf-8
#----------------------------------------------------------
#   Draw Pattern 1 Main Loop for the Light Painting System
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
from lp_patt import *
from lp_sub import *
from lp_setup import *


# -- Function do_pattern
#--------------------------------------------------------
def do_pattern (strip,numberpatt):

    if lp_defglobal.debug: 
        print "----doing pattern %d " % numberpatt
        
    sleep(lp_defglobal.waitdraw)                 # wait n sec before drawing starts
    
    if numberpatt==1:
#        lp_defglobal.iteration_pattern=2
        savedelay=lp_defglobal.column_delay_time
        lp_defglobal.column_delay_time=10
        rainbowStatic (strip, 0,143,0,lp_defglobal.brightness)
        lp_defglobal.column_delay_time=savedelay
        set_led(lp_defglobal.strip,lp_defglobal.BLACKCOL)                      # set all pixels to BLACK

    if numberpatt==2:
 #       lp_defglobal.iteration_pattern=4
        savedelay=lp_defglobal.column_delay_time
        lp_defglobal.column_delay_time=10
        rainbowStatic (strip, 0,143,1,lp_defglobal.brightness)
        lp_defglobal.column_delay_time=savedelay
        set_led(lp_defglobal.strip,lp_defglobal.BLACKCOL)                      # set all pixels to BLACK

    if numberpatt==3:
        savedelay=lp_defglobal.column_delay_time
        lp_defglobal.column_delay_time=1
        rainbowTime2 (strip,0,143,0,lp_defglobal.brightness)       # rainbow with luminace 50 / 1536 colors
        lp_defglobal.column_delay_time=savedelay
        set_led(lp_defglobal.strip,lp_defglobal.BLACKCOL)                      # set all pixels to BLACK

        pass
    if numberpatt==4:
   #     lp_defglobal.iteration_pattern=10
        savedelay=lp_defglobal.column_delay_time
        lp_defglobal.column_delay_time=1
        rainbowTime2 (strip,0,143,1,lp_defglobal.brightness)       # rainbow with luminace 50 / 1536 colors
        lp_defglobal.column_delay_time=savedelay
        set_led(lp_defglobal.strip,lp_defglobal.BLACKCOL)                      # set all pixels to BLACK

    elif numberpatt==5:
        savedelay=lp_defglobal.column_delay_time
        lp_defglobal.column_delay_time=20
        rainbowTime (strip,0,0,lp_defglobal.FULL,lp_defglobal.brightness)
        set_led(lp_defglobal.strip,lp_defglobal.BLACKCOL)                      # set all pixels to BLACK
        lp_defglobal.column_delay_time=savedelay

    
    elif numberpatt==6:
        savedelay=lp_defglobal.column_delay_time
        lp_defglobal.column_delay_time=1
        background=[90,90,90]
        set_led(lp_defglobal.strip,background)                      # set all pixels to BLACK
        rainbowTime2 (strip,10,134,0,lp_defglobal.brightness)       # rainbow with luminace 50 / 1536 colors
        set_led(lp_defglobal.strip,lp_defglobal.BLACKCOL)                      # set all pixels to BLACK
        lp_defglobal.column_delay_time=savedelay

    
        pass
    elif numberpatt==7:
        savedelay=lp_defglobal.column_delay_time
        lp_defglobal.column_delay_time=1
        background=[90,90,90]
        set_led(lp_defglobal.strip,background)                      # set all pixels to BLACK
        rainbowTime2 (strip,10,134,1,lp_defglobal.brightness)
        set_led(lp_defglobal.strip,lp_defglobal.BLACKCOL)                      # set all pixels to BLACK
        lp_defglobal.column_delay_time=savedelay
 
        pass

    
    elif numberpatt==8:                 # Snake 1---------------------
        patt=rainbowMakePatt(40)
        for j in range(lp_defglobal.iteration_pattern):
            pattRun (lp_defglobal.strip,lp_defglobal.brightness,patt,UP,UP,130,10,lp_defglobal.BLACKCOL) 
            pattRun (lp_defglobal.strip,lp_defglobal.brightness,patt,DOWN,UP,130,10,lp_defglobal.BLACKCOL)
            pattRun (lp_defglobal.strip,lp_defglobal.brightness,patt,UP,UP,130,10,lp_defglobal.BLACKCOL)
            pattRun (lp_defglobal.strip,lp_defglobal.brightness,patt,DOWN,UP,130,10,lp_defglobal.BLACKCOL) 

        sleep(0.2)
        set_led(lp_defglobal.strip,lp_defglobal.BLACKCOL)                      # set all pixels to BLACK

    elif numberpatt==9:                 # Snake 2 ----------------------
        patt=rainbowMakePatt (40)
        for j in range(lp_defglobal.iteration_pattern):
            pattRun (lp_defglobal.strip,lp_defglobal.brightness,patt,UP,UP,TOP, BOTTOM,lp_defglobal.BLACKCOL)  # Red wipe
            pattRun (lp_defglobal.strip,lp_defglobal.brightness,patt,DOWN,DOWN,TOP, BOTTOM,lp_defglobal.BLACKCOL)  # Red wipe
            pattRun (lp_defglobal.strip,lp_defglobal.brightness,patt,UP,UP,TOP, BOTTOM,lp_defglobal.BLACKCOL)  # Red wipe
            pattRun (lp_defglobal.strip,lp_defglobal.brightness,patt,DOWN,DOWN,TOP, BOTTOM,lp_defglobal.BLACKCOL)  # Red wipe

        sleep(0.2)
        set_led(lp_defglobal.strip,lp_defglobal.BLACKCOL)                      # set all pixels to BLACK

    elif numberpatt==10:                # Snake 3 ----------------------
        patt=rainbowMakePatt (40)
        background=[120,120,120]
        set_led(lp_defglobal.strip,background,50)                      # set all pixels to back
        sleep(0.4)
        for j in range(lp_defglobal.iteration_pattern):
            pattRun (lp_defglobal.strip,lp_defglobal.brightness,patt,UP,UP,130,10,background)  # Red wipe
            pattRun (lp_defglobal.strip,lp_defglobal.brightness,patt,DOWN,UP,130,10,background)  # Red wipe
            pattRun (lp_defglobal.strip,lp_defglobal.brightness,patt,UP,UP,130,10,background)  # Red wipe
            pattRun (lp_defglobal.strip,lp_defglobal.brightness,patt,DOWN,UP,130,10,background)  # Red wipe
            set_led(lp_defglobal.strip,background,50)                      # set all pixels to back
        sleep(0.4)

        set_led(lp_defglobal.strip,lp_defglobal.BLACKCOL)                      # set all pixels to BLACK

    elif numberpatt==11:
        background=[80,80,80]

        pattDraw_12 (lp_defglobal.strip, background, 1,0,lp_defglobal.brightness)
        
        pass

    elif numberpatt==12:
        background=[0,160,240]

        pattDraw_12 (lp_defglobal.strip, background, 1,1,lp_defglobal.brightness)
        
        pass

    elif numberpatt==13:
        background=[255,45,10]

        pattDraw_12 (lp_defglobal.strip, background, 2,2,lp_defglobal.brightness)
        pass
        
    elif numberpatt==14:
        background=[120,40,160]
        pattDraw_12 (lp_defglobal.strip, background, 3,0,lp_defglobal.brightness,200)

        pass
    elif numberpatt==15:
        background=[10,120,255]
        pattDraw_12 (lp_defglobal.strip, background, 3,0,lp_defglobal.brightness,100)

        pass
    elif numberpatt==16:
        pattDraw_13 (lp_defglobal.strip, 0 , lp_defglobal.brightness)
  
        pass

    elif numberpatt==17:
        background=[0,10,255]
        pattDraw_11 (lp_defglobal.strip, 0,background,0,lp_defglobal.brightness)
        pass

    elif numberpatt==18:
        background=[160,0,0]

        pattDraw_11 (lp_defglobal.strip, 0,background,1,lp_defglobal.brightness)
        pass

    elif numberpatt==19:
        mytheaterChase(lp_defglobal.strip,20,1,lp_defglobal.brightness )  # Red theater chase
        pass
        pass

    elif numberpatt==20:
        theaterChaseRainbow(lp_defglobal.strip,lp_defglobal.brightness)  # Red theater chase
        pass
        pass

    elif numberpatt==21:
        pattFade (lp_defglobal.strip,[255,0,0])
        set_led(lp_defglobal.strip,lp_defglobal.BLACKCOL)                      # set all pixels to BLACK
        pass
        
    elif numberpatt==22:
        pattFade (lp_defglobal.strip,[0,0,255],1)
        set_led(lp_defglobal.strip,lp_defglobal.BLACKCOL)                      # set all pixels to BLACK
        pass

    elif numberpatt==23:
        pattFade (lp_defglobal.strip,[0,120,145],1)
        set_led(lp_defglobal.strip,lp_defglobal.BLACKCOL)                      # set all pixels to BLACK
        pass
      
    return(0)    


#--#----------------------------------------------
# Main Loop Typ 2
#---------------------------------------------
def main_loop_type2(GPIO):

    ready_yes=0

    i=1                 # i contains pattern number
                        # pattern are in  pattern_description
    anzpatt=len(lp_defpattern.pattern_description)   # number of patterns found
    while True:         # run forever - ctrl-C interrupts
                        # check termination in variable lp_defglobal.do_term    
        if lp_defglobal.debug:
            print "Type 2 starting while loop, i %d  anzpatt %d" % (i,anzpatt)
        if  lp_defglobal.do_term: break             # break from main Loop
        if  lp_defglobal.type_switch: break             # break from main Loop

        sleep(0.5)       
        if i > anzpatt: 
            i=1	 # maxbild ist Anzahl pattern gefunden, gehe rundum, wenn am Ende
        GPIO.output(lp_defglobal.led_green, False)   # green led off

        lp_defglobal.msg_line[0]='{:<12}'.format(lp_defpattern.pattern_description[i][0:12]) \
        +    " "    \
        +   '{:>3}'.format(str(lp_defglobal.brightness))

 
        if lp_defpattern.pattern_time[i]=="man":
            showtime="man"
        else:
            showtime=str(lp_defpattern.pattern_time[i]*lp_defglobal.iteration_pattern) + "s"
        
        lp_defglobal.msg_line[1]='{:<3}'.format(showtime) \
        +   '{:>2}'.format(str(lp_defglobal.iteration_pattern)) \
        +   '{:>2}'.format(str(lp_defglobal.gamma)) \
        +   '{:>2}'.format(str(lp_defglobal.waitdraw)) + "s"\
        +  '{:>6}'.format (str(i)+ "/" + str(anzpatt))     # format second line of display
            
        if lp_defglobal.debug: print lp_defglobal.msg_line
        showmsg( lp_defglobal.msg_line)                 # show pattern number on led display
        ret=button_pressed(GPIO)                # wait for button Press
        if lp_defglobal.debug: print "Return button_pressed: %s" % lp_defglobal.but[ret]
        sleep(0.1)                          # for testing
            
            # process button press
            # is either RED, BLACK or SETUP
            
        if ret==lp_defglobal.BLACK:      # user wants next pattern
            i=i+1
            continue        # continue loop with next pattern
            
        elif ret==lp_defglobal.SETUP:
            if do_setup(GPIO):
                if lp_defglobal.debug: 
                    print "Return from do_setup %d Type Change" % ret 
                break
                
                
        elif ret==lp_defglobal.REDSHORT:       # user wants to paint current image
            GPIO.output(lp_defglobal.led_green, True) # give the green light, ready to draw, wait for red key
            
            if ready_yes:               # eingebaut, damit schneller reagiert.
    
                if lp_defpattern.pattern_time[i]=="man":
                    showtime="man"
                else:
                    showtime=str(lp_defpattern.pattern_time[i]*lp_defglobal.iteration_pattern) + "s"
                    
                lp_defglobal.msg_line[1]='{:<6}'.format(showtime)  \
                    + '{:^4}'.format(lp_defglobal.direction[lp_defglobal.direction_flag])  \
                    + '{:>6}'.format("ready")    # format second line of display

                showmsg( lp_defglobal.msg_line)   # display ready message

#               now we are ready to paint
                ret=button_pressed(GPIO)                # ready to draw, wait for user input
                if ret==lp_defglobal.BLACK:                      # user wants next image
                    GPIO.output(lp_defglobal.led_green, False)   # switch off green led
                    break                        # continue loop with next imagew
                    
                elif ret==lp_defglobal.REDSHORT:      # user wants to paint current image, stay with this image after paint
                    if lp_defglobal.debug: print "bei lp_defglobal.REDSHORT"
                    GPIO.output(lp_defglobal.led_green, False)   # green led off
                    lp_defglobal.msg_line[1]='{:<6}'.format(showtime)  \
                    + '{:^4}'.format(lp_defglobal.direction[lp_defglobal.direction_flag])  \
                    + '{:>6}'.format("paint")    # format second line of display
                    showmsg( lp_defglobal.msg_line)   # display PAINT message 

    
            lp_defglobal.lcd.backlight(lp_defglobal.lcd.OFF)    # Display off while painting

    #---------------- paint pattern -------------
            do_pattern(lp_defglobal.strip,i)        # patern (i) 
    #---------------- paint pattern -------------

            lp_defglobal.lcd.backlight(lp_defglobal.lcd.ON)

            GPIO.output(lp_defglobal.led_green, True)   # green led off
#                lp_defglobal.msg_line[1]='{:<6}'.format(str(lp_defglobal.column_delay_time) + "ms") \
#                + '{:^4}'.format(lp_defglobal.direction[lp_defglobal.direction_flag])  \
#                + '{:>6}'.format("DONE")    # format second line of display
#                showmsg( lp_defglobal.msg_line)   # display DONE message 
                    
#                sleep(1)
            set_led(lp_defglobal.strip,lp_defglobal.BLACKCOL)                      # set all pixels to BLACK

          
        #  der loop läuft, bis ein Keyboard interrupt kommt, ctrl-c ----


    pass                        

    return(0)    
#---- End Main Loop Typ2-------------------------------------------------------------
#


