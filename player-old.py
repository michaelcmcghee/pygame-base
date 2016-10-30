import pygame  # Import the PyGame Module

class Player:

    def __init__(self, x, y):
        self.x=x
        self.y=y
        self.width=32
        self.height=32
        self.velocity=0
        self.falling=True
        self.onGround=False

    def detectCollisions(self, x1, y1, w1, h1, x2, y2, w2, h2):
        if (x2 + w2 >= x1 >= x2 and y2 + h2 >= y1 >= y2):
            return True
        elif (x2 + w2 >= x1 + w1 >= x2 and y2 + h2 >= y1 >= y2):
            return True
        elif (x2 + w2 >= x1 >= x2 and y2 + h2 >= y1 + h1 >= y2):
            return True
        elif (x2 + w2 >= x1 + w1 >= x2 and y2 + h2 >= y1 + h1 >= y2):
            return True
        else:
            return False


    def update(self, gravity, blockList):
        if(self.velocity<0):
            self.falling=True
            collision=False

        blockX,blockY=0,0
        for block in blockList:
            collision = self.detectCollisions(self.x, self.y, self.width, self.height, block.x, block.y, block.width, block.height)

            if(collision==True):
                blockX=block.x
                blockY=block.y
                self.onGround = True
                self.falling = False
                self.velocity = 0
                #self.y = blockY - self.height
                print('Collision: %s' %collision)
                break

        if(collision==False):
            self.onGround = False
            self.falling = True
            self.velocity+=gravity

        self.y-= self.velocity

    def render(self, screen):
        DISPLAYSURF.blit(player.image, (player.x, player.y))
        pygame.draw.rect(screen,(255,0,0),(self.x,self.y,self.width,self.height))
