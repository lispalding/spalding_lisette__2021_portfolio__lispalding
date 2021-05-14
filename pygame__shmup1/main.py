# MADE BY: Lisette Spalding
# ART WORK CREDIT: "Kenney.nl" @ "www.kenney.nl"
# FILE NAME: main.py
# PROJECT NAME: python_shmup
# DATE CREATED: 02/25/2021
# DATE LAST MODIFIED: 04/01/2021
# PYTHON VER. USED: 3.8

########### !! IMPORTS !! ############
import pygame as pg
from pygame.locals import *
import random as r
from colors import *
from math import *
from os import *
############## !! FIN !! ###############

########### !! CONSTANTS !! ############
title = "Shmup"

WIDTH = 300
HEIGHT = 600

debugging = False

POWERUP_TIME = 5000
############## !! FIN !! ###############

############# !! ASSETS !! #############
gameFolder = path.dirname(__file__)
imageDirectory = path.join(gameFolder, "images")
soundDirectory = path.join(gameFolder, "sounds")

## Image Directories
backgroundImgDir = path.join(imageDirectory, "background")
bulletImgDir = path.join(imageDirectory, "bullet")
meteorImgDir = path.join(imageDirectory, "meteor")
playerImgDir = path.join(imageDirectory, "player")
explosionImgDir = path.join(imageDirectory, "explosions")
powerupsImgDir = path.join(imageDirectory, "power_ups")

## Sound Directories
fillerSoundDir = path.join(soundDirectory, "filler_sound")
ambientSoundDir = path.join(soundDirectory, "ambient_fx")
musicSoundDir = path.join(soundDirectory, "music")
fxSoundsDir = path.join(soundDirectory, "sound_fx")
############## !! FIN !! ###############

############# !! CLASSES !! ############
class Player(pg.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__() # Setting the __init__ function as the super class
        # self.image = pg.Surface((20, 40)) # Setting the height and width of the player sprite
        # self.image.fill(GREEN) # Filling the sprite image a certain color

        # Creating the player image:
        self.image = playerImage
        self.image = pg.transform.scale(playerImage, (50, 38))
        self.image.set_colorkey(BLACK)

        # Creating a bound box around the image:
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.85 / 2)
        if debugging:
            pg.draw.circle(self.image, RED, self.rect.center, self.radius)

        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH/2
        self.rect.bottom = (HEIGHT - (HEIGHT*.05))

        self.speedx = 0

        self.shield = 100
        self.fuel = 100
        self.FUEL_SUBTRACTION = 8

        self.shootDelay = 250
        self.lastShot = pg.time.get_ticks()

        self.lives = 3

        self.hidden = False
        self.hideTimer = pg.time.get_ticks()

        self.powerLevel = 1
        self.powerTimer = pg.time.get_ticks()

        self.keypressed = False

    def powerup(self):
        """ To use: self.powerup()
        This method causes the power level of the gun to go up"""
        gunPowerSound.play()

        self.powerLevel += 1
        self.powerTimer = pg.time.get_ticks()

    def shoot(self):
        """ To use: self.shoot()
        This function causes a bullet to be shot by the player. """
        now = pg.time.get_ticks()

        if now - self.lastShot > self.shootDelay:
            self.lastShot = now

            if self.powerLevel == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                bulletGroup.add(bullet)
                allSprites.add(bullet)
            if self.powerLevel >= 2:
                bullet1 = Bullet(self.rect.right, self.rect.centery)
                bullet2 = Bullet(self.rect.left, self.rect.centery)
                bulletGroup.add(bullet1)
                allSprites.add(bullet1)
                bulletGroup.add(bullet2)
                allSprites.add(bullet2)

    def getHit(self, radius):
        # self.shield -= radius*2
        pass

    def hide(self):
        """ To use: self.hide()
        This function hides the player (With immunity) temporarily. """
        self.hidden = True
        self.hideTimer = pg.time.get_ticks()

        self.rect.center = (WIDTH /2, (HEIGHT - (HEIGHT*.05)))

    def togglePressed(self):
        """ To use: self.togglePressed()
         This is the function that will check to see if a keypress is False. """
        self.keypressed = False
        self.speedx = 0

    def update(self):
        """ To use: self.update()
         This is the function that will update the movement of the player character. """
        keystate = pg.key.get_pressed() # Checking the Keystate, whether it is pressed or not

        ########## !!!! .. FLOW MOVEMENT .. !!!! ##########
        if self.keypressed == False:
            if (keystate[pg.K_LEFT] or keystate[pg.K_a]) and player.fuel > 0:
                self.speedx += -8
                self.fuel -= self.FUEL_SUBTRACTION
                self.keypressed = True

            if (keystate[pg.K_RIGHT] or keystate[pg.K_d]) and player.fuel > 0:
                self.speedx += 8
                self.fuel -= self.FUEL_SUBTRACTION
                self.keypressed = True

        self.rect.x += self.speedx
        ########## !!!! .. FLOW FINISHED .. !!!! ##########

        ### Unhide if hidden
        if self.hidden and pg.time.get_ticks() - self.hideTimer > 2000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10

        ### Timeout for powerups
        if self.powerLevel >= 2 and pg.time.get_ticks() - self.powerTimer > POWERUP_TIME:
            self.powerLevel -= 1
            self.powerTimer = pg.time.get_ticks()

        ### Shoot if Space Bar is pressed
        if self.keypressed == False:
            if keystate[pg.K_SPACE]:
                shootSound.play()
                self.shoot()

        ######### !!!! .. SCREEN BINDING .. !!!! ##########
        ## Binding player to screen area...
        if self.rect.left <= 0:
            self.rect.left = 0

        if self.rect.top <= 0:
            self.rect.top = 0

        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT

        if self.rect.right >= WIDTH:
            self.rect.right = WIDTH
        ######### !!!! .. BINDING FINISH .. !!!! ##########

