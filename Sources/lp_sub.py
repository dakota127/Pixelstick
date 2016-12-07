#!/usr/bin/python
# coding: utf-8
#----------------------------------------------------------
#   Collection of Functions for the Light Painting System
# 
#   Peter K. Boxler, February 2015
#----------------------------------------------------------- 

import lp_defglobal
import time, datetime
from time import sleep
from neopixel import *

#------- Funktion showmsg ---------------------------------
#        Display 2 Lines of text on CharPlate 16x2
def showmsg(output):
    lp_defglobal.lcd.clear()
    lp_defglobal.lcd.message(output[0] + "\n"  + output[1])

# -------------------------------------------------------

# ----- set all pixel to a color    
def set_led(strip,color,bright=100):
    if lp_defglobal.debugg: print"Clear LED................"   
    for i in range (lp_defglobal.striplen):
        strip.setPixelColor(i, (Color(color[0],color[1],color[2])))
    strip.setBrightness(bright)
    
    strip.show()
    return(0)
#--------------------------

# ----- set all pixel to a color    
def set_led2(strip, parmlist):
    if lp_defglobal.debugg: print"set_led2..... von %d  bis %d" %  (parmlist[0],parmlist[1])
    
    
    for i in range (parmlist[0],parmlist[1]+1):
        strip.setPixelColor(i, (Color(parmlist[2][0],parmlist[2][1],parmlist[2][2])))
    strip.setBrightness(parmlist[3])
    
    strip.show()
    return(0)
#--------------------------

# ----------------------------------
def setgamma ():
# Calculate gamma correction table based on variable gamma
# Gamma correction ist used for all pixels in the image
    if lp_defglobal.debug: print"set gamma-table with gamma %d" %  lp_defglobal.gamma

    for i in range(256):
        lp_defglobal.gamma_a[i] = int(pow(i / lp_defglobal.g_maxin, lp_defglobal.gamma) * 255.0 + 0.5)

    if lp_defglobal.debugg:
        for z in range(256):
            print "gamma_a %d %d" % (z,lp_defglobal.gamma_a[z])
#-----------------------------------


#------Wait for button Press (Black or Red or Setup) --------------------------------    
def button_pressed(GPIO,type=0):
    if lp_defglobal.debug: print "Waiting for Buttonpress..type %d" % type
    
    while True:
        inpblack=1
        inpred=1
        inpblack=GPIO.input(lp_defglobal.black_button)       # high if NOT pressed !
        inpred=GPIO.input(lp_defglobal.red_button)
        inpsetup=GPIO.input(lp_defglobal.setup_button)
        inptypeswitch=GPIO.input(lp_defglobal.switch_type_pin)

#        print "Button %d %d" % (inpblack, inpred)
 
        if not inpsetup:  
            if inptypeswitch:               # check what he wants: setup or select type                     
                lp_defglobal.type_switch=1
                return(lp_defglobal.SETUP)         # black button went to low
            else:
                return(lp_defglobal.SETUP)
                
        if not inpblack:  
            sleep(0.3)
            return(lp_defglobal.BLACK)         # black button went to low
            
        if not inpred:                          # red button went to low
            if type:   
                sleep(0.2)                         # do not wait for long red
                if lp_defglobal.debug: print "return redshort"
                return(lp_defglobal.REDSHORT)
            sleep(1)                            # check if red is pressed long or short
            inpred=GPIO.input(lp_defglobal.red_button)
            sleep(0.1)
            if inpred: return(lp_defglobal.REDSHORT)
            else: return(lp_defglobal.REDLONG)

    pass
#-------------------------------------------

# ***** Function blink-led **************************
def blink_led(GPIO,pin,anzahl):  # blink led 3 mal bei start und bei shutdown
        for i in range(anzahl):
            GPIO.output(pin, True)
            sleep(0.1)
            GPIO.output(pin, False)
            sleep(0.1)
#-------------------------

