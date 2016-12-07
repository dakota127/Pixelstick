#!/usr/bin/python
# coding: utf-8
#----------------------------------------------------------
#   Setup Functions for the Light Painting System
#   
#   Peter K. Boxler, February 2015
#---------------------------------------------------------

import lp_defglobal
from time import sleep
from lp_sub import *

#---------------------------------------------------
#   Function do_setup --------------------
#   black buttonpress cycles thru all 4 setups
#
def do_setup(GPIO):
    
    if lp_defglobal.debug:
        print "---do_setup"
    msg_setup=list()
    if  GPIO.input(lp_defglobal.switch_type_pin): # check switch type
        if lp_defglobal.debug:
            print "going to change type"
            lp_defglobal.type_switch=1
        return(1)
    else:
        if lp_defglobal.debug:
            lp_defglobal.type_switch=0
            print "Changing setup"

#  ----- SETUP 1 ----------Brightness ------------------------------    
    msg_setup.append('{:<8}'.format("Setup 1")  + '{:>8}'.format("Bright")  )  # format second line of display
    msg_setup.append(" ")
   
    msg_setup[1]='{:<5}'.format(str(lp_defglobal.brightness) + "%")  + '{:>11}'.format("adjust")    # format second line of display
    showmsg(msg_setup)
    sleep(1)
    ret=button_pressed(GPIO,1)
    if lp_defglobal.debug: print "Setup1 Return: %s" % lp_defglobal.but[ret]
    sleep(0.1)                          # for testing
            
    # process button press
    # is either RED, BLACK or SETUP
    while True:
        if ret==lp_defglobal.SETUP: break         
        elif ret==lp_defglobal.REDSHORT:            # increment
            lp_defglobal.brightness=lp_defglobal.brightness+40
            if (lp_defglobal.brightness > 250): lp_defglobal.brightness=250
        elif ret==lp_defglobal.BLACK:         # decrement
            lp_defglobal.brightness=lp_defglobal.brightness-40
            if (lp_defglobal.brightness <60): lp_defglobal.brightness=30

        msg_setup[1]='{:<5}'.format(str(lp_defglobal.brightness) + "%")  + '{:>11}'.format("adjust")    # format second line of display
        showmsg(msg_setup)
        sleep(lp_defglobal.waitbutton_1)
        ret=button_pressed(GPIO,1)
    pass
    msg_setup[:]=[]

#  End of SETUP 1 -----------------------------      

#  ----- SETUP 2 ------------Intervall Column Draw-----------------    
    msg_setup.append('{:<8}'.format("Setup 2")  + '{:>8}'.format("Interv")  )  # format second line of display
    msg_setup.append(" ")
   
    msg_setup[1]='{:<5}'.format(str(lp_defglobal.column_delay_time) + "ms")  + '{:>11}'.format("adjust")    # format second line of display
    showmsg(msg_setup)
    sleep(1)
    ret=button_pressed(GPIO,1)
    if lp_defglobal.debug: print "Setup 2 Return: %s" % lp_defglobal.but[ret]
    sleep(0.1)                          # for testing
            
    # process button press
    # is either RED, lp_defglobal.BLACK or lp_defglobal.SETUP
    while True:        
        if ret==lp_defglobal.SETUP: break
        elif ret==lp_defglobal.REDSHORT:            # increment
            lp_defglobal.column_delay_time=lp_defglobal.column_delay_time+5
            if (lp_defglobal.column_delay_time > 50): lp_defglobal.column_delay_time=50
        elif ret==lp_defglobal.BLACK:         # decrement
            lp_defglobal.column_delay_time=lp_defglobal.column_delay_time-5
            if (lp_defglobal.column_delay_time <12): lp_defglobal.column_delay_time=11
        if lp_defglobal.debug: print "delay new: %d" % lp_defglobal.column_delay_time
        msg_setup[1]='{:<5}'.format(str(lp_defglobal.column_delay_time) + "ms")  + '{:>11}'.format("adjust")    # format second line of display
        showmsg(msg_setup)
        sleep(lp_defglobal.waitbutton_1)

        ret=button_pressed(GPIO,1)
    pass
    msg_setup[:]=[]
    
#  End of SETUP 2 -----------------------------     

#  ----- SETUP 3 --------Wait time before Draw------------    
    msg_setup.append('{:<8}'.format("Setup 3")  + '{:>8}'.format("Wait")  )  # format second line of display
    msg_setup.append(" ")
   
    msg_setup[1]='{:<5}'.format(str(lp_defglobal.waitdraw) + "sec")  + '{:>11}'.format("adjust")    # format second line of display
    showmsg(msg_setup)
    sleep(1)
    ret=button_pressed(GPIO,1)
    if lp_defglobal.debug: print "Setup 3 Return: %s" % lp_defglobal.but[ret]
    sleep(0.1)                          # for testing
            
    # process button press
    # is either RED, lp_defglobal.BLACK or lp_defglobal.SETUP
    while True:        
        if ret==lp_defglobal.SETUP: break
        elif ret==lp_defglobal.REDSHORT:            # increment
            lp_defglobal.waitdraw=lp_defglobal.waitdraw+2
            if (lp_defglobal.waitdraw > 10): lp_defglobal.waitdraw=10
        elif ret==lp_defglobal.BLACK:         # decrement
            lp_defglobal.waitdraw=lp_defglobal.waitdraw-2
            if (lp_defglobal.waitdraw <0): lp_defglobal.waitdraw=0
       
        msg_setup[1]='{:<5}'.format(str(lp_defglobal.waitdraw) + "sec")  + '{:>11}'.format("adjust")    # format second line of display
        showmsg(msg_setup)
        sleep(lp_defglobal.waitbutton_1)
        ret=button_pressed(GPIO,1)
    pass
    msg_setup[:]=[]
    