class Bullet(pg.sprite.Sprite):
    def __init__(self, x, y):
        super(Bullet, self).__init__()

        ## Creating the bullet image
        # self.image = pg.Surface((10, 20))  # Setting the height and width of the player sprite
        # self.image.fill(BLUE)  # Filling the sprite image a certain color

        # Creating the player image:
        self.image = bulletImage
        self.image = pg.transform.scale(bulletImage, (8, 25))
        self.image.set_colorkey(BLACK)

        # Creating a bound box around the image:
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.85 / 2)
        if debugging:
            pg.draw.circle(self.image, RED, self.rect.center, self.radius)

        # Positioning the bullet
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y

        self.speedy = -5

    def update(self):
        """ To use: self.update()
                 This function constantly updates the image of the Bullet. """
        self.rect.y += self.speedy

        if self.rect.bottom < 0:
            self.kill()

class NPC(pg.sprite.Sprite):
    def __init__(self):
        super(NPC, self).__init__()  # Setting the __init__ function as the super class
        # self.image = pg.Surface((20, 20))  # Setting the height and width of the player sprite
        # self.image.fill(RED)  # Filling the sprite image a certain color

        ## Random width and height of image
        self.randHeight = r.randrange(8, 65)
        self.randWidth = r.randrange(8, 65)

        self.imageOrig = r.choice(meteorImages)
        self.imageOrig = pg.transform.scale(self.imageOrig, (self.randWidth, self.randHeight))
        self.imageOrig.set_colorkey(BLACK)
        self.image = self.imageOrig.copy()

        # Creating the player image:
        # self.image = theNpcImage
        # self.image.set_colorkey(BLACK)

        ## Creating a bound box around the image:
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.85 / 2)

        if debugging:
            # Draws a red circle on the image if debugging = True
            pg.draw.circle(self.image, RED, self.rect.center, self.radius)

        self.rect.x = r.randrange(WIDTH - self.rect.width)
        self.rect.y = (HEIGHT * .08)

        ## Setting the speed
        self.randSpeedX = r.randrange(-3,3)
        self.randSpeedY = r.randrange(1,8)

        self.speedx = self.randSpeedX
        self.speedy = self.randSpeedY

        ## Setting up rotation:
        self.rotation = 0
        self.rotationSpeed = r.randint(-8, 8)
        self.lastUpdate = pg.time.get_ticks()

    def rotate(self):
        """ To use: self.rotate()
         This function rotates an image. """
        now = pg.time.get_ticks()

        if now - self.lastUpdate > 60:
            self.lastUpdate = now # Setting the last update time to now...

            ## Rotating sprite
            self.rotation = (self.rotation + self.rotationSpeed) % 360

            newImage = pg.transform.rotate(self.imageOrig, self.rotation)
            oldCenter = self.rect.center

            self.image = pg.transform.rotate(self.imageOrig, self.rotation)
            self.rect = self.image.get_rect()
            self.rect.center = oldCenter

    def update(self):
        """ To use: self.update()
         This function constantly updates the image of the NPC. """
        self.rotate()

        self.rect.x += self.speedx
        self.rect.y += self.speedy

        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH +20:
            self.rect.x = r.randrange(WIDTH - self.rect.width)
            self.rect.y = r.randrange(-100, -40)
            self.speedy = r.randrange(1, 8)

