import pygame as pg
from constants_file import *
import numpy as np

BASETILEWIDTH = 16
BASETILEHEIGHT = 16

class Spritesheet(object):
    def __init__(self):
        self.sheet = pg.image.load("C:\\Users\Sam\PycharmProjects\Charlie\spritesheet.png").convert_alpha()
        transcolor = self.sheet.get_at((0, 0))
        self.sheet.set_colorkey(transcolor)
        width = int(self.sheet.get_width() / BASETILEWIDTH * TILE_W)
        height = int(self.sheet.get_height() / BASETILEHEIGHT * TILE_H)
        self.sheet = pg.transform.scale(self.sheet, (width, height))

    def getImage(self, x, y, width, height):
        x *= TILE_W
        y *= TILE_H
        self.sheet.set_clip(pg.Rect(x, y, width, height))
        return self.sheet.subsurface(self.sheet.get_clip())


class CharlieSprites(Spritesheet):
    def __init__(self, character):
        Spritesheet.__init__(self)
        self.character = character
        self.character.image = self.getStartImage()

    def getStartImage(self):
        return self.getImage(8, 0)

    def getImage(self, x, y):
        return Spritesheet.getImage(self, x, y, 2*TILE_W, 2*TILE_H)

    def update(self):
        if self.character.direction == UP:
            self.character.image = self.getImage(6, 0)
        if self.character.direction == DOWN:
            self.character.image = self.getImage(4, 0)
        if self.character.direction == RIGHT:
            self.character.image = self.getImage(2, 0)
        if self.character.direction == LEFT:
            self.character.image = self.getImage(0, 0)

class EnemySprites(Spritesheet):
    def __init__(self, character):
        Spritesheet.__init__(self)
        self.x = {ENEMY1: 0, ENEMY2: 2, ENEMY3: 4, ENEMY4: 6}
        self.character = character
        self.character.image = self.getStartImage()

    def getStartImage(self):
        return self.getImage(self.x[self.character.name], 6)

    def getImage(self, x, y):
        return Spritesheet.getImage(self, x, y, 2 * TILE_W, 2 * TILE_H)

    def update(self):
        x = self.x[self.character.name]
        if self.character.direction == UP:
            self.character.image = self.getImage(x, 4)
        if self.character.direction == DOWN:
            self.character.image = self.getImage(x, 6)
        if self.character.direction == RIGHT:
            self.character.image = self.getImage(x, 10)
        if self.character.direction == LEFT:
            self.character.image = self.getImage(x, 8)

class FruitSprites(Spritesheet):
    def __init__(self, character, niveau):
        Spritesheet.__init__(self)
        self.character = character
        self.fruits = {0: (8, 4), 1: (8, 6), 2: (8, 8)}
        self.character.image = self.getStartImage(niveau % len(self.fruits))

    def getStartImage(self, cle):
        return self.getImage(*self.fruits[cle])

    def getImage(self, x, y):
        return Spritesheet.getImage(self, x, y, 2*TILE_W, 2*TILE_H)

class MazeSprites(Spritesheet):
    def __init__(self, mazefile, rotfile):
        Spritesheet.__init__(self)
        self.data = self.readMazeFile(mazefile)
        self.rotdata = self.readMazeFile(rotfile)

    def getImage(self, x, y):
        return Spritesheet.getImage(self, x, y, TILE_W, TILE_H)

    def readMazeFile(self, mazefile):
        return np.loadtxt(mazefile, dtype='<U1')

    def constructBackground(self, background, y):
        for row in list(range(self.data.shape[0])):
            for col in list(range(self.data.shape[1])):
                if self.data[row][col].isdigit():
                    x = int(self.data[row][col]) + 12
                    sprite = self.getImage(x, y)
                    rotval = int(self.rotdata[row][col])
                    sprite = self.rotate(sprite, rotval)
                    background.blit(sprite, (col * TILE_W, row * TILE_H))
                elif self.data[row][col] == '=':
                    sprite = self.getImage(10, 8)
                    background.blit(sprite, (col * TILE_W, row * TILE_H))
        return background

    def rotate(self, sprite, value):
        return pg.transform.rotate(sprite, value * 90)

class VieSprites(Spritesheet):
    def __init__(self, vies):
        Spritesheet.__init__(self)
        self.reinitVies(vies)

    def retirerImage(self):
        if len(self.images) > 0:
            self.images.pop(0)

    def reinitVies(self, vies):
        self.images = []
        for i in range(vies):
            self.images.append(self.getImage(4, 0))

    def getImage(self, x, y):
        return Spritesheet.getImage(self, x, y, 2*TILE_W, 2*TILE_H)

