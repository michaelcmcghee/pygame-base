import random, pygame, math

class Platforms:
    BOXSIZE = 30

    def __init__(self, x, y):
        self.image = pygame.Surface((self.BOXSIZE, self.BOXSIZE))
        self.image.fill((0,255,0))
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.x = x
        self.y = y

    def centerX(self):
        return self.x + (self.width / 2)

    def centerY(self):
        return self.y + (self.height / 2)

    def render(self, screen):
        screen.blit(self.image, (self.x, self.y))