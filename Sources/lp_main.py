#!/usr/bin/python
# coding: utf-8
#----------------------------------------------------------
#
#   Light Painting Programm for 144 led NeoPixel Strip
#
#   Based on several examples found on the Adafruit Learning System
#   Thanks to Tony DiCola , Phillip Burgess and others
#
#   This version adapted and expanded by Peter K. Boxler, Switzerland
#   January 2015
#
#   Programm can draw different types of animations
#   a) images - müssen vorbereitet sein und 144 pixel hoch sein
#   b) diverse Lichtmuster, die in den scripten lp_main2/3.py codiert sind
#   c) text - dies ist aber noch nicht realisiert, bräuchte eine Tastatur um den Text einzugeben
#
#   User-Interface :
#       Adafruit CharPlate 16x2 
#               shows current image, its width, intervall in ms, direction (left/right), waittime before paint
# 
#       3 Pushbuttons  Red, lp_defglobal.BLACK and Green
#       2 Led (red and green) - not really needed
#
#       lp_defglobal.BLACK-Button:   goto next image (round robin)
#       Red-Button  :   Select current image for painting, Red-Button again: paint after lp_defglobal.waitdraw seconds
#       Green-Button:   Enter lp_defglobal.SETUP
#
#       Images  need to be in folder ./image  and have to be 144pixels  in height (jpg)
#
#   NeoPixel Products here: 
#   ----> https://www.adafruit.com/products/1506
#-----------------------------------------------------------
#
#Import all modules
import sys, getopt, os
from time import sleep
import time, datetime
import RPi.GPIO as GPIO
from PIL import Image
import struct
from neopixel import *
from threading import Thread
#from PIL import ImageDraw
#from PIL import ImageFont
#import cStringIO
import random
from math import floor
import lp_defglobal
from lp_sub import *
from lp_setup import *
from lp_main2 import *
from lp_main3 import *

from lp_main4 import *
from lp_test import *
import signal


# LED lp_defglobal.strip configuration:
LED_COUNT      = lp_defglobal.striplen     # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)

# Configurable values
image_folder_usb = "/media/usb1/images"          # path to pictures on usb stick
image_folder = "images"          # path to pictures local
pfad=" "
fullname=" "            	             	
onoff={1:'ON', 0:'OFF'}

colorfile=((255,0,0),(0,255,0),(0,0,255),(40,170,100),(220,80,40))

# Lists
files=list()            # list of files found in picture folder
images=list()           # list of files found that are pictures
images_width=list()        # list of with of all images
column=list()           # list of list of RGB colorvalues for each pixel in current image     
gamma   =2.3            # gamma correction
gamma_a=(list)          # list of gamma corrections for every lp_defglobal.brightness 0-255
averagepix=125             # average pixel value in image

#                                                           2: from text input
exitapp=False             # signals quitiing of programm


# definitions for Adafruit 16x2 Led display
from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate
# Initialize the LCD plate.  Should auto-detect correct I2C bus.  If not,
# pass '0' for early 256 MB Model B boards or '1' for all later versions

lp_defglobal.msg_line.append (" Light Painting ")
lp_defglobal.msg_line.append (" - Initialize - ")



# ------ Function Definitions ----------------------------------
#
# ---- Function Parse commandline arguments -------------------
# get and parse commandline args
#
def arguments(argv):
    global image_folder, gamma
    try:
        opts, args=getopt.getopt(argv,"hdp:n")
    except getopt.GetoptError:
        print ("Parameter Error")
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print
            print "App %s --  Light Up those NeoPixels ---------" % lp_defglobal.appname
            print "usage: %s [-d -n -p]" % lp_defglobal.appname
            print
            sys.exit(2)
        elif opt == '-d': 	lp_defglobal.debug = 1
        elif opt == '-p': 	image_folder = arg     # not implemented
        elif opt == '-n': 	gamma = 1           # use gamma one
	
# ---------------------------------------------------------

