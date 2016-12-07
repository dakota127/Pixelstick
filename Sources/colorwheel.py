#!/usr/bin/python
# coding: utf-8
#-------------------------------------------------
# Colorwheel Function 1536 colors max
# Author: Peter K. Boxler
#
#-------------------------------------------------

#-------------------------------------------------
# Generate 1536 rgb Colors around the colorwheel
# Starting with RED
#-------------------------------------------------
#   parameters: 
#   position on colorwheel, luminace 10-90 %
#   loop needs to be outside the function (see example)
#   pos indicates postion on the colorwheel
#   luminance can be 10,20,30,40,50,60,70,80,90 %
#   luminance 50% gives max. number of colors : 1536
#   the loopcounter has to set like this:
#   while True
#
#   returns  (retcode , [ r ,g, b]
#      
#   retcode:
#   0 if colorvalue 
#   -98 wrong luminance
#   -99 max. color reached
# 
#   Peter K. Boxler, February 2015
# ---------------------------------------------------------------  
def color_wheel_r (debug, posin , lum=50):

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
    if debug:
        print "colwheel --- posin: %d pos: %d  from: %d  to: %d z: %d count: %d ----------" % (posin, pos, start, max, z, count[lum/10])
    
    if pos < z: 
        if debug: print "colwheel --- pos %d doing part 1" % pos
                # first sixth of wheel
        return(retu,[max, pos+start, start])        # red=max, green increases=0, blue=0
    
    elif pos < (2 * z):                             # second sixth of wheel
        pos -= z
        if debug: print "colwheel --- pos %d doing part 2" % pos
        return(retu,[max-pos, max, start])          # red decrases, green=max, blue=0
    elif pos < (3 * z):                             # third sixth of wheel
        if debug: print "colwheel --- pos %d doing doing 3" % pos
        pos -= 2 * z
        return(retu,[start, max, pos+start])        # red=0, green max, blue=increases
    elif pos < (4 * z):                             # fourth sixth of wheel
        if debug: print "colwheel --- pos %d doing part 4" % pos
        pos -= 3 * z
        return(retu,[start, max-pos, max])          # red=0, green=decreases, blue=max
    elif pos < (5 * z):                             # fifth sixth of wheel
        if debug: print "colwheel --- pos %d doing part 5" % pos
        pos -= 4 * z
        return(retu,[pos+start, start, max])        # red increases, green=0, blue=max
    else:                                           # last sixth of wheel
        if debug: print "colwheel --- pos %d doing part 6" % pos
        pos -= (5 * z)
        return(retu,[max, start, max-pos])          # red=max, green=0, blue decreases

#--------------------------------------------------------------


# old old old
#---------------------------------------------------------------
# Generate 1536 rgb Colors around the colorwheel
# Starting with GREEN
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
# ---------------------------------------------------------------  
def color_wheel_g (pos , lum=50):
    global debug

    colval_min=[255,0,0,0,0,0,51,102,153,204,255]      # rbg values max and min
    colval_max=[0,51,102,153,204,255,255,255,255,255,255]      # rbg values max and min

    count=[0,312,618,924,1230,1536,1230,924,618,312,0]  # loop counter limit based on lum
    
    if lum<10 or lum>90:        # must be between 10 and 90
        return (-99)
    if pos >= count[lum/10]:    # loop breaks, we reached max number of colors for this luminace
        return (-99)
 
    start=colval_min[lum/10]    # set min values for r,g and b  based on luminace
    max=colval_max[lum/10]      # set max values for r,g and b  
    z=max-start+1
    if debug:
        print "----- lumi: %d min: %d  max: %d z: %d count: %d -------------------" % (lum, start, max, z, count[lum/10])
    
    if pos < z:                 # first sixth of wheel
        return(pos+start, max, start)
    
    elif pos < (2 * z):         # second sixth of wheel
        pos -= z
        if debug: print "pos %d doing 2" % pos
        return(max, max-pos, start) 
        
    elif pos < (3 * z):          # third sixth of wheel
        if debug: print "pos %d doing 3" % pos
        pos -= 2 * z
        return(max, start, pos+start)
        
    elif pos < (4 * z):          # fourth sixth of wheel
        if debug: print "pos %d doing 4" % pos
        pos -= 3 * z
        return(max-pos, start, max)

    elif pos < (5 * z):           # fifth sixth of wheel
        if debug: print "pos %d doing 5" % pos
        pos -= 4 * z
        return(start, pos+start, max)

    else:                          # last sixth of wheel
        if debug: print "pos %d doing 6" % pos
        pos -= (5 * z)
        return(start, max, max - pos)
      
#---------------------------------------------------------------


#--------------------------------------------------------
# The END        
#---------------------------------------------------------
