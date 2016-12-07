#!/usr/bin/python
# coding: utf-8
#-------------------------------------------------------
#  Global Variables für Lightpainting --------------------
#   Used by all modules lP_xxx.py
#------------------------------------------------------
#
debug=0                 # 0= no debug output, 1= debug output
debugg=0                # Big debug, more details
appname=" "             # application name (script)
do_term=0               # term signal in mainloop
lcd=0
msg_line=list()         # lines to be displayed 16x2 Char 

type_switch=0

# Button and Led's Definiton
red_button = 23         # red button
black_button =24        # black button
setup_button =25        # to enter stup
led_green=9             # signals image selected and ready to paint
switch_type_pin = 22    # setup switch

BLACK=1                 # return from button_pressed
REDSHORT=2              # return from button_pressed
REDLONG=3               # return from button_pressed
SETUP=4                 # return from button_pressed
but={1:'Black', 2:'Red-short', 3:'Red-long', 4:'Setup'}
direction={0:'<--', 1:'-->'}
direction_flag=1                # default direction left to right
waitdraw_default=2              # number of seconds to wait before drawing
waitdraw=waitdraw_default       # number of seconds to wait before drawing

setup_pixel_time=11             # from experience (Python is slooow)
column_delay_time_min=9         # minmal value
column_delay_time_default=9
column_delay_time = column_delay_time_default + setup_pixel_time
                                # in milliseconds       
brightness_default=255          # max 255
brightness=brightness_default

waitbutton_1 = 0.8      # wait time in sec for button
iteration_pattern=1     # iteration counter for drawPatt functions
painting_type=1         # what sort of LightPainting to do  (1: images from Image folder)
striplen=144            # number of led in the strip
column=list()           # list of list of RGB colorvalues for each pixel in current image     

strip=0
BLACKCOL=[0,0,0]            # Black Color
WHITECOL=[255,255,255]      # white color
BOTTOM=-1                   # constants
TOP=-1
UP=1
DOWN=0
FULL=-2
UPDOWN={1:'UP', 0:'DOWN'}

set_led_parm=[0,0,BLACKCOL,100]
set_led_parm_black=[0,0,BLACKCOL,100]

gamma  = 2                  # gamma correction
gamma_a = bytearray(256)
g_maxin =   255.0           # max values
g_maxout  = 255.0

anz_type=3                 # number of mainloops
killfile="lp_killed.txt"    # killfile name
type_description={1:'Images', 2:'Pattern 1',  3:'Pattern 2', 4:'Text', 5:'Undef'}
images_found={0:'Local', 1:'USB'}

savecollist=list()          # list of pixels to light up

# -------------------------------------------------------------------