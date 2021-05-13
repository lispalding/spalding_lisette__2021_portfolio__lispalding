# MADE BY: Lisette Spalding
# ART WORK CREDIT: "Kenney.nl" @ "www.kenney.nl"
# BACKGROUND MUSIC CREDIT: DIVELA
# SONG TITLE & YOUTUBE LINK: Vocalo-Colosseum @ https://youtu.be/5kIeUb5AE4s
# FILE NAME: tilemap.py
# PROJECT NAME: python__tile_based_game
# DATE CREATED: 04/13/2021
# DATE LAST MODIFIED: 05/13/2021
# PYTHON VER. USED: 3.x

################### IMPORTS ####################
import pygame as pg
import random as r
from os import path
import pytmx

# Custom imports
from settings import *
################### FINISHED ###################

# Move this later:
def collideHitRect(spriteOne, spriteTwo):
    return spriteOne.hitRect.colliderect(spriteTwo.rect)
# Move FIN

class TextMap:
    """ To use: Map()
     This is the map class, it will load the maps necessary for the game. """
    def __init__(self, filename):
        self.data = []

        with open(filename, "rt") as f:
            for line in f:
                self.data.append(line.strip())

        # Obtaining the tile width & height
        self.tileWidth = len(self.data[0])
        self.tileHeight = len(self.data)

        # Obtaining the general width & height
        self.width = self.tileWidth * TILE_SIZE
        self.height = self.tileHeight * TILE_SIZE

class TiledMap:
    """ To use: TiledMap()
    This class reads a Tiled map (A map built using the 'Tiled' application. """
    def __init__(self, filename):
        tm =  pytmx.load_pygame(filename, pixelalpha = True) # This is loading the file

        # Creating the map width and height:
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight

        self.tmxdata = tm

    def render(self, surface):
        """ To use: self.render(surface)
        This method renders the tiles in the map. """
        ti = self.tmxdata.get_tile_image_by_gid

        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid, in layer:
                    tile = ti(gid)
                    if tile:
                        surface.blit(tile, (x * self.tmxdata.tilewidth, y * self.tmxdata.tileheight))

    def makeMap(self):
        """ To use: self.makeMap()
        This method creates a temporary surface and creates the map. """
        tempSurface = pg.Surface((self.width, self.height))

        self.render(tempSurface)
        return tempSurface

class Camera:
    """ To use: Camera()
    This is the Camera class, which will bind the metaphorical camera to the player. """
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)

        self.width = width
        self.height = height

    def apply(self, entity):
        """ To use: self.apply(entity)
        This method that keeps the entity that the camera is bound to in the center of the screen. """
        return entity.rect.move(self.camera.topleft)

    def applyRect(self, rect):
        return rect.move(self.camera.topleft)

    def update(self, target):
        """ To use: self.update(target)
        This is the method that keeps the map/camera updated as the player moves. """
        x = -target.rect.centerx + int(WIDTH / 2)
        y = -target.rect.centery + int(HEIGHT / 2)

        # Limiting scrolling to map size
        x = min(0, x) # Left limit
        y = min(0, y) # Top limit
        x = max(-(self.width - WIDTH), x) # Right limit
        y = max(-(self.height - HEIGHT), y) # Bottom limit

        # Adjusting the camera rectangle
        self.camera = pg.Rect(x, y, self.width, self.height)