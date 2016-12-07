#!/usr/bin/python
# coding: utf-8
#-------------------------------------------------------
#  Global Pattern Definition 2 für Lightpainting ------
#   prepared for a stick with 144 NeoPixel Led
#------------------------------------------------------
#

# ---  this pattern is used in pattDraw_21 ()  -------------------------
pixpatt1 = [
            [                           # first pattern
            [0,9,[90,90,90]],               
            [10,11,[0,0,0]],
            [12,65,[300]],
            [66,67,[0,0,0]],
            [68,75,[90,90,90]],        # Mitte
            [76,77,[0,0,0]],
            [78,131,[400]],
            [132,133,[0,0,0]],
            [134,142,[90,90,90]]
            ],
            
                
            [                           # second pattern
            
            [0,7,[90,90,90]],               
            [8,9,[0,0,0]],
            [10,38,[300]],
            [39,40,[0,0,0]],
            [41,65,[300]],
            
            [66,67,[0,0,0]],
            [68,75,[90,90,90]],        # Mitte
            [76,77,[0,0,0]],
            
            [78,102,[400]],
            [103,104,[0,0,0]],
            [105,133,[400]],
            [134,135,[0,0,0]],

            [136,143,[90,90,90]]
            ],

            [                           # third pattern
            
            [0,3,[180,180,180]],               
            [4,5,[0,0,0]],
            [6,18,[300]],
            [19,20,[0,0,0]],
            [21,33,[300]],
            [34,36,[0,0,0]],
            [37,49,[300]],
            [50,51,[0,0,0]],
            [52,64,[300]],
            [65,66,[0,0,0]],
            [67,71,[180,180,180]],
            [72,73,[0,0,0]],
            
            [74,86,[400]],
            [87,88,[0,0,0]],
            [89,101,[400]],
            [102,104,[0,0,0]],
            [105,117,[400]],
            [118,119,[0,0,0]],
            ]

        ]   

# ---  this color info is used in pattDraw_21 ()  -------------------------
pixcolor = [
            [                           # zero  color
            [200] ,                  # number of steps 1-1536, luminace
            [700,40,'u'],                 #color 1 start postion  
            [30,20,'c'],                 #color2  rgb  
            ],

            [                           # zero  color
            [400] ,                  # number of steps 1-1536, luminace
            [400,40,'d'],                 #color 1 start postion  
            [900,40,'u'],                 #color2  rgb  
            ],

            [                           # first  color
            [400] ,                  # number of steps 1-1536, luminace
            [700,40,'u'],                 #c                           # thiolor 1 start postion  
            [1400,40,'c'],                 #color2  rgb  
            ],

            [                           # second  color
            [400] ,                  # number of steps 1-1536, luminace
            [0,50,'u'],                 #color 1 start postion  
            [1000,50,'d'],                 #color2  rgb  
            ],
             
            [         
            [500] ,                    # number of steps 1-1536
            [800,50,'u'],                 #color 1 start postion  
            [1400,50,'d'],                 #color2  rgb  
            ],
                
            [                           # forth color
            [200] ,                    # number of steps 1-1536
            [1000,40,'u'],                 #color 1 start postion  
            [600,40,'d'],                 #color2  rgb  

            [120,132,[400]],
            [133,134,[0,0,0]],
            [135,138,[180,180,180]]                           ],
                
            [                           # fifth color
            [300] ,                    # number of steps 1-1536
            [1,40,'u'],                 #color 1 start postion  
            [1000,40,'d']                 #color2  rgb  
            ],
            
            [                   # sixth color
            [400] ,                    # number of steps 1-1536
            [1000,50,'u'],                 #color 1 start postion  
            [600,50,'u'],                 #color2  rgb  
            ],

            [                           # sseventh color
            [350] ,                    # number of steps 1-1536
            [570,20,'d'],                 #color 1 start postion  
            [1,30,'u'],                 #color2  rgb  
            ],

    ]
   
   
# pattern description for 16x2 Char display            
pattern_description={1:'Pat21', 2:'Pat22', 3:'Pat23', 4:'Pat24', \
    5:'Pat25  ',  6:'Pat26',   7:'Pat27' ,8:'Pat28', 9:'Pat29' , 10:'Pat2A' ,\
     11:'Pat2B' , 12:'Pat2C' , 13:'Pat2D' , 14:'Pat2E' , 15:'Pat2F'
    
    }

# pattern running time (measured with stop watch)
pattern_time={1:11, 2:11, 3:11, 4:11, 5:13,  6:9,   7:8 , 8:11, 9:9 , 10:9 \
    , 11:8 , 12:6 , 13:10 , 14:10 , 15:10 
    
    }

# ----------------------------------------------------