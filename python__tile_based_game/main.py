# MADE BY: Lisette Spalding
# ART WORK CREDIT: "Kenney.nl" @ "www.kenney.nl"
# BACKGROUND MUSIC CREDIT: DIVELA
# SONG TITLE & YOUTUBE LINK: Vocalo-Colosseum @ https://youtu.be/5kIeUb5AE4s
# FILE NAME: main.py
# PROJECT NAME: python__tile_based_game
# DATE CREATED: 04/07/2021
# DATE LAST MODIFIED: 05/13/2021
# PYTHON VER. USED: 3.x

################### IMPORTS ####################
import pygame as pg
import random as r
from os import path

# Custom Imports
from settings import *
from sprites import *
from tilemap import *
################### FINISHED ###################

################ GLOBAL FUNCTIONS ##################
def drawPlayerHealth(surface, x, y, healthPercentage):
    """ To use: drawPlayerHealth(surface, x, y, healthPercentage)
    This function draws the player's health bar. """
    if healthPercentage < 0:
        healthPercentage = 0

    # Setting up the cosmetics: AKA What the Health Bar will look like!
    BAR_LENGTH = 100
    BAR_HEIGHT = 20

    fill = healthPercentage * BAR_LENGTH

    outlineRect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fillRect = pg.Rect(x, y, fill, BAR_HEIGHT)

    # Setting up the colors in the bar
    if healthPercentage > 0.6:
        color = GREEN
    elif healthPercentage > 0.3:
        color = YELLOW
    else:
        color = RED

    # Drawing the bar on the screen!
    pg.draw.rect(surface, color, fillRect)
    pg.draw.rect(surface, WHITE, outlineRect, 2)
##################### FINISHED #####################

