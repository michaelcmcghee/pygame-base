import random, pygame, math
from player import *
from platforms import *

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