#--- Function get_type from user --------------------	
def get_type(GPIO):		
   
    z=0
    while True:
        z=z+1
        if z>lp_defglobal.anz_type:
            z=1
        if lp_defglobal.debug: print "User selects type"
        lp_defglobal.msg_line[0]="- Select Type - "          # format first line of display
        lp_defglobal.msg_line[1]='{:<2}'.format(str(z)) \
            + '{:>14}'.format(lp_defglobal.type_description[z])    # format second line of displ
        showmsg( lp_defglobal.msg_line)                 # show image number on led display
        lp_defglobal.type_switch=0
        ret=button_pressed(GPIO)
        if lp_defglobal.debug: print "Select Type Return: %s" % lp_defglobal.but[ret]
#        sleep(0.1)                          # for testing
        if ret==lp_defglobal.BLACK: 
            sleep(lp_defglobal.waitbutton_1)
            continue           # increment
        elif ret==lp_defglobal.REDSHORT: 
            lp_defglobal.msg_line[1]='{:<2}'.format(str(z)) + "  " \
            + '{:>10}'.format("selected")    # format second line of displ
            showmsg( lp_defglobal.msg_line)                 # show image number on led display
            sleep(0.2)
            return(z)        # decrement
        elif ret==lp_defglobal.SETUP: 
            z=z-2
            if z<0: z=0
    sleep(lp_defglobal.waitbutton_1)
    pass
#-----------------------------------------


#------- Funktion prepare_image ---------------------------------
#   Load image form folder and prepare array for each lp_defglobal.column
def prepare_image(img):
    
    if lp_defglobal.debug: print "Preparing Image"
     
    pixels    = img.load()
    width     = img.size[0]
    height    = img.size[1]
    if lp_defglobal.debug: print "Size: %dx%d pixels" % img.size
	# To do: add resize here if image is not desired height
#   not yet implemented
           
	# Create list of bytearrays, one for each lp_defglobal.column of image.
	# R, G, B byte per pixel
    lp_defglobal.column = [0 for x in range(width)]
    for x in range(width):
        lp_defglobal.column[x] = bytearray(height * 3 )
    if lp_defglobal.debug: print "Columns allocated: %d each has: %d" % (x, height*3)
#
	# Apply Gamma Correction to all pixels of the image
    if lp_defglobal.debug: print "Extracting colors..."
    for x in range(width):              # über Bildbreite
        for y in range(height):         # über Bildhöhe
            y1=height-y-1             # store down up (due to pysical layout of lp_defglobal.strip: input at bottom)
 #           y1=lp_defglobal.striplen-y-1             # store down up (due to pysical layout of lp_defglobal.strip: input at bottom)

            value = pixels[x, y]        # hole Werte
            y3 = y1 * 3
				#RGB
            if lp_defglobal.debugg: print "lp_defglobal.column x: %d y3: %d red: %d green: %d blue: %d" % (x, y3,value[0],value[1],value[2])	
            lp_defglobal.column[x][y3]     = lp_defglobal.gamma_a[value[0]]   # red
            lp_defglobal.column[x][y3 + 1] = lp_defglobal.gamma_a[value[1]]   # green
            lp_defglobal.column[x][y3 + 2] = lp_defglobal.gamma_a[value[2]]   # blue
    pass
    return((img,pixels,width,height))

#
# From Adadfruit: 
# Color should be a 24-bit value where the upper 8 bits are the red
# value, middle 8 bits are the green value, and lower 8 bits are the blue value.
# Color is a helper function that lets you define a color with
# just these red, green, blue component values.
#


# --------------------------------------------------------- 
#     Draws image column wise left to right / right to left
# ---------------------------------------------------------        
def draw2() :
    global gamma_a, images
    if lp_defglobal.debug: print "Zeichnen, warte %d Sek" %  lp_defglobal.waitdraw
    sleep(lp_defglobal.waitdraw)                 # wait n sec before drawing starts

    anzcol=len(lp_defglobal.column)
    lencol=len(lp_defglobal.column[0])/3
    startpix=40
    if lp_defglobal.debug: 
        print "Anzahl Streifen: %d" % anzcol
        print "Streifenlänge: %d" % lencol