#-- Function to handle kill Signal ---------------------
def sigterm_handler(signum = None, frame=None):
    sleep(0.4)
    # Raises SystemExit(0):
    if lp_defglobal.debug: print "Signal received " , signum 
    lp_cleanup()
    sleep(0.1)
    killit=open(lp_defglobal.killfile,"w")  # write killfile, so we know this was done
    killit.close()
    sleep(0.3)
    sys.exit(0)
#---------------------------------------------------

#---------------------------------------------
# find the with of every image that we found
# we can speed up userinterface
#--------------------------------------------
def imagewidth():
    global images, images_width, fullname
    
    for i in range (len(images)):
        imagepath=fullname + "/" + images[i]   # image path
        if lp_defglobal.debug: print "Opening image: %s" % imagepath
        try:
            imag  = Image.open(imagepath)
        except:
            print " Error opening imagefile: %s"  % imagepath
            return()
        pixels = imag.load()     # laden des Bildes 
        imgret=imag.size      
        images_width.append(imgret[0])      # Breite des Bildes in Pixel
        if lp_defglobal.debug: print "Image: %d  width: %d" % (i, imgret[0])
        imag.close()
    return()
#----------------------------------------------------------

#------- Funktion initpgm ---------------------------------
#       Initialize stuff
def initpgm():
    global files,images,pfad,fullname
    found_on_usb=0
    lp_defglobal.lcd = Adafruit_CharLCDPlate(1)
    lp_defglobal.set_led_parm_black[1]=lp_defglobal.striplen-1
    lp_defglobal.set_led_parm[1]=lp_defglobal.striplen-1

 #  Signal Handler aktivieren
    for sig in [signal.SIGTERM]:
        signal.signal (sig, sigterm_handler)
 
    if lp_defglobal.debug: 
        print "Signal Handler aktiviert"
    pass

    try:
        # try to open folder on USB stick
        if lp_defglobal.debug:
            print "USB Pfad: %s " % image_folder_usb
            print "Opening image folder %s" % image_folder_usb
        fullname=image_folder_usb
        files = os.listdir(image_folder_usb)
        found_on_usb=1
        if lp_defglobal.debug: 
            print "after opening image folder on usb"
            print "filecount USB: %d" % len(files)
        images = [img for img in files if (img.endswith('.jpg') or img.endswith('.gif') or img.endswith('.png')) and not img.startswith('.')]
        if len(images)==0:
            found_on_usb=0

        if lp_defglobal.debug: 
            print "imagecount USB: %d" % len(images)         
        
    except : 
        found_on_usb=0
        print "Error opening image folder on usb"
        
        
    if found_on_usb==0:
        try:        # now try to open local folder
            fullname=pfad + '/' + image_folder
            print "Opening image folder: %s" % image_folder

            files = os.listdir(fullname)
            found_on_usb=0

        except : 
            print  "Error opening local image folder"
            print "No images found - not on USB, not local. Nothing to do"
            lp_defglobal.lcd.backlight(lp_defglobal.lcd.OFF)

            sys.exit(2)     # sorry, no images found

    if lp_defglobal.debug:
        print "Valid Pathname is: %s" % fullname
        
    # one folder open
    images = [img for img in files if (img.endswith('.jpg') or img.endswith('.gif') or img.endswith('.png')) and not img.startswith('.')]
#
    if len(images)==0:              # no Images found, so there is nothing to do, lets call it a day.
        print "No images found in image folder: %s" % fullname
        sys.exit(2)
    images.sort()
    if lp_defglobal.debug:
        if found_on_usb:
            print "Images found on USB Stick "
        else:  print "Images found in local folder "

        print "Number of images found: %d" % len(images)
        print images


