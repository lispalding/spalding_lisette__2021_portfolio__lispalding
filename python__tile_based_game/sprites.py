# MADE BY: Lisette Spalding
# ART WORK CREDIT: "Kenney.nl" @ "www.kenney.nl"
# BACKGROUND MUSIC CREDIT: DIVELA
# SONG TITLE & YOUTUBE LINK: Vocalo-Colosseum @ https://youtu.be/5kIeUb5AE4s
# FILE NAME: sprites.py
# PROJECT NAME: python__tile_based_game
# DATE CREATED: 03/05/2021
# DATE LAST MODIFIED: 05/13/2021
# PYTHON VER. USED: 3.x

##################### IMPORTS ######################
import pygame as pg
import random as r
from os import path
import pytweening as tween

# Custom imports
from settings import *
from tilemap import collideHitRect
##################### FINISHED #####################

################### GLOBAL VAR #####################
vec = pg.math.Vector2
##################### FINISHED #####################

################ GLOBAL FUNCTIONS ##################
def collideWithWalls(sprite, group, dir):
    """ To use: self.collideWithWalls(dir)
    This is the method that checks to see if the player has collided with a wall, and how to deal with it. """
    if dir == "x":
        hits = pg.sprite.spritecollide(sprite, group, False, collideHitRect)
        if hits:
            if hits[0].rect.centerx > sprite.hitRect.centerx:
                sprite.position.x = hits[0].rect.left - sprite.hitRect.width / 2
            if hits[0].rect.centerx < sprite.hitRect.centerx:
                sprite.position.x = hits[0].rect.right + sprite.hitRect.width / 2

            sprite.velocity.x = 0
            sprite.hitRect.centerx = sprite.position.x

    if dir == "y":
        hits = pg.sprite.spritecollide(sprite, group, False, collideHitRect)
        if hits:
            if hits[0].rect.centery > sprite.hitRect.centery:
                sprite.position.y = hits[0].rect.top - sprite.hitRect.height / 2
            if hits[0].rect.centery < sprite.hitRect.centery:
                sprite.position.y = hits[0].rect.bottom + sprite.hitRect.height / 2

            sprite.velocity.y = 0
            sprite.hitRect.centery = sprite.position.y
##################### FINISHED #####################

##################### CLASSES ######################
class Spritesheet():
    """ To use: Spritesheet()
        This class will parse and load spritesheets. """
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def getImage(self, x, y, width, height):
        """ To use: getImage(x, y, width, height)
        This method obtains an image, grabbing it from the larger spritesheet. """
        # Grabbing an image out of a larger spritesheet
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0,0), (x, y, width, height))

        return image

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        super(Player, self).__init__()

        self._layer = PLAYER_LAYER

        ## Adding things to groups
        self.groups = game.allSprites
        pg.sprite.Sprite.__init__(self, self.groups)

        self.game = game

        # self.image = pg.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        # self.image.fill(PURPLE)

        self.image = self.game.playerImage

        # self.image = self.game.spritesheet.getImage(263, 132, 49, 43)
        # self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.hitRect = PLAYER_HIT_RECT
        self.hitRect.center = self.rect.center

        # Including vectors for movement and positioning
        self.velocity = vec(0, 0)
        self.position = vec(x, y)

        self.rotation = 0 # This variable tracks how much (how far) the player has rotated. Allowing the sprite to face in more than one direction.

        ## Traditional Placement, speed, etc
        # # self.rect.center = (WIDTH/2, HEIGHT/2)
        # self.vx, self.vy = 0, 0
        # self.x = x * TILE_SIZE
        # self.y = y * TILE_SIZE
        # ## Placement FIN
        #
        # self.speedx = 0
        # self.speedy = 0

        self.lastShot = 0 # Setting the last shot time

        self.health = PLAYER_HEALTH # Setting up the player health

    def getKeys(self):
        """ To use: self.getKeys()
        This is the method that acquires the keys pressed and determines what to do """
        self.rotationSpeed = 0
        self.velocity = vec(0, 0)

        keys = pg.key.get_pressed() # Obtaining the key pressed
        # If the key pressed is the left arrow key OR the "a" key, then do this:
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.rotationSpeed = PLAYER_ROTATION_SPEED

        # If the key pressed is the right arrow key OR the "d" key, then do this:
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.rotationSpeed = -PLAYER_ROTATION_SPEED

        # If the key pressed is the up arrow key OR the "w" key, then do this:
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.velocity = vec(PLAYER_SPEED, 0).rotate(-self.rotation)

        # If the key pressed is the down arrow key OR the "s" key, do this:
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.velocity = vec(-PLAYER_SPEED / 2, 0).rotate(-self.rotation)

        # If the key pressed is the space bar, do this:
        if keys[pg.K_SPACE]:
            now = pg.time.get_ticks()

            if now - self.lastShot > FIRING_RATE:
                self.lastShot = now

                direction = vec(1, 0).rotate(-self.rotation)
                position = self.position + BARREL_OFFSET.rotate(-self.rotation)

                Bullet(self.game, position, direction)

                self.velocity = vec(-KICKBACK, 0).rotate(-self.rotation)

                r.choice(self.game.weaponSounds["gun"]).play()

                MuzzleFlash(self.game, position)

        # SOLVING DIAGONAL ISSUE: !! NO LONGER NEEDED !!
        # If the x velocity does not equal zero and the y velocity does not equal zero, do this:
        # if self.velocity.x != 0 and self.velocity.y != 0:
        #     self.velocity *= 0.7071

    def update(self):
        """ To use: self.update()
        This is the method that will update the movement of the player character. """
        ##### !! Basic Movement !! #####
        # self.speedx = 0
        # self.speedy = 0

        # Cheking the Keystate
        keystate = pg.key.get_pressed()

        ## Custom movement:
        self.getKeys()

        self.rotation = (self.rotation + self.rotationSpeed * self.game.dt) % 360

        # Taking care of image rotation:
        self.image = pg.transform.rotate(self.game.playerImage, self.rotation)

        self.rect = self.image.get_rect()
        self.rect.center = self.position
        # Rotation FIN

        self.position += self.velocity * self.game.dt

        # Setting up wall collision
        self.hitRect.centerx = self.position.x
        collideWithWalls(self, self.game.walls, "x")

        self.hitRect.centery = self.position.y
        collideWithWalls(self, self.game.walls, "y")

        self.rect.center = self.hitRect.center

    def addHealth(self, amount):
        """ To use: self.addHealth
        This method restores health to the player, but only when they've crossed a healing item. """
        self.health += amount

        if self.health > PLAYER_HEALTH:
            self.health = PLAYER_HEALTH

