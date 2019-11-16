"""
  A colour object is
  RED    = 8bits = R
  GREEN  = 8bits = G
  BLUE   = 8bits = B;
  ALPHA  = 8bits = A
  HEX Colour  =  #ARGB
"""

class Colour(object):
    def __init__(self, red, green, blue, alpha= 255):
        self.__Red    = red;
        self.__Green  = green;
        self.__Blue   = blue;
        self.__Alpha  = alpha




    
