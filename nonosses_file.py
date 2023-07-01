import pygame as pg
from vector import Vector2
from constants_file import *
import numpy as np


class Nonosse(object):
    def __init__(self, row, column):
        self.name = NONOSSE
        self.pos = Vector2(column * TILE_W, row * TILE_H)
        self.color = WHITE
        self.radius = int(2 * TILE_W / 16)
        self.collideRadius = int(2 * TILE_W / 16)
        self.points = 10
        self.visible = True
        self.image = pg.image.load("C:\\Users\Sam\PycharmProjects\Charlie\croquette.png")

    def render(self, screen):
        if self.visible:
            #ajustement = Vector2(TILE_W, TILE_H) / 2
            #p = self.pos + ajustement
            screen.blit(self.image, self.pos.asTuple())


class SuperNonosse(Nonosse):
    def __init__(self, row, column):
        Nonosse.__init__(self, row, column)
        self.name = S_NONOSSE
        self.radius = int(8 * TILE_W / 16)
        self.points = 50
        self.flashTime = 0.1
        self.timer = 0
        self.image = pg.image.load("C:\\Users\Sam\PycharmProjects\Charlie\os.png").convert_alpha()
        self.image.set_colorkey(BLACK)


    def update(self, dt):
        self.timer += dt
        if self.timer >= self.flashTime:
            self.visible = not self.visible
            self.timer = 0


class NonosseGroup(object):
    def __init__(self, nonossefile):
        self.nonosseList = []
        self.all_supernonosses = []
        self.createNonosseList(nonossefile)
        self.numEaten = 0

    def update(self, dt):
        for powerpellet in self.all_supernonosses:
            powerpellet.update(dt)

    def createNonosseList(self, nonossefile):
        data = self.readNonossefile(nonossefile)
        for row in range(data.shape[0]):
            for col in range(data.shape[1]):
                if data[row][col] in ['.', '+']:
                    self.nonosseList.append(Nonosse(row, col))
                elif data[row][col] in ['P', 'p']:
                    pp = SuperNonosse(row, col)
                    self.nonosseList.append(pp)
                    self.all_supernonosses.append(pp)

    def readNonossefile(self, textfile):
        return np.loadtxt(textfile, dtype='<U1')

    def isEmpty(self):
        if len(self.nonosseList) == 0:
            return True
        return False

    def render(self, screen):
        for nonosse in self.nonosseList:
            nonosse.render(screen)