class Zombie(pg.sprite.Sprite):
    """ To use: Zombie()
    This class will create an NPC (In this case, a zombie). """
    def __init__(self, game, x, y):
        self._layer = ZOMBIE_LAYER

        # Setting up the groups
        self.groups = game.allSprites, game.zombieGroup
        pg.sprite.Sprite.__init__(self, self.groups)

        self.game = game

        self.image = game.zombieImage.copy()
        self.rect = self.image.get_rect() # Setting up the rectangle
        self.rect.center = (x, y)
        self.hitRect = ZOMBIE_HIT_RECT.copy()
        self.hitRect.center = self.rect.center

        # Setting up movement:
        self.position = vec(x, y)
        self.velocity = vec(0, 0)
        self.acceleration = vec(0, 0)

        # Setting up spawn point(s):
        self.rect.center = self.position

        # Setting up the zombie movement
        self.rotation = 0

        # Setting up zombie health
        self.health = ZOMBIE_HEALTH

        # Setting up zombie speed
        self.speed = r.choice(ZOMBIE_SPEEDS)

        # Saying the target of the Zombie drool
        self.target = game.player

    def avoidZombies(self):
        """ To use: self.avoidZombies
        This is the method that tells the zombies to avoid the other zombies. """

        for zombie in self.game.zombieGroup:
            if zombie != self:
                distance = self.position - zombie.position
                if 0 < distance.length() < AVOID_RADIUS:
                    self.acceleration += distance.normalize()

    def update(self):
        """ To use: self.update()
        This is the method that will update the movement of the zombie character. """
        ######### ROTATION START:
        targetDistance = self.target.position - self.position

        if targetDistance.length_squared() < DETECT_RADIUS ** 2:
            if r.random() < 0.002: # Playing a zombie sound if the zombie is chasing player
                r.choice(self.game.zombieMoanSounds).play()

            self.rotation = targetDistance.angle_to(vec(1, 0))

            self.image = pg.transform.rotate(self.game.zombieImage, self.rotation) # Rotating the mob image as it faces player
            self.rect = self.image.get_rect()
            self.rect.center = self.position
            ######### ROTATION FIN

            ######### MOVEMENT START:
            self.acceleration = vec(1, 0).rotate(-self.rotation)
            self.avoidZombies()
            self.acceleration.scale_to_length(self.speed)
            self.acceleration += self.velocity * -1
            self.velocity += self.acceleration * self.game.dt
            self.position += self.velocity * self.game.dt + 0.5 * self.acceleration * self.game.dt ** 2

            # Resetting rectangle
            self.hitRect.centerx = self.position.x
            collideWithWalls(self, self.game.walls, "x")
            self.hitRect.centery = self.position.y
            collideWithWalls(self, self.game.walls, "y")

            self.rect.center = self.hitRect.center
            ######### MOVEMENT FIN

        ######### HEALTH/DEATH START:
        if self.health <= 0:
            r.choice(self.game.zombieHitSounds).play()
            self.kill()
        ######### HEALTH/DEATH FIN

    def drawHealth(self):
        """ To use: drawHealth()
        This method draws the zombie's health in a health bar above it's head. """
        #### Setting up the colors
        if self.health > 60:
            color = GREEN
        elif self.health > 30:
            color =  YELLOW
        else:
            color = RED

        #### Setting up the bar itself
        width = int(self.rect.width * self.health / 100)

        self.healthBar = pg.Rect(0, 0, width, 7)
        if self.health < 100:
            pg.draw.rect(self.image, color, self.healthBar)

