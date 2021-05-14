# MADE BY: Lisette Spalding
# ART WORK CREDIT: "Kenney.nl" @ "www.kenney.nl"
# BACKGROUND MUSIC CREDIT (1): Snabisch
# SONG TITLE & OPEN GAME ART LINK (1): YIPPEE @ https://opengameart.org/content/yippee-0
# BACKGROUND MUSIC CREDIT (1): syncopika
# SONG TITLE & OPEN GAME ART LINK (1): happy tune @ https://opengameart.org/content/happy-tune
# FILE NAME: settings.py
# PROJECT NAME: python__simple_platformer_game
# DATE CREATED: 04/01/2021
# DATE LAST MODIFIED: 04/25/2021
# PYTHON VER. USED: 3.8

################### IMPORTS ####################
import pygame as pg
import random as r
from os import path
################### FINISHED ###################

################## VARIABLES ###################
WIDTH = 480
HEIGHT = 600
FPS = 60

FONT_NAME = "arial"

# Player Properties
PLAYER_ACCELERATION = 0.5
PLAYER_FRICTION = -0.12

PLAYER_GRAVITY = 0.8

PLAYER_JUMP = 23

PLAYER_WIDTH = 25
PLAYER_HEIGHT = 50

# Title
TITLE = "Jumpy Platformer - Python"
################### FINISHED ###################

################## PLATFORMS ###################
# Starting Platforms:
PLATFORM_LIST = [(0, HEIGHT - 60),
                 (WIDTH / 2 - 50, HEIGHT * 3 / 4),
                 (350, 200),
                 (175, 100)]

################### FINISHED ###################

################# FOLDER SETUP #################
gameFolder = path.dirname(__file__) # General folder set-up

# Basic image folders
imageFolder = path.join(gameFolder, "images")
spritesheetImageFolder = path.join(imageFolder, "Spritesheets")

# Basic sound folder
soundFolder = path.join(gameFolder, "sounds")

# Basic text data folder
textDataFolder = path.join(gameFolder, "text_data")

############ FOLDER CONSTANTS ############
HIGHSCORE_FILE = "highscore.txt"
SPRITESHEET_FILE = "spritesheet_jumper.png"

MUSIC_SELECTION = ["happy_tune.ogg", "YIPPEE.ogg"]
JUMPING_SOUNDS = ["Jump33.wav", "Jump40.wav"]
########## FOLDER CONSTANTS FIN ##########
################### FINISHED ###################

############### COLORS  (R. G. B) ##############
BGCOLOR = (0, 155, 155) # Background Color

BLACK = (0,0,0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Custom Colors
ORANGE = (242, 162, 41)
YELLOW_GREEN = (182, 219, 18)
MINT = (63, 232, 159)
PURPLE = (182, 103, 224)
PINK = (224, 103, 139)
LIGHT_BLUE = (100, 162, 209)
YELLOW = (245, 233, 154)
################### FINISHED ###################