#   SETUP General Input/Output-Pins of Raspberry    
    GPIO.setmode(GPIO.BCM) 
    GPIO.setwarnings(False)
    GPIO.setup(lp_defglobal.red_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)          # red button
    GPIO.setup(lp_defglobal.black_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)         # lp_defglobal.BLACK button
    GPIO.setup(lp_defglobal.setup_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)         # lp_defglobal.SETUP button
    GPIO.setup(lp_defglobal.switch_type_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)         # type switch 

    GPIO.setup(lp_defglobal.led_green, GPIO.OUT)   # rote Led
    GPIO.output(lp_defglobal.led_green, False)

    setgamma()      # build gamma table 
       # Clear 16x2 lcd-display and show greeting, pause 1 sec
    showmsg(lp_defglobal.msg_line)

    sleep(1)              # for testing
        
    if os.path.exists(lp_defglobal.killfile):         # remove killfile
        os.remove(lp_defglobal.killfile)
        if lp_defglobal.debug: print "killfile removed" 
        
    # establish the with of every image - added to speed up going through all images
    imagewidth ()
    
    lp_defglobal.msg_line[0]='{:<3}'.format(len(images))  + "Images" '{:>7}'.format(lp_defglobal.images_found[found_on_usb])    # format first line of display

    lp_defglobal.msg_line[1]='{:>16}'.format("Red:OK")
    showmsg(lp_defglobal.msg_line)
    sleep(0.5)
    ret=button_pressed(GPIO,1)
    if lp_defglobal.debug: print "Test Return: %s" % lp_defglobal.but[ret]
    sleep(0.1)                          # for testing
    
    if (ret==lp_defglobal.REDSHORT or ret==lp_defglobal.BLACK):
        return(0)
        

# -------- convert to hex -------------	
def float_to_hex(f):
    return hex(struct.unpack('<I', struct.pack('<f', f))[0])
#------------

# -------- Drwa Function for testing
# 
def draw(strup,colore) :
    print"Draw Image.........."  
    colorWipe(strup, Color(colore[0],colore[1],colore[2]))  # Red wipe
    sleep(1)
    return(0)
#-------------------------    


#-----------------------------------
def dirstring():        # second line of display
    if lp_defglobal.direction_flag==1:
            ab='{:^5}'.format(str(lp_defglobal.waitdraw) + lp_defglobal.direction[lp_defglobal.direction_flag])
    else:
        ab='{:^5}'.format( lp_defglobal.direction[lp_defglobal.direction_flag] + str(lp_defglobal.waitdraw) )
    return (ab)
#--------------------------------

        
        
#----------------------------------------------
# Main Loop Typ 1
# Main Loop für Images
# Bilder sind bereits eingelesen und befinden sich ind er Liste images[]
#---------------------------------------------
def main_loop_type1():
    global images,fullpath,images_width
    
    ready_yes=0
    i=0                 # i contains image number
                        # images are in list images
    anzim=len(images)   # number of images found
 
#  Loop durch alle vorhandenen Images
    
    while True:         # run forever - ctrl-C interrupts
                        # check termination in variable lp_defglobal.do_term    
        if lp_defglobal.debug:
            print "Type 1 starting while loop, do_term %d, type %d" % (lp_defglobal.do_term,lp_defglobal.type_switch)
        if  lp_defglobal.do_term: break             # break from main Loop
        if  lp_defglobal.type_switch: break         # break from main Loop

        if lp_defglobal.debug: print "doing type 1 (pictures)"

        if i>=anzim: 
            i=0	   # maxbild ist Anzahl Bilder gefunden, gehe rundum, wenn am Ende

        GPIO.output(lp_defglobal.led_green, False)   # green led off

        drawtime=images_width[i] * (lp_defglobal.column_delay_time+11) / float(1000)  # forcing float division
        if lp_defglobal.debug: print "time: %3.2f" % drawtime
        dt="%3.1f" % drawtime
        msg1="Image " + str(i+1)+ "/" + str(anzim) +  " "
        lp_defglobal.msg_line[0]='{:<11}'.format(msg1)  + '{:>5}'.format(dt)    # format first line of display
        lp_defglobal.msg_line[1]='{:<6}'.format(str(lp_defglobal.column_delay_time) + "ms")  \
            + dirstring()  \
            + '{:>5}'.format(str(averagepix))    # format second line of display
        showmsg( lp_defglobal.msg_line)           # show image number und weitere Info on 16x2 display
        
        ret=button_pressed(GPIO,1)                # wait for button Press
        
        if lp_defglobal.debug: print "Return button_pressed: %s" % lp_defglobal.but[ret]
        sleep(0.1)                      # for testing    
           
    # process button press
    # is either RED, BLACK or SETUP
            
        if ret==lp_defglobal.BLACK:     # user wants next image
            i=i+1
            continue                    # continue loop with next image
            
        elif ret==lp_defglobal.SETUP:
            if do_setup(GPIO):      # 1 heisst: user will output type ändern (nicht mehr images)
                if lp_defglobal.debug: 
                    print "Return from do_setup %d Type Change" % ret 
                break
            else:
                pass        # normaler setup ist fertig durchlaufen
                            # weiter in Verarbeitung images            

        elif ret==lp_defglobal.REDSHORT:            # user wants to paint current image
            GPIO.output(lp_defglobal.led_green, True) # give the green light, ready to draw, wait for red key

