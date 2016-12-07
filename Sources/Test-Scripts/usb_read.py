#!/usr/bin/python
# coding: utf-8
#----------------------------------------------------------
#
#   Test Programm: files lesen von USB-Stick oder von lokalem Dir, wenn USB Stick nicht da ist
#   usb stick ist mounted on /media/usb1
#   Ausgabe Resultat auf stdout und 16x2 Char Display
#-----------------------------------------------------------
#  USB Stick:  vorbereiten des Mount Point:
#
#   sudo mkdir /media/usb1
#   sudo chown pi:pi /media/usb1
#
#   Mounten des Sticks:
#   sudo mount -t vfat -o uid=pi,gid=pi /dev/sda1 /media/usb1
#
#   Unmount Stick:
#   sudo umount /media/usb1
#
#   Mount Stick at boot time -> add this line to  /etc/fstab
#
#   /dev/sda1       /media/usb1     vfat    rw,defaults     0       0
#

#-----------------------------------------------------------
#
#Import all modules
import sys, getopt, os
from time import sleep
import time, datetime
import RPi.GPIO as GPIO
import signal
from PIL import Image


# definitions for Adafruit 16x2 Led display
from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate
# Initialize the LCD plate.  Should auto-detect correct I2C bus.  If not,
# pass '0' for early 256 MB Model B boards or '1' for all later versions

debug=0                 # 0= no debug output, 1= debug output
debugg=0                # Big debug, more details
appname=" "             # application name (script)
do_term=0               # term signal in mainloop
msg_line=list()         # lines to be displayed 16x2 Char 
lcd=0
# Button and Led's Definiton
red_button = 23         # red button

# Configurable values
image_folder_usb = "/media/usb1/images"          # path to pictures on usb stick
image_folder = "images"          # path to pictures local
pfad=" "
fullname=" "            	             	
onoff={1:'ON', 0:'OFF'}

# Lists
files=list()            # list of files found in picture folder
images=list()           # list of files found that are pictures
images_width=list()        # list of with of all images
column=list()           # list of list of RGB colorvalues for each pixel in current image     
#                                                           2: from text input
exitapp=False             # signals quitiing of programm

msg_line.append (" USB Read Test ")
msg_line.append (" - Initialize - ")

killfile="usb_killed.txt"    # killfile name
type_description={1:'Images', 2:'Pattern 1',  3:'Pattern 2', 4:'Text', 5:'Undef'}
images_found={0:'Local', 1:'USB'}


# ------ Function Definitions ----------------------------------
#
# ---- Function Parse commandline arguments -------------------
# get and parse commandline args
#
def arguments(argv):
    global image_folder, debug
    try:
        opts, args=getopt.getopt(argv,"hdp:")
    except getopt.GetoptError:
        print ("Parameter Error")
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print
            print "App %s --  Light Up those NeoPixels ---------" % appname
            print "usage: %s [-d -n -p]" % appname
            print
            sys.exit(2)
        elif opt == '-d': 	debug = 1
        elif opt == '-p': 	image_folder = arg     # not implemented
	
# ---------------------------------------------------------

#-- Function to handle kill Signal ---------------------
def sigterm_handler(signum = None, frame=None):
    sleep(0.4)
    # Raises SystemExit(0):
    if debug: print "Signal received " , signum 
    lp_cleanup()
    sleep(0.1)
    killit=open(killfile,"w")  # write killfile, so we know this was done
    killit.close()
    sleep(0.3)
    sys.exit(0)
#---------------------------------------------------

#------- Funktion showmsg ---------------------------------
#        Display 2 Lines of text on CharPlate 16x2
def showmsg(output):
    global lcd
    lcd.clear()
    lcd.message(output[0] + "\n"  + output[1])

# -------------------------------------------------------

#---------------------------------------------
# find the with of every image that we found
# we can speed up userinterface
#--------------------------------------------
def imagewidth():
    global images, images_width, fullname
    for i in range (len(images)):
        imagepath=fullname + "/" + images[i]   # image path
        if debug: print "Opening image: %s" % imagepath
        try:
            imag  = Image.open(imagepath)
        except:
            print " Error opening imagefile: %s"  % imagepath
            return()

        imgret=imag.size       # prepare image, return list(numberpixels, width,height)
#        imgret=prepare_image(imag)       # prepare image, return list(numberpixels, width,height)
        images_width.append(imgret[0])
        if debug: print "Image: %d  width: %d" % (i, imgret[0])
        imag.close()
    return()
#----------------------------------------------------------

#------- Funktion initpgm ---------------------------------
#       Initialize stuff
def initpgm():
    global files,images,pfad,fullname, lcd
    found_on_usb=0
    
    lcd = Adafruit_CharLCDPlate(1)

 #  Signal Handler aktivieren
    for sig in [signal.SIGTERM]:
        signal.signal (sig, sigterm_handler)
 
    if debug: 
        print "Signal Handler aktiviert"
    pass