class Bullet(pg.sprite.Sprite):
    """ To use: Bullet()
    This is the Bullet Class. This class controls the bullets being shot by the player."""
    def __init__(self, game, position, direction):
        self._layer = BULLET_LAYER

        self.groups = game.allSprites, game.bulletGroup
        pg.sprite.Sprite.__init__(self, self.groups)

        self.game = game

        self.image = game.bulletImage
        self.rect = self.image.get_rect()

        self.hitRect = self.rect

        self.position = vec(position)
        self.rect.center = position

        self.rect.center = position

        spread = r.uniform(-GUN_SPREAD, GUN_SPREAD)
        self.velocity = direction.rotate(spread) * BULLET_SPEED

        self.spawnTime = pg.time.get_ticks() # Tracking the spawn time so we know when to delete the bullet

    def update(self):
        """ To use: self.update()
        This is the method that will update the movement of the bullet. """

        self.position += self.velocity * self.game.dt
        self.rect.center = self.position

        if pg.sprite.spritecollideany(self, self.game.walls): # Don't care what wall it hits, if it hits any wall do this:
            self.kill()

        if pg.time.get_ticks() - self.spawnTime > BULLET_LIFESPAN:
            self.kill()

class Wall(pg.sprite.Sprite):
    """ To use: Wall()
    This class creates walls in the game-- Dependent on the maps."""
    def __init__(self, game, x, y):
        self._layer = WALL_LAYER

        # Setting up the groups
        self.groups = game.allSprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)

        # Initializing the Game variable
        self.game = game
        self.image = game.wallImage

        # self.image = pg.Surface((TILE_SIZE, TILE_SIZE))
        # self.image.fill(GREEN) # Filling the walls with green

        self.rect = self.image.get_rect()

        self.x = x
        self.y = y

        self.rect.x = x * TILE_SIZE
        self.rect.y = y * TILE_SIZE

class Obstacle(pg.sprite.Sprite):
    """ To use: Wall()
    This class creates walls in the game-- Dependent on the maps."""
    def __init__(self, game, x, y, width, height):
        self._layer = WALL_LAYER

        self.groups = game.walls
        pg.sprite.Sprite.__init__(self, self.groups)

        self.rect = pg.Rect(x, y, width, height)

        self.x = x
        self.y = y

        self.rect.x = x
        self.rect.y = y

class MuzzleFlash(pg.sprite.Sprite):
    """ To use: MuzzleFlash()
    This class is the muzzle flash class, it creates the flash of the gun when it fires a bullet."""
    def __init__(self, game, position):
        self._layer = EFFECTS_LAYER

        self.groups = game.allSprites
        pg.sprite.Sprite.__init__(self, self.groups)

        self.game = game

        # Setting up the rectangle
        size = r.randint(20, 50)
        self.image = pg.transform.scale(r.choice(game.gunFlashes), (size, size))

        self.rect = self.image.get_rect()

        # Setting up the position of the flash
        self.position = position
        self.rect.center = position

        # Setting up the time the flash stays
        self.spawnTime = pg.time.get_ticks()

    def update(self):
        if pg.time.get_ticks() - self.spawnTime > FLASH_DURATION:
            self.kill()

class Item(pg.sprite.Sprite):
    """To use: Item()
    This class loads and displays the item sprites. """
    def __init__(self, game, position, type):
        self._layer = ITEMS_LAYER

        self.groups = game.allSprites, game.itemsGroup
        pg.sprite.Sprite.__init__(self, self.groups)

        self.image = game.itemImages[type]

        self.rect = self.image.get_rect()

        self.type = type

        self.position = position
        self.rect.center = position

        # Setting up tweening: A way of motion for an icon
        self.tween = tween.easeInOutSine
        self.step = 0
        self.direction = 1

    def update(self):
        # Bobbing motion:
        offset = BOBBING_RANGE * (self.tween(self.step / BOBBING_RANGE) - 0.5)

        self.rect.centery = self.position.y + offset * self.direction

        self.step += BOBBING_SPEED
        if self.step > BOBBING_RANGE:
            self.step = 0
            self.direction *= -1
##################### FINISHED #####################