import pygame as pg
from characters_file import Character
from constants_file import *
from sprites_file import FruitSprites

class Fruit(Character):
    def __init__(self, inter, niveau=0):
        Character.__init__(self, inter)
        self.sprites = None
        self.name = FRUIT
        self.color = LIME
        self.duration = 15
        self.timer = 0
        self.disappear = False
        self.points = 100 + niveau*20
        self.sprites = FruitSprites(self, niveau)

    def update(self, dt):
        self.timer += dt
        if self.timer >= self.duration:
            self.disappear = True
