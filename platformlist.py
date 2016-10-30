import random, pygame, math
from random import randint
from platforms import *

class PlatformList:

    def __init__(self):
        return

    def leveldata(self, WINDOWWIDTH, WINDOWHEIGHT):
        bwidth = (randint(0, WINDOWWIDTH)-90)
        bheight = (randint(0, WINDOWHEIGHT)-90)

        platformList = [
            #Platforms(320, WINDOWHEIGHT - 80),
            Platforms(350, WINDOWHEIGHT - 80),
            Platforms(200, 164),
            Platforms(560, 324),
            Platforms(320, 225),
            #Platforms(bwidth, bheight),
            Platforms(430, 250)
        ]
        #print bwidth
        #print bheight
        return platformList