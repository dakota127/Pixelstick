#!/usr/bin/python
# coding: utf-8
#-------------------------------------------------------
#   Global Pattern Definition 1 für Lightpainting ------
#   prepared for a stick with 144 NeoPixel Led
#------------------------------------------------------
#

# ---  this pattern is used in pattDraw_12 ()  -------------------------
pixpatt = [
        [0,1,2,3,4,5,6,              \
            13,14,15,16,17,18,19,       \
            26,27,28,29,30,31,32,       \
            39,40,41,42,43,44,45,       \
            52,53,54,55,56,57,58,       \
            65,66,67,68,69,70,71,       \
            78,79,80,81,82,83,84,       \
            91,92,93,94,95,96,97,       \
            104,105,106,107,108,109, 110,   \
            117,118,119,120,121,122,123,    \
            130,131,132,133,134,135,136  
            ],

           [0 ,1 ,2 ,3 ,4 ,5 ,6 ,7 ,8 ,9 ,10,11,12,13,14,15,16,17,18,   \
            25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,    \
            50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,     \
            75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,     \
            100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,  \
            125,126,127,128,129,130,131,132,133,134,135,136,137,138,139,140,141,142,143 
            ],
            
            [0,1,2,3,4,             \
            14,16,17,18,           \
            25,26,27,28,            \
            36,37,38,39,         \
            47,48,49,50,          \
            58,59,60,61,         \
            69,70,71,72,       \
            80,81,82,83,       \
            91,92,93,94,        \
            102,103,104,105,    \
            113,114,115,116,    \
            124,125,126,127,    \
            135,136,137,138   
            ],
            
            [1,2,3,4,5,6,7,8,9,10,          \
            14,15,16,17,18,19,20,21,22,23,       \
            27,28,29,30,31,32,33,34,35,36,       \
            39,40,41,42,43,44,45,46,47,48,       \
            52,53,54,55,56,57,58,59,60,61,       \
            65,66,67,68,69,70,71,72,73,74,       \
            78,79,80,81,82,83,84,85,86,87,       \
            91,92,93,94,95,96,97,98,99,100,       \
            104,105,106,107,108,109,110,111,112,113,   \
            117,118,119,120,121,122,123,124,125,126,    \
            130,131,132,133,134,135,136,137,138,139
            ],
            
            [10,12,14,16,18,  \
             40,42,44,46,48, \
             60,62,64,66,68, \
             80,82,84,86,88, \
             100,102,104,106,108, \
             120,122,124,126,128
            
            ]
    ]

# ---  this pattern is used in pattDraw_11 ()  -------------------------
pixpatt2=[
            [
            [1,2,3,4,5,6,7,8,9,10],          \
            [14,15,16,17,18,19,20,21,22,23],       \
            [27,28,29,30,31,32,33,34,35,36],       \
            [39,40,41,42,43,44,45,46,47,48],       \
            [52,53,54,55,56,57,58,59,60,61],       \
            [65,66,67,68,69,70,71,72,73,74],       \
            [78,79,80,81,82,83,84,85,86,87],       \
            [91,92,93,94,95,96,97,98,99,100],       \
            [104,105,106,107,108,109,110,111,112,113],   \
            [117,118,119,120,121,122,123,124,125,126],    \
            [130,131,132,133,134,135,136,137,138,139]     \
            ],
            
            [
            [1,2,3,4,5,6,7,8,9,10],          \
            [14,15,16,17,18,19,20,21,22,23],       \
            [27,28,29,30,31,32,33,34,35,36],       \
            [39,40,41,42,43,44,45,46,47,48],       \
            [52,53,54,55,56,57,58,59,60,61],       \
            [65,66,67,68,69,70,71,72,73,74],       \
            [78,79,80,81,82,83,84,85,86,87],       \
            [91,92,93,94,95,96,97,98,99,100],       \
            [104,105,106,107,108,109,110,111,112,113],   \
            [117,118,119,120,121,122,123,124,125,126],    \
            [130,131,132,133,134,135,136,137,138,139]     \
            ]
    ]
            
# ---  this pattern is used in pattDraw_13 ()  -------------------------
pixpatt3=[
            [
            [2,4,6,8,10],                                                   # pixel
            [[23,23,45],[120,120,120],[45,255,50],[255,255,0],[0,0,157]]    # color
            ],
            [
            [2,4,6,8,10],                                                   # pixel
            [[23,23,45],[120,120,120],[45,255,50],[255,255,0],[0,0,157]]    # color
            ]
            ]

# pattern description for 16x2 Char display            
pattern_description={1:'Rainbow Full', 2:'Rainbow Full', 3:'RainbowTime', 4:'RainbowTime', \
    5:'Rainbow256  ',  6:'RainbowTime',   7:'RainbowTime' ,8:'Snake 1 ', 9:'Snake 2 ' , 10:'Snake 3 ' ,\
     11:'Stripes 1 ' , 12:'Stripes 2 ' , 13:'Stripes 3 ' , 14:'Stripes 4 ' , 15:'Stripes 5 ', \
      16:'Stripes 6 ' , 17:'Stripes RB ' , 18:'Stripes RB ' ,
    19:'Theater 1' ,20:'Theater 2' , 21:'Fade 1 Down ' , 22:'Fade 1 Up', 23:'Fade 2 Up'

    }

# pattern running time (measured with stop watch)
pattern_time={1:6, 2:'man', 3:16, 4:'man', 5:8,  6:14,   7:'man' , 8:8, 9:17 , 10:9 \
    , 11:9 , 12:6 , 13:'man' , 14:7 , 15:5 , 16:'man' , 17:8, 18:'man' , 19:'man' , 20:'man' ,21:12, 22:12, 23:12
    
    }

#----------------------------------------------------