################ MAIN GAME LOOP ################
####### Game class #######
class Game(object):
    """ To use: Game()
    This class runs the main game. """
    def __init__(self):
        self.running = True

        pg.init()  # Initializing Pygame Library
        pg.mixer.init()  # Sounds

        # Initializing display
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(title)

        # Initializing clock
        self.clock = pg.time.Clock()

        # Setting repeat variable
        pg.key.set_repeat(500, 100)

        self.loadData()

    def loadData(self):
        """ To use: self.loadData()
        This method creates data for maps. """
        # self.map = TextMap(path.join(textMapsFolder, "example_map2__large.txt"))

        # Setting up the map
        self.map = TiledMap(path.join(firstTiledMapFolder, "50x30__60px_tile_map__top_down_shooter.tmx"))
        self.mapImage = self.map.makeMap()
        self.mapRect = self.mapImage.get_rect()

        # Loading spritesheet image
        self.spritesheet = Spritesheet(path.join(spritesheetImgFolder, CHARACTERS_SPRITESHEET))

        # Loading individual player image
        self.playerImage = pg.image.load(path.join(manBlueImageFolder, PLAYER_IMAGE)).convert_alpha()

        # Loading the individual bullet image
        self.bulletImage = pg.image.load(path.join(pngImgFolder, BULLET_IMAGE)).convert_alpha()

        ## Loading individual zombie image
        self.zombieImage = pg.image.load(path.join(zombieImageFolder, ZOMBIE_IMAGE)).convert_alpha()

        # Loading individual wall tiles
        self.wallImage = pg.image.load(path.join(wallImageFolder, WALL_IMAGE)).convert_alpha()
        self.wallImage = pg.transform.scale(self.wallImage, (TILE_SIZE, TILE_SIZE))

        # Loading gun flashes
        self.gunFlashes = []
        for image in MUZZLE_FLASHES:
            self.gunFlashes.append(pg.image.load(path.join(pngImgFolder, image)).convert_alpha())

        # Loading item images
        self.itemImages = {}
        for item in ITEM_IMAGES:
            self.itemImages[item] = pg.image.load(path.join(itemsImageFolder, ITEM_IMAGES[item])).convert_alpha()

        ## Loading Sounds
        pg.mixer.music.load(path.join(musicFolder, BACKGROUND_MUSIC))
        pg.mixer.music.set_volume(0.21)

        self.effectsSounds = {}
        for type in EFFECTS_SOUNDS:
            s = pg.mixer.Sound(path.join(soundEffectsFolder, EFFECTS_SOUNDS[type]))
            s.set_volume(0.6)

            self.effectsSounds[type] = s

        self.weaponSounds = {}
        self.weaponSounds["gun"] = []
        for sound in WEAPON_SOUNDS_GUN:
            s = pg.mixer.Sound(path.join(soundEffectsFolder, sound))
            s.set_volume(0.5)

            self.weaponSounds["gun"].append(s)

        self.zombieMoanSounds = []
        for sound in ZOMBIE_MOAN_SOUNDS:
            s = pg.mixer.Sound(path.join(soundEffectsFolder, sound))
            s.set_volume(0.3)

            self.zombieMoanSounds.append(s)

        self.zombieHitSounds =  []
        for sound in ZOMBIE_HIT_SOUNDS:
            s = pg.mixer.Sound(path.join(soundEffectsFolder, sound))
            s.set_volume(0.8)

            self.zombieHitSounds.append(s)

        self.playerHitSounds = []
        for sound in PLAYER_HIT_SOUNDS:
            s = pg.mixer.Sound(path.join(playerSoundsFolder, sound))
            s.set_volume(2)

            self.playerHitSounds.append(s)

    def new(self):
        """ To use: self.new()
        This method creates a new game. """
        # Creating the sprite groups
        self.allSprites = pg.sprite.LayeredUpdates() # All sprites group

        self.playerGroup = pg.sprite.Group() # Player group

        self.bulletGroup = pg.sprite.Group() # Bullet group

        self.walls = pg.sprite.Group() # The Walls group

        self.zombieGroup = pg.sprite.Group() # The Zombie group

        self.itemsGroup = pg.sprite.Group() # The Item group

        ## Creating the game objects

        # Spawning walls and things in text map
        # for row, tiles in enumerate(self.map.data): # Where the "enumerate" uses both index number and list item
        #     for col, tile in enumerate(tiles):
        #         if tile == "1":
        #             Wall(self, col, row)
        #
        #         if tile == "Z":
        #             Zombie(self, col, row)
        #
        #         if tile == "P":
        #             self.player = Player(self, col, row)
        #
        #             # Adding player to sprite groups
        #             self.allSprites.add(self.player)
        #             self.playerGroup.add(self.player)

        for tileObject in self.map.tmxdata.objects:
            objectCenter = vec(tileObject.x + tileObject.width / 2, tileObject.y + tileObject.height / 2)
            # Spawning Player
            if tileObject.name == "Player":
                self.player = Player(self, objectCenter.x, objectCenter.y)

            # Spawning Zombie
            if tileObject.name == "Zombie":
                Zombie(self, objectCenter.x, objectCenter.y)

            # Creating Objects -- things that the player can collide with
            if tileObject.name == "Wall":
                Obstacle(self, tileObject.x, tileObject.y, tileObject.width, tileObject.height)

            if tileObject.name in ["health"]:
                Item(self, objectCenter, tileObject.name)

        # Spawning camera
        self.camera = Camera(self.map.width, self.map.height)

        self.drawDebug = False

        ## Playing sound effects
        self.effectsSounds["levelStart"].play()

        # Start running game loop...
        self.run()

    def run(self):
        """ To use: self.run()
        This method runs the game. """
        ## Game loop
        self.playing = True
        pg.mixer.music.play(loops = -1)

        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000

            # Processing input events
            self.events()

            # Processing updated variables
            self.update()

            # Creating the images on the screen
            self.draw()

    def events(self):
        """ To use: self.events()
        This method keeps track of the events that happen throughout running the game. """
        for event in pg.event.get():
            # Check for closing windows:
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.playing = False

                # Debugging variable change
                if event.key == pg.K_h:
                    self.drawDebug = not self.drawDebug

                # Movement events: .. --NOT NEEDED-- ..
                # if event.key == pg.K_LEFT:
                #     self.player.move(dx = -1)
                # if event.key == pg.K_RIGHT:
                #     self.player.move(dx = 1)
                # if event.key == pg.K_UP:
                #     self.player.move(dy = -1)
                # if event.key == pg.K_DOWN:
                #     self.player.move(dy = 1)

    def update(self):
        """ To use: self.update()
        This method updates what is shown on the HUD. """
        self.allSprites.update()
        self.camera.update(self.player)

        # When player hits item
        hits = pg.sprite.spritecollide(self.player, self.itemsGroup, False)

        for hit in hits:
            if hit.type == "health" and self.player.health < PLAYER_HEALTH:
                hit.kill()

                self.effectsSounds["healthUp"].play()

                self.player.addHealth(HEALTH_PACK_AMOUNT)

        # When zombies hit player
        hits = pg.sprite.spritecollide(self.player, self.zombieGroup, False, collideHitRect)

        for hit in hits:
            self.player.health -= ZOMBITE

            if r.random() < 0.7:
                r.choice(self.playerHitSounds).play()

            hit.velocity = vec(0, 0) # Stunning the player

            if self.player.health <= 0:
                self.playing = False
        if hits:
            self.player.position += vec(ZOMBITE_KNOCKBACK, 0).rotate(-hits[0].rotation)

        # When bullets hit zombies
        hits = pg.sprite.groupcollide(self.zombieGroup, self.bulletGroup, False, True)

        for hit in hits:
            hit.health -= BULLET_DAMAGE

            hit.velocity = vec(0, 0) # Stunning the Zombies when they get hit

    def drawGrid(self):
        """ To use: self.drawGrid()
        This method draws a grid on the screen. Useful for tile-based games. """
        for x in range(0, WIDTH, TILE_SIZE):
            pg.draw.line(self.screen, LIGHT_GREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILE_SIZE):
            pg.draw.line(self.screen, LIGHT_GREY, (0, y), (WIDTH, y))

    def draw(self):
        """ To use: self.draw()
        This method draws the content on the screen. """
        # pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        # self.screen.fill(BG_COLOR)

        self.screen.blit(self.mapImage, self.camera.applyRect(self.mapRect))

        ## Customizing the draw() method for a tile-based game: AKA Drawing a Grid on the Background
        # self.drawGrid()
        ## FIN

        for sprite in self.allSprites:
            if isinstance(sprite, Zombie): # If the sprite is an instance of the Zombie sprite, then do this:
                sprite.drawHealth()
            self.screen.blit(sprite.image, self.camera.apply(sprite))


            if self.drawDebug:
                pg.draw.rect(self.screen, MINT, self.camera.applyRect(sprite.hitRect), 1)

        if self.drawDebug:
            for wall in self.walls:
                pg.draw.rect(self.screen, MINT, self.camera.applyRect(wall.rect), 1)

        # Drawing the player health:
        drawPlayerHealth(self.screen, 10, 10, self.player.health / PLAYER_HEALTH)

        ## This is the very last thing to happen during the draw:
        pg.display.flip()

    def showStartingScreen(self):
        """ To use: self.showStartingScreen()
        This method shows the starting screen. """
        pass

    def showGameOverScreen(self):
        """ To use: self.showGameOverScreen()
        This method shows the game over screen. """
        pass

####### Finished #######

g = Game() # Defining the game start

g.showStartingScreen() # Showing the starting screen for the new game

while g.running:
    g.new() # This kicks off the actual game loop
    g.showGameOverScreen()

# If the loop ever breaks this happens:
pg.quit()
################### FINISHED ###################