#  End of SETUP 3 -----------------------------     

#  ----- SETUP 4 -----------iterationn ---------------    
    msg_setup.append('{:<8}'.format("Setup 4")  + '{:>8}'.format("Iter")  )  # format second line of display
    msg_setup.append(" ")
   
    msg_setup[1]='{:<4}'.format(str(lp_defglobal.iteration_pattern) + " times")  + '{:>9}'.format("adjust")    # format second line of display
    showmsg(msg_setup)
    sleep(1)
    ret=button_pressed(GPIO,1)
    if lp_defglobal.debug: print "Setup 4 Return: %s" % lp_defglobal.but[ret]
    sleep(0.1)                          # for testing
            
    # process button press
    # is either RED, BLACK or SETUP
    while True:        
        if ret==lp_defglobal.SETUP: break
        elif ret==lp_defglobal.REDSHORT:          #  increment
            lp_defglobal.iteration_pattern=lp_defglobal.iteration_pattern+1
        elif ret==lp_defglobal.BLACK:         # right to left
            lp_defglobal.iteration_pattern=lp_defglobal.iteration_pattern-1
        msg_setup[1]='{:<4}'.format(str(lp_defglobal.iteration_pattern) + " times")  + '{:>9}'.format("adjust")    # format second line of display

        showmsg(msg_setup)
        sleep(lp_defglobal.waitbutton_1)
        ret=button_pressed(GPIO,1)
    pass
    msg_setup[:]=[]

#  End of SETUP 4 -----------------------------      
 
#  -----  5 -----------Draw Direction ---------------    
    msg_setup.append('{:<8}'.format("Setup 5")  + '{:>8}'.format("Direct")  )  # format second line of display
    msg_setup.append(" ")
   
    msg_setup[1]='{:<12}'.format("Direction")  + '{:>4}'.format(lp_defglobal.direction[lp_defglobal.direction_flag])    # format second line of display
    showmsg(msg_setup)
    sleep(1)
    ret=button_pressed(GPIO,1)
    if lp_defglobal.debug: print "Setup 5 Return: %s" % lp_defglobal.but[ret]
    sleep(0.1)                          # for testing
            
    # process button press
    # is either RED, lp_defglobal.BLACK or lp_defglobal.SETUP
    while True:        
        if ret==lp_defglobal.SETUP: break
        elif ret==lp_defglobal.REDSHORT:            # left to right
            lp_defglobal.direction_flag=1
        elif ret==lp_defglobal.BLACK:         # right to left
            lp_defglobal.direction_flag=0
        if (lp_defglobal.gamma <1): lp_defglobal.gamma=1
 
        msg_setup[1]='{:<12}'.format("Gamma")  + '{:>4}'.format(lp_defglobal.direction[lp_defglobal.direction_flag])    # format second line of display
        showmsg(msg_setup)
        sleep(lp_defglobal.waitbutton_1)
        ret=button_pressed(GPIO,1)
    pass
    msg_setup[:]=[]

#  End of  5 -----------------------------      

#  -----  6 -----------Gamma  ---------------    
    msg_setup.append('{:<8}'.format("Setup 6")  + '{:>8}'.format("Gamma")  )  # format second line of display
    msg_setup.append(" ")
   
    msg_setup[1]='{:<5}'.format(str(lp_defglobal.gamma))  + '{:>11}'.format("adjust")    # format second line of display
    showmsg(msg_setup)
    sleep(1)
    ret=button_pressed(GPIO,1)
    if lp_defglobal.debug: print "Setup 6 Return: %s" % lp_defglobal.but[ret]
    sleep(0.1)                          # for testing
            
    # process button press
    # is either RED, lp_defglobal.BLACK or lp_defglobal.SETUP
    while True:        
        if ret==lp_defglobal.SETUP:
            setgamma()
            break
        elif ret==lp_defglobal.REDSHORT:            # left to right
            lp_defglobal.gamma=lp_defglobal.gamma+0.4
            if (lp_defglobal.gamma > 3): lp_defglobal.gamma=3

        elif ret==lp_defglobal.BLACK:         # right to left
            lp_defglobal.gamma=lp_defglobal.gamma-0.4
            if (lp_defglobal.gamma <1): lp_defglobal.gamma=1
        msg_setup[1]='{:<5}'.format(str(lp_defglobal.gamma) )  + '{:>11}'.format("adjust")    # format second line of display
        showmsg(msg_setup)
        sleep(lp_defglobal.waitbutton_1)
        ret=button_pressed(GPIO,1)
    pass
    msg_setup[:]=[]

#  End of  6 -----------------------------      
  
  

#   SETUP Done, goback to wherever it was called from
    
    return(0)

#--------------------------------------