class Explosion(pg.sprite.Sprite):
    def __init__(self, center, size):
        pg.sprite.Sprite.__init__(self)

        self.size = size
        self.image = explosionAnimation[self.size][0]

        self.rect = self.image.get_rect()
        self.rect.center = center

        self.frame = 0

        self.lastUpdate = pg.time.get_ticks()
        self.frameRate = 60

    def update(self):
        now = pg.time.get_ticks()

        if now - self.lastUpdate > self.frameRate:
            self.lastUpdate = now
            self.frame += 1

            if self.frame == len(explosionAnimation[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosionAnimation[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

class Powerup(pg.sprite.Sprite):
    def __init__(self, center):
        super(Powerup, self).__init__()

        pg.sprite.Sprite.__init__(self)

        self.type = r.choice(["gun", "gun", "gun", "shield", "shield", "shield", "shield", "shield", "shield",
                              "lives", "lives", "lives", "fuel", "fuel", "fuel", "fuel", "fuel", "alienPow", "alienPow",
                              "alienPow", "alienPow", "alienPoints", "alienPoints", "alienPoints"])

        # Creating the powerup image:
        self.image = powerupImages[self.type]

        if self.image == (powerupImages["alienPow"] or powerupImages["alienPoints"]):
            self.image.set_colorkey(RED_TRANSPARENT)
        if self.image != (powerupImages["alienPow"] or powerupImages["alienPoints"]):
            self.image.set_colorkey(BLACK)

        # Creating a bound box around the image:
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.85 / 2)
        if debugging:
            pg.draw.circle(self.image, RED, self.rect.center, self.radius)

        # Positioning the bullet
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 2

    def update(self):
        """ To use: self.update()
                 This function constantly updates the image of the Bullet. """
        self.rect.y += self.speedy

        if self.rect.bottom < 0:
            self.kill()
############## !! FIN !! ###############

######### !! INITIALIZATION !! #########
pg.init()
pg.mixer.init()

screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption(title)
clock = pg.time.Clock()

fontName = pg.font.match_font("arial")
############## !! FIN !! ###############

########### !! LOAD SOUNDS !!###########
shootSound = pg.mixer.Sound(path.join(fxSoundsDir, "RetroLaser3.wav"))

playerHitSound = pg.mixer.Sound(path.join(fxSoundsDir, "Hit4.wav"))

shieldSound = pg.mixer.Sound(path.join(fxSoundsDir, "UI1.wav"))
gunPowerSound = pg.mixer.Sound(path.join(fxSoundsDir, "Upgrade2.wav"))
livesSound = pg.mixer.Sound(path.join(fxSoundsDir, "Square3.wav"))

fuelPowSound = pg.mixer.Sound(path.join(fxSoundsDir, "Alert1.wav"))
fuelRefillSound = pg.mixer.Sound(path.join(fxSoundsDir, "Scratch2.wav"))
fuelEmptySound = pg.mixer.Sound(path.join(fxSoundsDir, "Bump3.wav"))

alienSpawnSound = pg.mixer.Sound(path.join(fxSoundsDir, "Spectra1.wav"))
alienHitSound = pg.mixer.Sound(path.join(fxSoundsDir, "SFX7.wav"))

explosionSounds = []
for snd in ["Explosion 5.wav", "Explosion 1.wav"]:
    s = pg.mixer.Sound(path.join(fxSoundsDir, snd))
    s.set_volume(0.72)

    explosionSounds.append(s)

pg.mixer.music.load(path.join(musicSoundDir, "MattOglseby - 6.ogg"))
pg.mixer.music.set_volume(0.5)
############## !! FIN !! ###############

########### !! LOAD IMAGES !! ###########
## Loading all game graphics
## Background ##
background = pg.image.load(path.join(backgroundImgDir, "starfield.png")).convert()
background_rect = background.get_rect()

## Player Image ##
playerImage = pg.image.load(path.join(playerImgDir, "playerShip1_orange.png")).convert()

## Lives Image ##
playerLivesImage = pg.image.load(path.join(playerImgDir, "playerShip1_orange.png")).convert()
playerLivesImageMini = pg.transform.scale(playerLivesImage, (25, 19))
playerLivesImageMini.set_colorkey(BLACK)

## NPC Image ##
meteorImages = []
npcImages = ["meteorBrown_big1.png", "meteorBrown_big2.png", "meteorBrown_big3.png",
             "meteorBrown_big4.png", "meteorBrown_med1.png", "meteorBrown_med3.png",
             "meteorBrown_small1.png", "meteorBrown_small2.png", "meteorBrown_tiny1.png",
             "meteorBrown_tiny2.png", "meteorGrey_big1.png", "meteorGrey_big2.png",
             "meteorGrey_big3.png", "meteorGrey_big4.png", "meteorGrey_med1.png",
             "meteorGrey_med2.png", "meteorGrey_small1.png", "meteorGrey_small2.png",
             "meteorGrey_tiny1.png", "meteorGrey_tiny2.png"]

for image in npcImages:
    meteorImages.append(pg.image.load(path.join(meteorImgDir, image)).convert())

## Bullet Image ##
bulletImage = pg.image.load(path.join(bulletImgDir, "laserRed16.png")).convert()

## Explosion Image ##
explosionAnimation = {}
explosionAnimation["lg"] = []
explosionAnimation["sm"] = []
explosionAnimation["player"] = []

for i in range(9):
    filename = "regularExplosion0{}.png".format(i)
    image = pg.image.load(path.join(explosionImgDir, filename)).convert()
    image.set_colorkey(BLACK)

    imageLg = pg.transform.scale(image, (75, 75))
    explosionAnimation["lg"].append(imageLg)

    imageSm = pg.transform.scale(image, (32, 32))
    explosionAnimation["sm"].append(imageSm)

    filename = "sonicExplosion0{0}.png".format(i)
    image = pg.image.load(path.join(explosionImgDir, filename)).convert()
    image.set_colorkey(BLACK)

    explosionAnimation["player"].append(image)

## Powerups Images ##
playerLivesImagePow = pg.image.load(path.join(playerImgDir, "playerShip1_orange.png")).convert()
playerLivesImageMiniPow = pg.transform.scale(playerLivesImagePow, (20, 14))

gunPowImage = pg.image.load(path.join(powerupsImgDir, "powerupRed_bolt.png")).convert()
gunPowImageMini = pg.transform.scale(gunPowImage, (20, 20))

shieldPowImage = pg.image.load(path.join(powerupsImgDir, "powerupBlue_shield.png")).convert()
shieldPowImageMini = pg.transform.scale(shieldPowImage, (20, 20))

fuelPowImage = pg.image.load(path.join(powerupsImgDir, "powerupYellow_bolt.png")).convert()
fuelPowImageMini = pg.transform.scale(fuelPowImage, (20, 20))

alienPowImage = pg.image.load(path.join(powerupsImgDir, "alien_pow.png")).convert()
alienPowImageMini = pg.transform.scale(alienPowImage, (20, 20))

alienExtraPointImage = pg.image.load(path.join(powerupsImgDir, "alien_extra_points.png")).convert()
alienExtraPointImageMini = pg.transform.scale(alienExtraPointImage, (20, 20))

powerupImages = {}
powerupImages["shield"] = shieldPowImageMini
powerupImages["gun"] = gunPowImageMini
powerupImages["fuel"] = fuelPowImageMini
powerupImages["lives"] = playerLivesImageMiniPow
powerupImages["alienPow"] = alienPowImageMini
powerupImages["alienPoints"] = alienExtraPointImageMini
############## !! FIN !! ###############

########## !! GAME OBJECTS !! ###########
######### .. SPRITES .. ##########
player = Player()

allSprites = pg.sprite.Group()
playersGroup = pg.sprite.Group()
npcGroup = pg.sprite.Group()
bulletGroup = pg.sprite.Group()

powerups = pg.sprite.Group()

alienPower = pg.sprite.Group()

# Adding Player and NPC to sprite groups
playersGroup.add(player)

for i in range(3):
    npc = NPC()
    npcGroup.add(npc)

# Auto adding sprites to allSprites group
for i in playersGroup:
    allSprites.add(i)

for i in npcGroup:
    allSprites.add(i)
############## !! FIN !! ###############

############ !! GAME LOOP !! ###########
### .. GAME UPDATE VARIABLES ###
playing = True
score = 0
level = 1
difficulty = 0

FPS = 60

pg.mixer.music.play(loops = -1)
########## .. FIN .. ###########

######### !! GAME FUNCTIONS !! #########
def drawText(surface, text, size, x, y):
    """ To use: drawText(surface, text, size, x, y)
    This function draws the text on the screen. """
    font = pg.font.Font(fontName, size)
    textSurface = font.render(text, True, WHITE)
    textRect = textSurface.get_rect()
    textRect.midtop = (x, y)
    surface.blit(textSurface, textRect)

def drawShieldBar(surface, x, y, pct):
    """ To use: drawShieldBar(surface, x, y, pct)
     This function draws the shield bar on the screen. """
    if pct < 0:
        pct = 0

    BAR_LENGTH = 100
    BAR_HEIGHT = 20

    fill = (pct / 100) * BAR_LENGTH
    outlineRect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fillRect = pg.Rect(x, y, fill, BAR_HEIGHT)

    pg.draw.rect(surface, BLUE, fillRect)
    pg.draw.rect(surface, WHITE, outlineRect, 1)

def drawFuelBar(surface, x, y, pct):
    """ To use: drawShieldBar(surface, x, y, pct)
     This function draws the shield bar on the screen. """
    if pct < 0:
        pct = 0

    BAR_LENGTH = 100
    BAR_HEIGHT = 20

    fill = (pct / 100) * BAR_LENGTH
    outlineRect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fillRect = pg.Rect(x, y, fill, BAR_HEIGHT)

    pg.draw.rect(surface, YELLOW, fillRect)
    pg.draw.rect(surface, WHITE, outlineRect, 1)

def drawLives(surface, x, y, lives, image):
    """ To use: drawLives(surface, x, y, lives, image)
     This function draws the lives icons on the screen. """
    for i in range(lives):
        imgRect = image.get_rect()
        imgRect.x = x + 30 * i
        imgRect.y = y
        surface.blit(image, imgRect)

def spawnNpc():
    """ To use: spawnNPC()
     This function spawns an NPC. """
    npc = NPC()
    npcGroup.add(npc)
    allSprites.add(npc)
######### !! GAME FUNC FINISH !! #######

######## .. GAME LOOP .. ########
while playing:
    ### Timing
    clock.tick(FPS)  # Controlling the loop

    ### Collecting Input
    ##### Processing input ######
    for event in pg.event.get():  # Getting a list of events that have happened
        if event.type == pg.KEYUP: ## Getting if a key has been released
            if (event.key == pg.K_LEFT) or (event.key == pg.K_a):
                player.togglePressed()

            if (event.key == pg.K_RIGHT) or (event.key == pg.K_d):
                player.togglePressed()

            if (event.key == pg.K_UP) or (event.key == pg.K_w):
                player.togglePressed()

            if (event.key == pg.K_DOWN) or (event.key == pg.K_s):
                player.togglePressed()

        ### TEMPORARY FIX FOR BULLETS ###
        # if event.type == KEYDOWN:
        #     if event.key == pg.K_SPACE:
        #         player.shoot()
        ####### FIN TEMPORARY FIX #######

        if event.type == pg.QUIT: ## Quitting the game when we hit "x" or hits escape
            playing = False
        if event.type == pg.KEYDOWN:
            if event.key == K_ESCAPE:
                playing = False

    ### Updating Section
    ## If NPC hits Player
    hits = pg.sprite.spritecollide(player, npcGroup, True, pg.sprite.collide_circle)

    for hit in hits:
        player.shield -= hit.radius * 2
        playerHitSound.play()
        explosion = Explosion(hit.rect.center, "sm")
        allSprites.add(explosion)
        spawnNpc()
        if player.shield <= 0 and pg.time.get_ticks() - player.hideTimer > 1000:
            deathExplosion = Explosion(player.rect.center, "player")
            allSprites.add(deathExplosion)

            player.hide()

            player.lives -= 1
            player.shield = 100

            if player.lives == 0 and not deathExplosion.alive():
                running = False

    ## If Bullet hits NPC
    hits = pg.sprite.groupcollide(npcGroup, bulletGroup, True, True)

    for hit in hits: # Spawning an NPC when an asteroid hits bullet
        score += 50 - hit.radius
        r.choice(explosionSounds).play()
        explosion = Explosion(hit.rect.center, "lg")
        allSprites.add(explosion)

        if r.random() > 0.9:
            pow = Powerup(hit.rect.center)
            allSprites.add(pow)
            powerups.add(pow)
        spawnNpc()


    ## If player hits a Powerup
    hits = pg.sprite.spritecollide(player, powerups, True)

    for hit in hits:
        if hit.type == "shield":
            shieldSound.play()
            if player.shield >= 100:
                player.shield += r.randrange(10, 30)
                if player.shield >= 100:
                    player.shield = 100

        if hit.type == "lives":
            livesSound.play()
            if player.lives > 3:
                player.lives = 3
            if player.lives == 3:
                player.lives = 4

        if hit.type == "fuel":
            fuelRefillSound.play()

            choice = r.random()
            if (player.fuel < 100) and choice < 0.7:
                player.fuel += r.randrange(10, 30)
                if player.fuel >= 100:
                    player.fuel = 100
            if choice >= 0.7 or player.fuel == 100:
                fuelPowSound.play()
                if player.FUEL_SUBTRACTION == 8:
                    player.FUEL_SUBTRACTION = 5
                elif player.FUEL_SUBTRACTION == 5:
                    player.FUEL_SUBTRACTION = 2

        if hit.type == "gun":
            player.powerup()

        if hit.type == "alienPow":
            choice = r.randint(1, 5)
            if choice == 1:
                shieldSound.play()
                if player.shield >= 100:
                    player.shield += r.randrange(10, 30)
                    if player.shield >= 100:
                        player.shield = 100
            if choice == 2:
                fuelRefillSound.play()
                if player.fuel <= 100:
                    player.fuel += r.randrange(10, 30)
                    if player.fuel >= 100:
                        player.fuel = 100
            if choice == 3:
                fuelPowSound.play()
                if player.fuel >= 100:
                    if player.FUEL_SUBTRACTION == 8:
                        player.FUEL_SUBTRACTION = 5
                    elif player.FUEL_SUBTRACTION == 5:
                        player.FUEL_SUBTRACTION = 2
            if choice == 4:
                if player.lives > 3:
                    livesSound.play()
                    player.lives = 3
                if player.lives == 3:
                    livesSound.play()
                    player.lives = 4
            if choice == 5:
                player.powerup()

        if hit.type == "alien_extra_point":
            alienHitSound.play()
            score += 500

    allSprites.update()

    ### Display Changes / Render
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    allSprites.draw(screen)

    drawText(screen, str(score), 25, WIDTH / 2, 10)
    drawLives(screen, WIDTH - 100, 5, player.lives, playerLivesImageMini)
    drawShieldBar(screen, 5, 5, player.shield)
    drawFuelBar(screen, 5, 30,  player.fuel)

    pg.display.flip()
########## .. FIN .. ###########

pg.quit()
############## !! FIN !! ###############