# try to read file from usb stick -----------------------------
# try/except to figure out if folder/stick is present
#---------------------------------------------------------------
    try:
        # try to open folder on USB stick
        if debug:
            print "USB Pfad: %s " % image_folder_usb
            print "Opening image folder %s" % image_folder_usb

        fullname=image_folder_usb
        files = os.listdir(image_folder_usb)
        found_on_usb=1
        if debug: 
            print "sucsessfully opened image folder on usb"
            print "found files on USB: %d" % len(files)
        images = [img for img in files if (img.endswith('.jpg') or img.endswith('.gif') or img.endswith('.png')) and not img.startswith('.')]
        if len(images)==0:
            found_on_usb=0

        if debug: 
            print "found images on USB: %d" % len(images)         
        
    except : 
        found_on_usb=0
        print "Error opening image folder on usb"
        
# try to open local folder (only if files not found on usb stick) ------
# try/except
#-----------------------------------------------------------------------
    if found_on_usb==0:             # nothing found on usb
        try:                        # now try to open local folder
            fullname=pfad + '/' + image_folder
            print "Opening local image folder: %s" % image_folder
            files = os.listdir(fullname)
        except : 
            print  "Error opening local image folder"
            print "No images found - not on USB, not local. Nothing to do"
            lcd.backlight(lp_defglobal.lcd.OFF)
            sys.exit(2)                 # sorry, no images found on stick and none local, so we quit

    if debug:
        print "Successfully opened this image-path: %s" % fullname
        print "found files on local folder: %d" % len(files)

#---now, hopefully we found eithr folder on stick or local folder ------------
#        
    # one folder open
    images = [img for img in files if (img.endswith('.jpg') or img.endswith('.gif') or img.endswith('.png')) and not img.startswith('.')]
#
    if len(images)==0:              # no Images found, so there is nothing to do, lets call it a day.
        print "No images found in image folder: %s" % fullname
        sys.exit(2)
    if debug: 
        print "found images on local folder: %d" % len(images)         

    images.sort()                   # sort images

    if debug:
        if found_on_usb:  print "Images found on USB Stick "
        else:  print "Images found in local folder "

        print "Number of images found: %d" % len(images)
        print images


#   SETUP General Input/Output-Pins of Raspberry    
    GPIO.setmode(GPIO.BCM) 
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM) 
    GPIO.setwarnings(False)
    GPIO.setup(red_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)          # red button

       # Clear 16x2 lcd-display and show greeting, pause 1 sec
    showmsg(msg_line)

    sleep(1)              # for testing
        
    if os.path.exists(killfile):         # remove killfile
        os.remove(killfile)
        if debug: print "killfile removed" 
        
    # establish the with of every image - added to speed up going through all images
    imagewidth ()
    
    msg_line[0]='{:<3}'.format(len(images))  + "Images" '{:>7}'.format(images_found[found_on_usb])    # format first line of display

    msg_line[1]='{:>16}'.format("Red:Exit")
    showmsg(msg_line)
    sleep(0.5)
    sleep(0.1)                          # for testing
    

# ----- Function cleaup ----------------------------------------
def lp_cleanup():
    if debug: print "\Doing cleanup in %s" % appname
    lcd.backlight(lcd.OFF)

    GPIO.cleanup(red_button)
    lcd.backlight(lcd.OFF)
    return(0)

# *************************************************
# Program starts here, let's roll
# *************************************************

if __name__ == '__main__':

    appname=os.path.basename(__file__)
#
    arguments(sys.argv[1:])  # get commandline arguments

    pfad=os.path.dirname(os.path.realpath(__file__))    # pfad wo dieses script läuft
  
    killfile =  pfad + "/" + killfile    # set correct path
    if debug: 
        print "Current dir: %s" % pfad
        print "ScriptName: ",appname
        print "Killfile: %s" % killfile
                       
    initpgm()                   # init stuff
    sleep(1)
#    

# posit: do it as long not Ctlr-C 
    try:
        while True:
#
            print " doing nothing...Wait for Ctrl-C"
            sleep(0.2)
            if GPIO.input(red_button):
                pass
            else: 
                lp_cleanup()
                break
    
    except KeyboardInterrupt:
        pass
    # cleanup
        if debug: print "\nKeyboard Interrupt in %s" % appname
        do_term=1
        lp_cleanup()
    finally:
    # write file - so we know this part was done properly
        if debug: print "\nFinally reached in %s" % appname

#  Clean-Up and terminate
    exitapp = True                  # signal exit to the other threads, they will terminate themselfs

    
    print "Program %s terminated...." % appname
    sys.exit(0)
    
#**************************************************************
#  That is the end
#***************************************************************
#