#    
    shift=0                 # used for testing
    if lp_defglobal.debug:
        stime1 = datetime.datetime.now()            # time to test total draw time time

    for z in range (anzcol):
    
        if lp_defglobal.direction_flag:                      # 1=left to right / 0 right to left 
            z1=z                                # count forward, start with zero         
        else: z1=anzcol-z-1                     # count backwards, start with max
        
        # SETUP one column
        if lp_defglobal.debug:
            stime = datetime.datetime.now()     # time to test lp_defglobal.SETUP time
        for y in range (lencol):
                             # bild hat soviele Kollonnen
            y3=y*3
#           ---------- write this pixel into the pixel array using library
            lp_defglobal.strip.setPixelColor(y, Color(lp_defglobal.column[z1][y3+shift] , lp_defglobal.column[z1][y3+shift+1]  , lp_defglobal.column[z1][y3+shift+2]   ))
#           --------------------------------------------------------------
            if lp_defglobal.debugg:
                if (z>106 and z<140) and (y==60): 
                    colo=(lp_defglobal.column[z][y3+shift], lp_defglobal.column[z][y3 + shift+ 1], lp_defglobal.column[z][y3 + shift +2])
                    print colo
                    print "Col: %d Color %d %d %d " % (z, colo[0],colo[1],colo[2])

#       -------- show all pixel, light them up, baby......
#        lp_defglobal.strip.setBrightness(10)
        lp_defglobal.strip.show()
#      --------------------------------------------------
        if lp_defglobal.debug:
            etime = datetime.datetime.now()     # end time lp_defglobal.SETUP pixel
            if z==1:
                dauer=etime-stime
                print "Elapsed Time setup Pixels one column %s ms" % str(dauer.microseconds/1000)
#
#       and have them on for a certain time        
        time.sleep((lp_defglobal.column_delay_time)/1000.0)        # in Miliseconds
    
    
    # End of loop over columns
    pass
 #   column[:]=[]            # ??????
    
    if lp_defglobal.debug:                                           # total Draw Time for testing
        etime1 = datetime.datetime.now()
        dauer=etime1-stime1
        print "Elapsed Time ms Draw Total " , (dauer.microseconds/1000)
        print "columns lit for %d ms" % (lp_defglobal.column_delay_time)


#    sleep(0.1)              # for testing only
    return(0)
# -------------------------

#--------------------------------------------
# Function wheel, 256 colors
#---------------------------------------------
def wheel (start , how=0, gamma=0):
#    Generate rainbow colors within 0-255, mit gamma function

    if start < 85:
#        print "%d:  %d  %d  %d" % (start, start * 3, 255 - start * 3, 0)

        if how: 
            if gamma:
                return (lp_defglobal.gamma_a[start * 3],lp_defglobal.gamma_a [ 255 - start * 3], 0)
            
            else:           # forward
                return (start * 3, 255 - start * 3, 0)
        else:
            if gamma:
                return Color(lp_defglobal.gamma_a[start * 3],lp_defglobal.gamma_a [ 255 - start * 3], 0)
            else:
                return Color(start * 3, 255 - start * 3, 0)

    elif start < 170:
 #       print "%d:  %d  %d  %d" % (start, 255- (start-85) * 3, 0, (start-85)*3 )

        start -= 85

        if how: 
            if gamma:
                return (lp_defglobal.gamma_a[255 - start * 3], 0, lp_defglobal.gamma_a[start * 3])
            else:            #forward
                return (255 - start * 3, 0, start * 3)
        else:
        
            if gamma:
                return Color(lp_defglobal.gamma_a[255 - start * 3], 0, lp_defglobal.gamma_a[start * 3])
        
            else:
                return Color(255 - start * 3, 0, start * 3)

    else:
  #      print "%d:  %d  %d  %d" % (start, 0, (start-170) * 3, 255 - (start-170) * 3)

        start -= 170

        if how:
            if gamma:
                return (0, lp_defglobal.gamma_a[start * 3], lp_defglobal.gamma_a[255 - start * 3])
            else:
                return (0, start * 3, 255 - start * 3)
        else:
            if gamma:
                return Color (0, lp_defglobal.gamma_a[start * 3], lp_defglobal.gamma_a[255 - start * 3])
            else:
                return Color (0, start * 3, 255 - start * 3)
