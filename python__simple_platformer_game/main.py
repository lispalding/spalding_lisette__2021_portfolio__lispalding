# MADE BY: Lisette Spalding
# ART WORK CREDIT: "Kenney.nl" @ "www.kenney.nl"
# FILE NAME: main.py
# PROJECT NAME: python__simple_platformer_game
# DATE CREATED: 04/01/2021
# DATE LAST MODIFIED: 04/25/2021
# PYTHON VER. USED: 3.8

################### IMPORTS ####################
import pygame as pg
import random as r
from os import path

# Custom Imports
from settings import *
from sprites import *
################### FINISHED ###################

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
        pg.display.set_caption(TITLE)

        # Initializing clock
        self.clock = pg.time.Clock()

        # Finding the font on the system
        self.fontName = pg.font.match_font(FONT_NAME)

        # Loading the data
        self.loadData()

    def loadData(self):
        """ To use: self.loadData()
        This method loads the necessary files. """

        # Loading the highscore:
        with open(path.join(textDataFolder, HIGHSCORE_FILE), "r") as hScore:
            try:
                self.highscore = int(hScore.read())
            except:
                self.highscore = 0

        # Loading Images
        self.spritesheet = Spritesheet(path.join(spritesheetImageFolder, SPRITESHEET_FILE))

    def new(self):
        """ To use: self.new()
        This method creates a new game. """
        self.score = 0 # Setting the score to zero when starting a new game

        # Creating the sprite groups
        self.allSprites = pg.sprite.Group() # All sprites group
        self.playerGroup = pg.sprite.Group() # Player group
        self.platformsGroup = pg.sprite.Group() # Platform group

        ## Creating the game objects
        self.player = Player(self)
        # Adding player to sprite groups
        self.allSprites.add(self.player)
        self.playerGroup.add(self.player)

        # Spawning platforms
        for plat in PLATFORM_LIST:
            p = Platform(self, *plat)
            self.allSprites.add(p)
            self.platformsGroup.add(p)
        # Start running game loop...
        self.run()

    def run(self):
        """ To use: self.run()
        This method runs the game. """
        ## Game loop
        self.playing = True

        while self.playing:
            self.clock.tick(FPS)

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

                # Starting the checks for keys pressed that will affect the player movement
                if event.key == pg.K_SPACE:
                    self.player.jump()

    def update(self):
        """ To use: self.update()
        This method updates what is shown on the HUD. """
        self.allSprites.update()

        # Collision check between player and platforms -- ONLY if falling
        if self.player.velocity.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platformsGroup, False)
            if hits:
                self.player.position.y = hits[0].rect.top
                self.player.velocity.y = 0

        if self.player.rect.top <= HEIGHT / 4: # When player reaches the top 1/4 of the screen, do this:
            self.player.position.y += max(abs(self.player.velocity.y), 2) # Where abs() means Take The Absolute Value
            for plat in self.platformsGroup:
                plat.rect.y += max(abs(self.player.velocity.y), 2) # Where abs() means Take The Absolute Value
                if plat.rect.top >= HEIGHT: # If the platform goes below the bottom of the screen
                    plat.kill()
                    self.score += 10

        # For if we die / Fall off the screen:
        if self.player.rect.bottom > HEIGHT:
            for sprite in self.allSprites:
                sprite.rect.y -= max(self.player.velocity.y, 10)

                if sprite.rect.bottom < 0:
                    sprite.kill()

        if len(self.platformsGroup) == 0:
            self.playing = False
        # Die FIN

        # Spawning new platforms to replace the killed platforms - This will keep the same average number of platforms
        while len(self.platformsGroup) < 6:
            width = r.randrange(50, 100)
            p = Platform(self, r.randrange(0, WIDTH - width), r.randrange(-75, -30))

            self.allSprites.add(p)
            self.platformsGroup.add(p)

    def draw(self):
        """ To use: self.draw()
        This method draws the content on the screen. """
        self.screen.fill(BGCOLOR)

        self.allSprites.draw(self.screen)

        self.screen.blit(self.player.image, self.player.rect)

        self.drawText(str(self.score), 22, WHITE, WIDTH / 2, 15)

        ## This is the very last thing to happen during the draw:
        pg.display.flip()

    def showStartingScreen(self):
        """ To use: self.showStartingScreen()
        This method shows the starting screen. """
        self.screen.fill(BGCOLOR)
        self.drawText(TITLE, 35, WHITE, WIDTH / 2, HEIGHT / 4.2) # Drawing title on screen, located: center width-wise and top 1/4 of the screen

        # Instructional Text:
        self.drawText("Instructions:", 22, WHITE, WIDTH / 2, HEIGHT / 2.4)
        self.drawText("Left and right arrow keys to move, space bar to jump!", 18, WHITE, WIDTH / 2, HEIGHT / 2.1)
        self.drawText("Press any key to play!",  25, WHITE, WIDTH / 2, HEIGHT *  3 / 4)

        # Highscore Text:
        self.drawText("Current High Score: " + str(self.highscore), 22, WHITE, WIDTH / 2, HEIGHT / 2 + 40)

        pg.display.flip()
        self.waitForKey()

    def showGameOverScreen(self):
        """ To use: self.showGameOverScreen()
        This method shows the game over screen. """
        self.screen.fill(BGCOLOR)

        # Drawing Text
        self.drawText("GAME OVER :(", 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.drawText("Score: " + str(self.score), 30, WHITE, WIDTH / 2, HEIGHT / 2)
        self.drawText("Press any key to play again...", 25, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        # Drawing Text FIN

        # Checking to see if the score is higher than the current highscore; before drawing highscore text
        if self.score > self.highscore:
            self.highscore = self.score

            # Congratulating the player for getting a new highscore
            self.drawText("NEW HIGH SCORE!!", 22, WHITE, WIDTH / 2, HEIGHT / 2 + 40)

            # Writing the new highscore to file
            with open(path.join(textDataFolder, HIGHSCORE_FILE), "w") as newScore:
               newScore.write(str(self.score))
        else:
            self.drawText("Current High Score: " + str(self.highscore), 22, WHITE, WIDTH / 2, HEIGHT / 3)

        pg.display.flip()
        self.waitForKey()

    def waitForKey(self):
        """ To use: self.waitForKeyEvent()
        This method waits for a key to be pressed. """
        waiting = True
        while waiting:
            self.clock.tick(FPS)

            # Ways to end the loop:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False

                if event.type == pg.KEYUP:
                    if event.key == pg.K_ESCAPE:
                        waiting = False
                        self.running = False
                    if event.key != pg.K_ESCAPE:
                        # If you press any key while on this screen (Aside from ESC key), this action happens
                        waiting = False

    def drawText(self, text, size, color, x, y):
        """ To use: self.drawText(text, size, color, x, y)
        This method draws text on the screen. """
        font = pg.font.Font(self.fontName, size)
        textSurface = font.render(text, True, color)
        textRect = textSurface.get_rect()
        textRect.midtop = (x, y)
        self.screen.blit(textSurface, textRect)

####### Finished #######

g = Game() # Defining the game start

g.showStartingScreen() # Showing the starting screen for the new game

while g.running:
    g.new() # This kicks off the actual game loop

    # This if statement will keep the game from displaying the game over screen unless the game is running
    if g.running == True:
        g.showGameOverScreen()

# If the loop ever breaks this happens:
pg.quit()
################### FINISHED ###################