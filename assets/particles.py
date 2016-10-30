import random, pygame, sys, math
from pygame.locals import *

FPS = 60
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
BGCOLOR = (60, 60, 100)
BLUE = (0, 0, 255)

# Key Constants
UP = 'up'
DOWN = 'down'
RIGHT = 'right'
LEFT = 'left'


class Player:
    # Constants used for physics applied to a player. Can be abstracted out and used in other
    # moving classes (like enimies ai)
    FRICTION = 0.6
    SPEED_LIMIT = 5
    GRAVITY = 0.8
    ACCELERATION = 1.5
    BOUNCE = -0.3
    JUMP_FORCE = -12
    BOTTOM_OFFSET = 0  # Pixels from the bottom of the window to the top of the ground

    def __init__(self, x, y):

        # Set player class properties
        self.image = pygame.image.load('./assets/images/spellun-sprite.png')
        self.rect = self.image.get_rect()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.x = x
        self.y = y
        self._accelerationX = 0
        self._accelerationY = 0
        self._vx = 0
        self._vy = 0
        self._isOnGround = True
        self._friction = self.FRICTION
        self._bounceX = 0
        self._bounceY = 0
        self._spriteFacing = 'right'

    def centerX(self):
        return self.x + (self.width / 2)

    def centerY(self):
        return self.y + (self.height / 2)

    def isOnGround(self, val):
        self._isOnGround = val

    def onKeyDown(self, event):
        if event.key == K_LEFT or event.key == K_RIGHT:
            # Player is moving so disable friction
            self._friction = 1

        if event.key == K_LEFT:
            self._accelerationX = -self.ACCELERATION
            if self._spriteFacing == 'right':
                self.image = pygame.transform.flip(self.image, True, False)
                self._spriteFacing = 'left'
        if event.key == K_RIGHT:
            self._accelerationX = self.ACCELERATION
            if self._spriteFacing == 'left':
                self.image = pygame.transform.flip(self.image, True, False)
                self._spriteFacing = 'right'
        if event.key == K_UP or event.key == K_SPACE:
            if self._isOnGround:
                self._accelerationY = self.JUMP_FORCE
                self._isOnGround = False

    def onKeyUp(self, event):
        if event.key == K_LEFT or event.key == K_RIGHT:
            self._accelerationX = 0
            self._friction = self.FRICTION
        if event.key == K_UP or event.key == K_SPACE:
            self._accelerationY = 0

    def update(self):
        # Apply Acceleration to velocity value
        self._vx += self._accelerationX
        if self._vx > self.SPEED_LIMIT:
            self._vx = self.SPEED_LIMIT
        if self._vx < -self.SPEED_LIMIT:
            self._vx = -self.SPEED_LIMIT

        self._vy += self._accelerationY
        if self._vy > self.SPEED_LIMIT * 3:
            self._vy = self.SPEED_LIMIT * 3

        # Apply Friction
        if self._isOnGround:
            self._vx *= self._friction
        # Make sure velocity eventually reaches zero
        if math.fabs(self._vx) < 0.1:
            self._vx = 0
        if math.fabs(self._vy) < 0.1:
            self._vy = 0

        self._vy += self.GRAVITY

        # Apply bounce from collisions
        self.x += self._bounceX
        self.y += self._bounceY

        # Move Player
        self.x += self._vx
        self.y += self._vy

        # Reset platform bounce values
        self._bounceX = 0
        self._bounceY = 0

        # Prevent player from moving up if it's not on the ground
        if not self._isOnGround:
            self._accelerationY = 0

        if self._vy >= 0:
            self._isOnGround = False

        # Set window boundries
        if self.x + self.width > WINDOWWIDTH:
            self._vx = 0
            self.x = WINDOWWIDTH - self.width
        elif self.x < 0:
            self._vx = 0
            self.x = 0
        if self.y < 0:
            self._vy = 0
            self.y = 0 + self.height
        elif self.y + self.height > WINDOWHEIGHT - self.BOTTOM_OFFSET:
            self._vy *= self.BOUNCE
            self.y = WINDOWHEIGHT - self.height - self.BOTTOM_OFFSET
            self._isOnGround = True


class Platform:
    BOXSIZE = 30

    def __init__(self, x, y):
        self.image = pygame.Surface((self.BOXSIZE, self.BOXSIZE))
        self.image.fill(BLUE)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.x = x
        self.y = y

    def centerX(self):
        return self.x + (self.width / 2)

    def centerY(self):
        return self.y + (self.height / 2)