#--------------------------------------------  

#---------------------------------------------
def wheel2 (start , how=0):
#    Generate rainbow colors within 0-255 ohne gamma
    if start < 85:
        if how:             # forward
            return (start * 2, 255 - start * 2, 0)
        else:
            return Color(start * 2, 255 - start * 2, 0)

    elif start < 170:
        start -= 85
        if how:             #forward
            return (255 - start * 3, 0, start * 3)
        else:
            return Color(255 - start * 3, 0, start * 3)

    else:
        start -= 170
        if how:
            return (0, start * 3, 255 - start * 3)
        else:
            return Color (0, start * 3, 255 - start * 3)
  #--------------------------------------------  


#---------------------------------------------------------------
# Generate 1536 rgb Colors around the colorwheel
# Starting with RED
#---------------------------------------------------------------
#   parameters: position on colorwheel, luminace 10-90 %
#   loop needs to be outside the function (see example)
#   pos indicates postion on the colorwheel
#   luminance can be 10,20,30,40,50,60,70,80,90 %
#   luminance 50% gives max. number of colors : 1536
#   the loopcounter has to set like this:
#   while True
#
#   returns -99 if max. number of colors reached or wrong luminance
# 
#   Peter K. Boxler, February 2015
# ---------------------------------------------------------------  
def color_wheel_r (debug,posin , lum=50):

    colval_min=[255,0,0,0,0, 0 , 51,102,153,204,255]      # rbg values max and min
    colval_max=[0  , 51,102,153,204,255,255,255,255,255,255]      # rbg values max and min

    count=[0,312,618,924,1230,1536,1230,924,618,312,0]  # loop counter limit based on lum
    retu=0
    
    if lum<10 or lum>90:        # must be between 10 and 90
        return (-98,[0,0,0])
    pos=posin                   # keep colorwheel pos input
    if pos >= count[lum/10]:    # signal that we reached max number of colors for this luminace
        pos=pos-count[lum/10]
        retu=-99                # signal overflow to caller (but continue after correction)
    if pos < 0:
        pos=count[lum/10]-abs(pos)         # ?????????????????
        if debug: print "colwheel --- pos below zero, new value: %d" % pos
        retu=-99
    start=colval_min[lum/10]    # set min values for r,g and b  based on luminace
    max=colval_max[lum/10]      # set max values for r,g and b  
    z=max-start+1
    if lp_defglobal.debug:
        print "colwheel --- posin: %d pos: %d  von: %d  bis: %d z: %d count: %d -------------------" % (posin, pos, start, max, z, count[lum/10])
    
    if pos < z: 
        if lp_defglobal.debugg: print "colwheel --- pos %d doing part 1" % pos
                # first sixth of wheel
        return(retu,[max, pos+start, start])        # red=max, green increases=0, blue=0
    
    elif pos < (2 * z):                             # second sixth of wheel
        pos -= z
        if lp_defglobal.debugg: print "colwheel --- pos %d doing part 2" % pos
        return(retu,[max-pos, max, start])          # red decrases, green=max, blue=0
    elif pos < (3 * z):                             # third sixth of wheel
        if lp_defglobal.debugg: print "colwheel --- pos %d doing doing 3" % pos
        pos -= 2 * z
        return(retu,[start, max, pos+start])        # red=0, green max, blue=increases
    elif pos < (4 * z):                             # fourth sixth of wheel
        if lp_defglobal.debugg: print "colwheel --- pos %d doing part 4" % pos
        pos -= 3 * z
        return(retu,[start, max-pos, max])          # red=0, green=decreases, blue=max
    elif pos < (5 * z):                             # fifth sixth of wheel
        if lp_defglobal.debugg: print "colwheel --- pos %d doing part 5" % pos
        pos -= 4 * z
        return(retu,[pos+start, start, max])        # red increases, green=0, blue=max
    else:                                           # last sixth of wheel
        if lp_defglobal.debugg: print "colwheel --- pos %d doing part 6" % pos
        pos -= (5 * z)
        return(retu,[max, start, max-pos])          # red=max, green=0, blue decreases
    
#---------------------------------------------------------------