# ----- verlangtes Image behandeln -----
            imagepath=fullname + "/" + images[i]   # image path
            if lp_defglobal.debug: print "Opening image: %s" % imagepath
            try:
                imag  = Image.open(imagepath).convert("RGB")
            except:
                print " Error opening imagefile: %s"  % imagepath
                lp_defglobal.msg_line[0]="Error Open"   # format first line of display
                lp_defglobal.msg_line[1]=imagepath
                showmsg(lp_defglobal.msg_line)
                sleep(5)
                sys.exit(2)    
            imgret=prepare_image(imag)       # prepare image, return list(numberpixels, width,height)
            if lp_defglobal.debug: print imgret

#  -------- Ready ausgeben, bereit zum Zeichnen -------------
             
            lp_defglobal.msg_line[1]='{:<6}'.format(str(lp_defglobal.column_delay_time) + "ms")  \
                + '{:^4}'.format(lp_defglobal.direction[lp_defglobal.direction_flag])  \
                + '{:>6}'.format("ready")           # format second line of display

            showmsg( lp_defglobal.msg_line)         # display ready message

#        now we are ready to paint, warte auf button press
            ret=button_pressed(GPIO,1)              # ready to draw, wait for user input
            if ret==lp_defglobal.BLACK:             # user wants next image
                i=i+1
                GPIO.output(lp_defglobal.led_green, False)   # switch off green led
                continue                            # continue loop with next imagew
                    
            elif ret==lp_defglobal.REDSHORT:        # user wants to paint current image, stay with this image after paint
                if lp_defglobal.debug: print "bei lp_defglobal.REDSHORT"
                GPIO.output(lp_defglobal.led_green, False)   # green led off
                lp_defglobal.msg_line[1]='{:<6}'.format(str(lp_defglobal.column_delay_time) + "ms") \
                + '{:^4}'.format(lp_defglobal.direction[lp_defglobal.direction_flag])  \
                + '{:>6}'.format("paint")    # format second line of display
                showmsg( lp_defglobal.msg_line)     # display PAINT message 
                lp_defglobal.lcd.backlight(lp_defglobal.lcd.OFF)
    
            draw2()                                 # draw image i
            lp_defglobal.lcd.backlight(lp_defglobal.lcd.ON)

            GPIO.output(lp_defglobal.led_green, True)   # green led off
            
#  -------- Done ausgeben, Zeichnen fertig -------------
            
            lp_defglobal.msg_line[1]='{:<6}'.format(str(lp_defglobal.column_delay_time) + "ms") \
            + '{:^4}'.format(lp_defglobal.direction[lp_defglobal.direction_flag])  \
            + '{:>6}'.format("DONE")                # format second line of display
            showmsg( lp_defglobal.msg_line)         # display DONE message 
                    
            sleep(0.2)
            set_led(lp_defglobal.strip,lp_defglobal.BLACKCOL)   # set all pixels to BLACK


#   End While True    über alle Bilder                
#  der loop läuft, bis ein Keyboard interrupt kommt, ctrl-c ----

    pass                        
    return(0)    
#---- End Main Loop Typ1 (Images) -------------------------------------------------------
#