class Collision:
    def playerAndPlatform(self, player, platform, bounce, friction):
        # Player center points and half width/height
        playerCenterX = player.centerX()
        playerCenterY = player.centerY()
        playerHalfWidth = player.width / 2
        playerHalfHeight = player.height / 2

        # Platform center points and half width/height
        platformCenterX = platform.centerX()
        platformCenterY = platform.centerY()
        platformHalfWidth = platform.width / 2
        platformHalfHeight = platform.height / 2

        # Find the distance between the player and platform on the x axis
        dx = platformCenterX - playerCenterX

        # Find the amount of overlap on the x axis. Since the distance delta (dx) is between
        # the center point of the platform to the center point of the player, we add the
        # half widths of each object, the subtract the absolute value of the distance. If
        # ox > 0, we know that the two objects overlap. If it's less than zero, they are not.
        ox = platformHalfWidth + playerHalfWidth - math.fabs(dx)

        # Check for collisions on the x axis
        if ox > 0:
            # If objects overlap on x axis, a collision might be occuring. Set vars to check on y axis
            dy = playerCenterY - platformCenterY
            oy = platformHalfHeight + playerHalfHeight - math.fabs(dy)

            if oy > 0:
                # Collision occuring.  Let's find which side
                if ox < oy:
                    if dx < 0:
                        # Collision on right
                        oy = 0
                        dx = 1
                        dy = 0
                    else:
                        # Collision on left
                        oy = 0
                        ox *= -1
                        dx = -1
                        dy = 0
                else:
                    if dy < 0:
                        # Collision on Top
                        ox = 0
                        oy *= -1
                        dx = 0
                        dy = -1
                        # Set isOnGround
                        player.isOnGround(True)
                    else:
                        # collision on bottom
                        ox = 0
                        dx = 0
                        dy = 1

                # Find the direction of the collision
                directionOfCollision = player._vx * dx + player._vy * dy

                # Calculate the new direction for the bounce
                newDirectionX = directionOfCollision * dx
                newDirectionY = directionOfCollision * dy

                # Find the "tangent velocity" the speed in the direction that the object is moving.
                # Used to calculate additional platform friction
                tangent_vx = player._vx - newDirectionX
                tangent_vy = player._vy - newDirectionY

                # Apply collision forces if the object is moving into a colision
                if directionOfCollision < 0:
                    # Calculate the friction
                    frictionX = tangent_vx * friction
                    frictionY = tangent_vy * friction

                    # Calculate the amount of bounce
                    bounceX = newDirectionX * bounce
                    bounceY = newDirectionY * bounce

                else:
                    # Prevent forces from being applied if the object is moving out of a collision
                    bounceX = 0
                    bounceY = 0
                    frictionX = 0
                    frictionY = 0

                # Apply platform friction
                player._vx += ox - frictionX
                player._vy += oy - frictionY
                player._vy = 0

                # Move the player out of the collision
                player.x += ox
                player.y += oy

                # Bounce the player off the platform
                player._bounceX = bounceX
                player._bounceY = bounceY


def main():
    global FPSCLOCK, DISPLAYSURF
    pygame.init()
    platformList = [
        Platform(320, WINDOWHEIGHT - 80),
        Platform(350, WINDOWHEIGHT - 80),
        Platform(200, 164),
        Platform(560, 324),
        Platform(320, 225),
        Platform(20, 175),
        Platform(440, WINDOWHEIGHT - 90),
        Platform(470, WINDOWHEIGHT - 90),
        Platform(120, WINDOWHEIGHT - 80),
        Platform(220, 340),
        Platform(430, 250),
    ]

    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Platformer Test')
    player = Player(15, WINDOWHEIGHT - 32)
    collision = Collision()

    while True:

        DISPLAYSURF.fill(BGCOLOR)  # Drawing the window

        # Run a collision check for the player with all of the platforms
        for platform in platformList:
            collision.playerAndPlatform(player, platform, 0.2, 0)

        for event in pygame.event.get():  # event handling loop
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                player.onKeyDown(event)
            if event.type == KEYUP:
                player.onKeyUp(event)

        # Update the player's position
        player.update(WINDOWWIDTH, WINDOWHEIGHT)

        # Render the platforms
        for platform in platformList:
            DISPLAYSURF.blit(platform.image, (platform.x, platform.y))

        # Render the player
        DISPLAYSURF.blit(player.image, (player.x, player.y))

        pygame.display.update()
        FPSCLOCK.tick(FPS)


if __name__ == '__main__':
    main()