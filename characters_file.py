import pygame
from pygame.locals import *
from vector import Vector2
from constants_file import *
from random import randint


class Character(object):
    def __init__(self, inter):
        self.name = None
        self.directions = {UP: Vector2(0, -1), DOWN: Vector2(0, 1),
                           LEFT: Vector2(-1, 0), RIGHT: Vector2(1, 0), STOP: Vector2()}
        self.direction = STOP
        self.setSpeed(100)
        self.radius = 10
        self.collideRadius = 5
        self.visible = True
        self.disablePortal = False
        self.goal = None
        self.directionMethod = self.randomDirection
        self.setStartInter(inter)
        self.image = None

    def setStartInter(self, inter):
        self.inter = inter
        self.startInter = inter
        self.target = inter
        self.setPosition()

    def setPosition(self):
        self.pos = self.inter.pos.copy()

    def validDirection(self, direction):
        if direction is not STOP:
            if self.name in self.inter.access[direction]:
                if self.inter.neighbors[direction] is not None:
                    return True
        return False

    def getNewTarget(self, direction):
        if self.validDirection(direction):
            return self.inter.neighbors[direction]
        return self.inter

    def overshotTarget(self):
        if self.target is not None:
            vec1 = self.target.pos - self.inter.pos
            vec2 = self.pos - self.inter.pos
            inter2Target = vec1.magnitudeSquared()
            inter2Self = vec2.magnitudeSquared()
            return inter2Self >= inter2Target
        return False

    def reverseDirection(self):
        self.direction *= -1
        temp = self.inter
        self.inter = self.target
        self.target = temp

    def oppositeDirection(self, direction):
        if direction is not STOP:
            if direction == self.direction * -1:
                return True
        return False

    def setSpeed(self, speed):
        self.speed = speed * TILE_W / 25

    def render(self, screen):
        if self.visible:
            if self.image is not None:
                ajustement = Vector2(TILE_W, TILE_H) / 2
                p = self.pos - ajustement
                screen.blit(self.image, p.asTuple())
            else:
                p = self.pos.asInt()
                pygame.draw.circle(screen, self.color, p, self.radius)

    def validDirections(self):
        directions = []
        for key in [UP, DOWN, LEFT, RIGHT]:
            if self.validDirection(key):
                if key != self.direction * -1:
                    directions.append(key)
        if len(directions) == 0:
            directions.append(self.direction * -1)
        return directions

    def randomDirection(self, directions):
        return directions[randint(0, len(directions)-1)]

    def goalDirection(self, directions):
        distances = []
        for direction in directions:
            vec = self.inter.pos + self.directions[direction] * TILE_W - self.goal
            distances.append(vec.magnitudeSquared())
        index = distances.index(min(distances))
        return directions[index]

    def reset(self):
        self.setStartInter(self.startInter)
        self.direction = STOP
        self.speed = 100
        self.visible = True


    def update(self, dt):
        self.pos += self.directions[self.direction]*self.speed*dt

        if self.overshotTarget():
            self.inter = self.target
            directions = self.validDirections()
            direction = self.directionMethod(directions)
            if not self.disablePortal:
                if self.inter.neighbors[PORTAL] is not None:
                    self.inter = self.inter.neighbors[PORTAL]
            self.target = self.getNewTarget(direction)
            if self.target is not self.inter:
                self.direction = direction
            else:
                self.target = self.getNewTarget(self.direction)

            self.setPosition()
