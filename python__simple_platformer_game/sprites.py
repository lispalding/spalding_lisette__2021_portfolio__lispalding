# MADE BY: Lisette Spalding
# ART WORK CREDIT: "Kenney.nl" @ "www.kenney.nl"
# FILE NAME: sprites.py
# PROJECT NAME: python__simple_platformer_game
# DATE CREATED: 04/01/2021
# DATE LAST MODIFIED: 04/25/2021
# PYTHON VER. USED: 3.8

##################### IMPORTS #####################
import pygame as pg
from random import choice
from os import path

# Custom Imports
from settings import *
#################### FINISHED #####################

################### GLOBAL VAR ####################
vec = pg.math.Vector2
#################### FINISHED #####################

class Spritesheet():
    """ To use: Spritesheet()
    This class will parse and load spritesheets. """
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def getImage(self, x, y, width, height):
        """ To use: getImage(x, y, width, height)
        This method obtains an image, grabbing it from the larger spritesheet. """
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))

        # Scaling image
        image = pg.transform.scale(image, (width // 2, height // 2))

        return image

class Player(pg.sprite.Sprite):
    def __init__(self, game):
        super(Player, self).__init__()
        self.game = game

        ##### VARIABLES FOR ANIMATION #####
        self.walking = False
        self.jumping = False

        self.currentFrame = 0 # This variable tells us what the current frame is for the animation

        self.lastUpdate = 0 # This variable keeps track of how long it has been since the last animation update
        ########## VARIABLES FIN ##########

        # Getting the player image
        self.loadImages()

        self.image = self.standingFrames[0]

        # self.image = pg.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        # self.image.fill(PURPLE)

        self.rect = self.image.get_rect()

        ## Placement
        self.rect.center = (40, HEIGHT - 100)
        ## Placement FIN

        ## Movement Variables:
        self.position = vec(40, HEIGHT - 100)
        self.velocity = vec(0, 0)
        self.acceleration = vec(0, 0)
        ## Movement Variables FIN

        self.keypressed = False

    def loadImages(self):
        """ To use: self.loadImages()
        This method loads the frames for the images required for animating the player. """

        self.standingFrames = [self.game.spritesheet.getImage(614, 1063, 120, 191),
                               self.game.spritesheet.getImage(690, 406, 120, 201)]
        for frame in self.standingFrames:
            frame.set_colorkey(BLACK)

        self.rightWalkingFrames = [self.game.spritesheet.getImage(678, 860, 120, 201),
                                   self.game.spritesheet.getImage(692, 1458, 120, 207)]
        for frame in self.rightWalkingFrames:
            frame.set_colorkey(BLACK)

        self.leftWalkingFrames = []
        for frame in self.rightWalkingFrames:
            frame.set_colorkey(BLACK)
            self.leftWalkingFrames.append(pg.transform.flip(frame, True, False)) # In this case, True is the horizontal flip, False is the vertical flip

        self.jumpingFrame = self.game.spritesheet.getImage(382, 763, 150, 181)
        self.jumpingFrame.set_colorkey(BLACK)

    def togglePressed(self):
        """ To use: self.togglePressed()
        This method changed the 'keypressed' value to False."""
        self.keypressed = False

    def jumpCut(self):
        if self.jumping:
            if self.velocity.y < -3:
                self.velocity.y = -3

    def jump(self):
        """ To use: self.jump()
        This method makes the player jump. Activated by the space bar; as defined in main.py... """

        ## Setting up, so we can create the ability to jump:
        self.rect.x += 2
        # Creating the ability to check to see if the sprite has collided with a platform:
        hits = pg.sprite.spritecollide(self, self.game.platformsGroup, False)
        self.rect.x -= 2
        ## Setup FIN

        if hits and not self.jumping: # Jump if only standing on a platform
            r.choice(self.game.jumpingSounds).play()
            self.jumping = True
            self.velocity.y += -PLAYER_JUMP

    def update(self):
        """ To use: self.update()
        This is the function that will update the movement of the player character. """
        self.animate()

        ##### !! Basic Movement !! #####
        self.acceleration = vec(0, PLAYER_GRAVITY)

        # Cheking the Keystate
        keystate = pg.key.get_pressed()

        ########## !!!! .. FLOW MOVEMENT .. !!!! ##########
        if keystate[pg.K_LEFT] or keystate[pg.K_a]:
            self.acceleration.x += -PLAYER_ACCELERATION

        if keystate[pg.K_RIGHT] or keystate[pg.K_d]:
            self.acceleration.x = PLAYER_ACCELERATION

        ## Player Movement Calculations
        self.acceleration.x += self.velocity.x * PLAYER_FRICTION # Applying friction

        # Equations of motion:
        self.velocity += self.acceleration

        if abs(self.velocity.x) < 0.1:
            self.velocity.x = 0

        self.position += self.velocity + 0.5 * self.acceleration
        ########## !!!! .. FLOW FINISHED .. !!!! ##########

        # Setting the screen-wrapping for left and right (Sides of the screen)
        if self.position.x > WIDTH + self.rect.width / 2:
            self.position.x = 0 - self.rect.width / 2
        if self.position.x < 0 - self.rect.width / 2:
            self.position.x = WIDTH + self.rect.width / 2

        # !! Back to movement !!
        self.rect.midbottom = self.position
        # !! Movement-2 FIN !!

    def animate(self):
        """ To use: self.animate()
        This method animates the player. """

        now = pg.time.get_ticks()

        ## Changing variables
        if self.velocity.x != 0:
            self.walking = True
        else:
            self.walking = False

        #### Walking Animation:
        if self.walking:
            if now - self.lastUpdate > 200:
                self.lastUpdate = now

                self.currentFrame = (self.currentFrame + 1) % len(self.leftWalkingFrames) # Updating the current frame

                # Updating rectangle:
                bottom = self.rect.bottom

                # Picking which direction we are walking:
                if self.velocity.x > 0:
                    self.image = self.rightWalkingFrames[self.currentFrame]
                else:
                    self.image = self.leftWalkingFrames[self.currentFrame]
                # Direction FIN

                # Back to updating rectangle:
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

        #### Idle Animation:
        if not self.jumping and not self.walking:
            if now - self.lastUpdate > 250:
                # Updating time and frame:
                self.lastUpdate = now
                self.currentFrame = (self.currentFrame + 1) % len(self.standingFrames)
                # FIN

                # Updating rectangle
                bottom = self.rect.bottom

                self.image = self.standingFrames[self.currentFrame] #Updating the animation again

                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        #### Idle Animation FIN

class Platform(pg.sprite.Sprite):
    """ To use: Platform()
    This is the Platform class. This class creates and maintains every platform that appears on the screen. """
    def __init__(self, game, x, y):
        pg.sprite.Sprite.__init__(self)

        self.game = game

        # Collecting the platform images
        platImages = [self.game.spritesheet.getImage(0, 288, 380, 94),
                      self.game.spritesheet.getImage(213, 1662, 201, 100)]

        self.image = choice(platImages)

        self.image.set_colorkey(BLACK)

        # Setting up the boundary rectangle:
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        # Rectangle FIN