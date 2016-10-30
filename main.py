try:
    import pygame_sdl2
    pygame_sdl2.import_as_pygame()
except ImportError:
    pass
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random, pygame, sys, math
from player import *
from platforms import *
from collision import *
from platformlist import *

#Color Variables
black=(0,0,0)
white=(255,255,255)
red=(255,0,0)
green=(0,255,0)
blue=(0,0,255)

#Class Variables
player=Player(400,0)
platforms=Platforms(0,0)
platformlist=PlatformList()

#Movement Variables
UP='up'
DOWN='down'
RIGHT='right'
LEFT='left'

#Window Globals
WINDOWWIDTH=800
WINDOWHEIGHT=600
#screen = pygame.display.set_mode(size, FULLSCREEN)

class MyGame():  # Game Class

    def main(self):  # Main Method (always takes the object as 1st arg)
        pygame.init()  # Initialise the PyGame Framework

        size=width, height=WINDOWWIDTH, WINDOWHEIGHT  # Set the dimensions of your window
        collision=Collision()
        screen=pygame.display.set_mode(size)  # Create your screen / window
        # You can also pass an optional fullscreen arg

        clock=pygame.time.Clock()  # Set up the game clock
        pygame.display.set_caption('My Game')  # Set the titlebar text
        movex,movey=0,0

        while True:  # The Game Loop

            clock.tick(60)  # 60 frames per second
            for platforms in platformlist.leveldata(WINDOWWIDTH, WINDOWHEIGHT):
                collision.playerAndPlatform(player, platforms, 0.2, 0)

            # process key presses
            for event in pygame.event.get():
                if event.type==pygame.QUIT:  # Handle Quit Event
                    sys.exit()
                if event.type==pygame.KEYDOWN:
                    player.onKeyDown(event)
                if event.type==pygame.KEYUP:
                    player.onKeyUp(event)

            #
            # Your Game Code Goes Here
            #

            #background
            screen.fill(blue)  # Fill the screen with white (RGB)



            # Render the platforms
            for platforms in platformlist.leveldata(WINDOWWIDTH, WINDOWHEIGHT):
                platforms.render(screen)

            #Render player
            player.x+=movex
            player.update(WINDOWWIDTH, WINDOWHEIGHT)
            player.render(screen)

            pygame.display.update()  # Update the screen

if __name__ == '__main__':
    game=MyGame()  # Instantiate the Game class
    game.main()  # Call the main method