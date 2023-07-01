import pygame as pg
from pygame.locals import *
from pygame import mixer
from constants_file import *
from player_file import Player
from intersections_file import InterGroup
from nonosses_file import NonosseGroup
from enemies_file import EnemyGroup
from walls_file import WallGroup
from fruit_file import Fruit
from pause_file import Pause
from sprites_file import MazeSprites
from sprites_file import VieSprites
from sprites_file import Spritesheet
from modes_file import ModeController
import inputbox
import name
import sys
import math

class Game(object):
    def __init__(self):
        pg.init()
        pg.joystick.init()
        mixer.init()
        # self.joystick = pg.joystick.Joystick(0)
        self.screen = pg.display.set_mode(SCREEN, 0, 32)
        self.background = None
        self.clock = pg.time.Clock()
        self.running = True
        self.score = 0
        self.font_name = pg.font.match_font(FONT_NAME)
        self.fruit = None
        self.vies = 3
        self.level = 0
        self.pause = Pause(True)
        self.vieSprites = VieSprites(self.vies)
        self.fruitsAttrapes = []
        self.intro = True
        self.scoreBoard = False
        # with open('score.txt', 'r+') as f:
        #     self.highscore = f.read()
        # print(self.highscore)
        self.eatSound = mixer.Sound("eat.mp3")
        self.selectSound = mixer.Sound("select.mp3")
        self.powerUpSound = mixer.Sound("woof.mp3")
        self.victorySound = mixer.Sound("victory.mp3")
        self.deathSound = mixer.Sound("death.mp3")
        self.gameMusic = mixer.Sound("musiqueJeu.mp3")
        self.menuMusic = mixer.Sound("musiqueMenu.mp3")
        self.titreY = SCREEN_W / 4
        self.bienvenueY = SCREEN_W / 6
        self.x = 0
        self.spritesheet = Spritesheet()
        self.charlieMenuImg = pg.image.load('CharlieMenu.png')
        self.charlieMenuImg_x = -150
        self.charlieMenuImg_y = 600
        self.charlieMenuImg_vit = 10

        self.marcMenuImg = pg.image.load('MarcMenu.png')
        self.marcMenuImg_x = -350
        self.marcMenuImg_y = 600
        self.marcMenuImg_vit = 10

        self.claireMenuImg = pg.image.load('ClaireMenu.png')
        self.claireMenuImg_x = -500
        self.claireMenuImg_y = 600
        self.claireMenuImg_vit = 10

        self.aliceMenuImg = pg.image.load('AliceMenu.png')
        self.aliceMenuImg_x = -650
        self.aliceMenuImg_y = 600
        self.aliceMenuImg_vit = 10

        self.mathisMenuImg = pg.image.load('MathisMenu.png')
        self.mathisMenuImg_x = -800
        self.mathisMenuImg_y = 600
        self.mathisMenuImg_vit = 10

    def setBackground(self):
        self.background = pg.surface.Surface(SCREEN).convert()
        self.background.fill(GRASS_GREEN)

    def startGame(self):
        self.setBackground()
        self.inters = InterGroup("maze1.txt")
        self.nonosses = NonosseGroup("maze1.txt")
        self.walls = WallGroup("maze1.txt")
        self.inters.setPortalPair((18, 17), (46, 17))
        self.player = Player(self.inters.getInterFromTiles(32, 20))
        self.enemies = EnemyGroup(self.inters.getStartTempInter(), self.player)
        self.enemies.enemy1.setStartInter(self.inters.getInterFromTiles(32, 14))
        self.enemies.enemy2.setStartInter(self.inters.getInterFromTiles(32, 17))
        self.enemies.enemy3.setStartInter(self.inters.getInterFromTiles(30, 17))
        self.enemies.enemy4.setStartInter(self.inters.getInterFromTiles(34, 17))
        self.enemies.setSpawnInter(self.inters.getInterFromTiles(32, 17))

        self.inters.denyHomeAccess(self.player)
        self.inters.denyHomeAccessList(self.enemies)
        self.inters.denyAccessList(32, 17, LEFT, self.enemies)
        self.inters.denyAccessList(32, 17, RIGHT, self.enemies)
        self.enemies.enemy3.startInter.denyAccess(RIGHT, self.enemies.enemy3)
        self.enemies.enemy4.startInter.denyAccess(LEFT, self.enemies.enemy4)
        self.mazesprites = MazeSprites("maze1.txt", "maze1_rotation.txt")
        self.background = self.mazesprites.constructBackground(self.background, self.level % 5)
        self.gameMusic.set_volume(0.0)
        self.gameMusic.play(loops=-1)
        self.menuMusic.set_volume(0.1)
        self.menuMusic.play(loops=-1)

    def restartGame(self):
        self.vies = 3
        self.level = 0
        # if self.score > int(self.highscore):
        #     with open('score.txt', 'w') as f:
        #         f.write(str(self.score))
        # self.highscore = self.score
        self.updateScoreBoard()
        self.score = 0
        self.enemies.resetSpeed()
        self.pause.paused = True
        self.fruit = None
        self.startGame()
        self.vieSprites.reinitVies(self.vies)
        self.fruitsAttrapes = []

    def resetLevel(self):
        self.pause.paused = True
        # with open('score.txt', 'r+') as f:
        #     self.highscore = f.read()
        self.player.reset()
        self.enemies.reset()
        self.fruit = None

    def update(self):
        dt = self.clock.tick(30) / 1000.0
        self.nonosses.update(dt)
        if not self.pause.paused:
            self.player.update(dt)
            self.enemies.update(dt)
            if self.fruit is not None:
                self.fruit.update(dt)
            self.checkNonosseEvents()
            self.checkEnemiesEvents()
            self.checkFruitEvents()
        postPauseMethod = self.pause.update(dt)
        if postPauseMethod is not None:
            postPauseMethod()
        self.checkEvents()
        self.render()

    def checkEvents(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()

            # if event.type == pg.JOYBUTTONDOWN:
            #     if event.button == 0:
            #         if self.player.alive:
            #             self.pause.setPause(playerPaused=True)
            #             if not self.pause.paused:
            #                 self.showCharacters()
            #             else:
            #                 self.hideCharacters()
            #         if self.intro == True:
            #             mixer.Sound.play(self.selectSound)
            #             self.intro = False
            #
            #     if event.button == 6:
            #         mixer.Sound.play(self.selectSound)
            #         self.scoreBoard = not self.scoreBoard
            #         if not self.pause.paused:
            #             self.pause.switch()
            #
            #     if event.button == 5:
            #         self.running = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.running = False
                if event.key == pg.K_SPACE:
                    if self.player.alive:
                        self.pause.setPause(playerPaused=True)
                        if not self.pause.paused:
                            self.showCharacters()
                        else:
                            self.hideCharacters()
                    if self.intro == True:
                        self.intro = False

                if event.key == pg.K_s:
                    self.scoreBoard = not self.scoreBoard
                    if not self.pause.paused:
                        self.pause.switch()

    def checkNonosseEvents(self):
        nonosse = self.player.eatNonosses(self.nonosses.nonosseList)
        if nonosse:
            mixer.Sound.play(self.eatSound)
            self.nonosses.numEaten += 1
            self.score += 10
            self.nonosses.nonosseList.remove(nonosse)
            if nonosse.name == S_NONOSSE:
                mixer.Sound.play(self.powerUpSound)
                self.enemies.startFreight()
            if self.nonosses.numEaten == 30:
                self.enemies.enemy3.startInter.allowAccess(RIGHT, self.enemies.enemy3)
            if self.nonosses.numEaten == 60:
                self.enemies.enemy4.startInter.allowAccess(LEFT, self.enemies.enemy4)
            if self.nonosses.isEmpty():
                self.hideCharacters()
                self.gameMusic.stop()
                mixer.Sound.play(self.victorySound)
                self.pause.setPause(pauseTime=5, func=self.nextLevel)

    def checkEnemiesEvents(self):
        for enemy in self.enemies:
            if self.player.collideEnemy(enemy):
                if enemy.mode.current is FREIGHT:
                    self.player.visible = False
                    enemy.visible = False
                    self.pause.setPause(pauseTime=1, func=self.showCharacters)
                    enemy.startSpawn()
                    self.inters.allowHomeAccess(enemy)
                    self.score += enemy.points
                elif enemy.mode.current is not SPAWN:
                    if self.player.alive:
                        mixer.Sound.play(self.deathSound)
                        self.vies -= 1
                        self.vieSprites.retirerImage()
                        self.player.die()
                        self.enemies.hide()
                        self.fruit = None
                        if self.vies <= 0:
                            self.pause.setPause(pauseTime=3, func=self.restartGame)
                        else:
                            self.pause.setPause(pauseTime=3, func=self.resetLevel)

    def checkFruitEvents(self):
        if self.nonosses.numEaten == 50 or self.nonosses.numEaten == 100:
            if self.fruit is None:
                self.fruit = Fruit(self.inters.getInterFromTiles(32, 20), self.level)
        if self.fruit is not None:
            if self.player.collideCheck(self.fruit):
                self.score += self.fruit.points
                self.fruitsAttrapes.append(self.fruit.image)
                self.fruit = None
            elif self.fruit.disappear:
                self.fruit = None

    def nextLevel(self):
        self.showCharacters()
        self.level += 1
        self.pause.paused = True
        self.startGame()
        self.enemies.increaseSpeed()

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def showCharacters(self):
        self.player.visible = True
        self.enemies.show()

    def hideCharacters(self):
        self.player.visible = False
        self.enemies.hide()

    def render(self):
        self.screen.blit(self.background, (0, 0))
        self.inters.render(self.screen)
        self.nonosses.render(self.screen)
        self.walls.render(self.screen)
        self.player.render(self.screen)
        self.enemies.render(self.screen)
        if self.fruit is not None:
            self.fruit.render(self.screen)
        self.draw_text("SCORE : ", 40, WHITE, 100, 30)
        self.draw_text(str(self.score), 40, WHITE, 210, 30)
        for i in range(len(self.vieSprites.images)):
            x = (self.vieSprites.images[i].get_width() * i) + 50
            y = (SCREEN_H - self.vieSprites.images[i].get_height()) - 50
            self.screen.blit(self.vieSprites.images[i], (x, y))

        for i in range(len(self.fruitsAttrapes)):
            x = SCREEN_W - self.fruitsAttrapes[i].get_width() * (i+1) - 50
            y = SCREEN_H - self.fruitsAttrapes[i].get_height() - 50
            self.screen.blit(self.fruitsAttrapes[i], (x, y))

        if self.vies <= 0:
            self.draw_text("GAME OVER !", 60, WHITE, SCREEN_W/2 + 25, SCREEN_H/2 - 100)

        if self.intro:
            self.menuMusic.set_volume(0.1)
            self.gameMusic.set_volume(0.0)
            self.drawTitleScreen()
        else:
            self.menuMusic.set_volume(0.0)
            self.gameMusic.set_volume(0.1)


        if self.scoreBoard:
            self.menuMusic.set_volume(0.1)
            self.gameMusic.set_volume(0.0)
            self.drawScoreBoard()

        if self.nonosses.isEmpty():
            self.draw_text("Bravo ! Vous passez au niveau " + str(self.level + 2) + " !", 60, WHITE, SCREEN_W/2 + 25, SCREEN_H/2 - 100)

        pg.display.update()

    def updateScoreBoard(self):
        with open("score.txt", "r+") as s:
            scores = s.readlines()
        with open("noms.txt", "r+") as n:
            noms = n.readlines()

        if self.score > int(scores[9]):
            for i in range(len(scores)):
                if self.score > int(scores[i]):
                    del scores[-1]
                    scores.insert(i, str(self.score) + "\n")
                    del noms[-1]
                    nom_entre = name.ask(self.screen)
                    # nom_entre = inputbox.ask(self.screen, "Question")
                    noms.insert(i, nom_entre + "\n")
                    self.scoreBoard = True
                    break

            with open("score.txt", "w") as f:
                f.writelines(scores)
            with open("noms.txt", "w") as f:
                f.writelines(noms)

    def drawTitleScreen(self):
        pg.draw.rect(self.screen, GRASS_GREEN, (0, 0, SCREEN_W, SCREEN_H))
        self.titreY = SCREEN_H / 4 + 40 * math.sin(self.x)
        self.bienvenueY = SCREEN_H / 6 + 40 * math.sin(self.x)
        self.x -= 0.05
        self.draw_text("Bienvenue dans", 60, WHITE, SCREEN_W / 2 + 25, self.bienvenueY)
        self.draw_text("PAC-CHARLIE", 150, BLACK, SCREEN_W / 2 + 20, self.titreY + 20)
        self.draw_text("PAC-CHARLIE", 150, WHITE, SCREEN_W / 2, self.titreY)
        self.draw_text("Appuyez sur le bouton X pour commencer", 20, WHITE, SCREEN_W / 2 + 25, SCREEN_H - 400)
        self.draw_text("Programmation : Mathis Mahaux - Dessins : Alice Musette", 20, (150, 150, 150), SCREEN_W / 2 + 25, SCREEN_H - 100)
        if self.charlieMenuImg_x < -800:
            self.charlieMenuImg = pg.transform.flip(self.charlieMenuImg, True, False)
            self.charlieMenuImg_vit = 10
        if self.charlieMenuImg_x > SCREEN_W + 800:
            self.charlieMenuImg = pg.transform.flip(self.charlieMenuImg, True, False)
            self.charlieMenuImg_vit = -10
        self.charlieMenuImg_x += self.charlieMenuImg_vit
        self.screen.blit(self.charlieMenuImg, (self.charlieMenuImg_x, self.charlieMenuImg_y))

        if self.marcMenuImg_x < -800:
            self.marcMenuImg = pg.transform.flip(self.marcMenuImg, True, False)
            self.marcMenuImg_vit = 10
        if self.marcMenuImg_x > SCREEN_W + 800:
            self.marcMenuImg = pg.transform.flip(self.marcMenuImg, True, False)
            self.marcMenuImg_vit = -10
        self.marcMenuImg_x += self.marcMenuImg_vit
        self.screen.blit(self.marcMenuImg, (self.marcMenuImg_x, self.marcMenuImg_y))

        if self.claireMenuImg_x < -800:
            self.claireMenuImg = pg.transform.flip(self.claireMenuImg, True, False)
            self.claireMenuImg_vit = 10
        if self.claireMenuImg_x > SCREEN_W + 800:
            self.claireMenuImg = pg.transform.flip(self.claireMenuImg, True, False)
            self.claireMenuImg_vit = -10
        self.claireMenuImg_x += self.claireMenuImg_vit
        self.screen.blit(self.claireMenuImg, (self.claireMenuImg_x, self.claireMenuImg_y))

        if self.aliceMenuImg_x < -800:
            self.aliceMenuImg = pg.transform.flip(self.aliceMenuImg, True, False)
            self.aliceMenuImg_vit = 10
        if self.aliceMenuImg_x > SCREEN_W + 800:
            self.aliceMenuImg = pg.transform.flip(self.aliceMenuImg, True, False)
            self.aliceMenuImg_vit = -10
        self.aliceMenuImg_x += self.aliceMenuImg_vit
        self.screen.blit(self.aliceMenuImg, (self.aliceMenuImg_x, self.aliceMenuImg_y))

        if self.mathisMenuImg_x < -800:
            self.mathisMenuImg = pg.transform.flip(self.mathisMenuImg, True, False)
            self.mathisMenuImg_vit = 10
        if self.mathisMenuImg_x > SCREEN_W + 800:
            self.mathisMenuImg = pg.transform.flip(self.mathisMenuImg, True, False)
            self.mathisMenuImg_vit = -10
        self.mathisMenuImg_x += self.mathisMenuImg_vit
        self.screen.blit(self.mathisMenuImg, (self.mathisMenuImg_x, self.mathisMenuImg_y))

    def drawScoreBoard(self):
        pg.draw.rect(self.screen, GRASS_GREEN, (0, 0, SCREEN_W, SCREEN_H))
        self.draw_text("LES 10 MEILLEURS SCORES : ", 60, WHITE,
                       SCREEN_W / 2 + 25, 50)

        with open("score.txt", "r+") as s:
            scores = s.readlines()
        with open("noms.txt", "r+") as n:
            noms = n.readlines()

        for i in range(len(scores)):
            self.draw_text(" ".join([str(i + 1), ":", str(scores[i].rstrip('\n')), "par", str(noms[i].rstrip('\n'))]),
                           50, (200, 200, 200), SCREEN_W / 2 + 25, (i + 3) * 60)

if __name__ == "__main__":
    game = Game()
    game.startGame()
    while game.running:
        game.update()