# ----- Function cleaup ----------------------------------------
def lp_cleanup():
    if lp_defglobal.debug: print "\Doing cleanup in %s" % lp_defglobal.appname
    
    lp_defglobal.lcd.backlight(lp_defglobal.lcd.OFF)
    GPIO.cleanup(lp_defglobal.led_green)
    GPIO.cleanup(lp_defglobal.red_button)
    GPIO.cleanup(lp_defglobal.black_button)
    GPIO.cleanup(lp_defglobal.setup_button)
    GPIO.cleanup(lp_defglobal.switch_type_pin)
    return(0)


#********************************************************
# *******************************************************
# Program starts here, let's roll
# *******************************************************
# *******************************************************

if __name__ == '__main__':

    lp_defglobal.appname=os.path.basename(__file__)     # name des scripts holen
#
    arguments(sys.argv[1:])                             # get commandline arguments

    pfad=os.path.dirname(os.path.realpath(__file__))    # pfad wo dieses script läuft
    
    lp_defglobal.killfile =  pfad + "/" + lp_defglobal.killfile    # set correct path
    if lp_defglobal.debug: print "Current dir: %s" % pfad
    if lp_defglobal.debug: print "Killfile: %s" % lp_defglobal.killfile
                       
    initpgm()                   # init stuff
    
    blink_led(GPIO,lp_defglobal.led_green,3)      # blink led green 
    sleep(1)
#    
    # Create NeoPixel object with appropriate configuration.
    lp_defglobal.strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
    # Intialize the library (must be called once before other functions).
 
    lp_defglobal.strip.begin()
    
    set_led(lp_defglobal.strip,lp_defglobal.BLACKCOL)   # set all pixels to dark

# posit: do it as long not Ctlr-C 
    try:
            
        do_test(lp_defglobal.strip, GPIO)               # do test pattern 

        while True:
            if  lp_defglobal.do_term: break             # break from main Loop
            if lp_defglobal.debug: print "Loop in Main, type %d"  % lp_defglobal.painting_type       
#
#                                               # what kind of Light Painting ?
            if lp_defglobal.painting_type==1:   # zeichne Images
                main_loop_type1()               # work is done in main_loop_type1()
                                                # return from mainloop if Ctrl-C on Keyboard
            elif lp_defglobal.painting_type==2: # zeichne muster 1
                main_loop_type2(GPIO)           # work is done in main_loop_type2()
                                                # return from mainloop if Ctrl-C on Keyboard
            elif lp_defglobal.painting_type==3: # Zeichne Muster 2   
                main_loop_type3(GPIO)           # work is done in main_loop_type3()
                                                # return from mainloop if Ctrl-C on Keyboard

            elif lp_defglobal.painting_type==4: # Zeichne Text   
                main_loop_type4(GPIO)           # work is done in main_loop_type4()
                                                # return from mainloop if Ctrl-C on Keyboard
            if lp_defglobal.type_switch:
                lp_defglobal.painting_type=get_type(GPIO)
#
    except KeyboardInterrupt:
        pass
    # cleanup
        if lp_defglobal.debug: print "\nKeyboard Interrupt in %s" % lp_defglobal.appname
        lp_defglobal.do_term=1
        lp_cleanup()
    finally:
    # write file - so we know this part was done properly
        if lp_defglobal.debug: print "\nFinally reached in %s" % lp_defglobal.appname
        lp_defglobal.msg_line[0]="Terminating...  "
        lp_defglobal.msg_line[1]="                "
        showmsg( lp_defglobal.msg_line)         # display DONE message 
        lp_defglobal.lcd.backlight(lp_defglobal.lcd.ON)
        sleep(2)
        lp_defglobal.lcd.backlight(lp_defglobal.lcd.OFF)
        set_led(lp_defglobal.strip,lp_defglobal.BLACKCOL)                   # set all pixels to dark
        lp_defglobal.strip.__del__()                    # cleanup NeoPixel Library

#  Clean-Up and terminate
    exitapp = True                  # signal exit to the other threads, they will terminate themselfs

    print "Program %s terminated...." % lp_defglobal.appname
    sys.exit(0)
    
#**************************************************************
#  That is the end
#***************************************************************
#
