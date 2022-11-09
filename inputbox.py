import pygame, pygame.font, pygame.event, pygame.draw, string
from pygame.locals import *

def get_key():
  while 1:
    event = pygame.event.poll()
    if event.type == KEYDOWN:
      return event.key
    else:
      pass

def display_box(screen, message):
  "Print a message in a box in the middle of the screen"
  fontobject = pygame.font.Font(None, 25)
  bg = pygame.Surface((2000, 1100))
  bg.set_alpha(128)
  bg.fill((255, 255, 255))
  screen.blit(bg, (0, 0))
  pygame.draw.rect(screen, (0, 0, 0),
                   ((screen.get_width() / 2) - 225,
                    (screen.get_height() / 2) - 28,
                    500, 30), 0)
  pygame.draw.rect(screen, (255, 255, 255),
                   ((screen.get_width() / 2) - 227,
                    (screen.get_height() / 2) - 30,
                    504, 34), 1)
  if len(message) != 0:
    screen.blit(fontobject.render(message, True, (255, 255, 255)),
                ((screen.get_width() / 2) - 223, (screen.get_height() / 2) - 22))
  pygame.display.flip()

def ask(screen, question):
  pygame.font.init()
  current_string = []
  display_box(screen, question + " " + "".join(current_string))
  while 1:
    inkey = get_key()
    if inkey == K_BACKSPACE:
      current_string = current_string[0:-1]
    elif inkey == K_RETURN:
      break
    elif inkey == K_MINUS:
      current_string.append("_")
    elif inkey <= 127:
      current_string.append(chr(inkey))
    display_box(screen, question + " " + "".join(current_string))
  return "".join(current_string)

def main():
  screen = pygame.display.set_mode((320,240))
  print(ask(screen, "Name") + " was entered")

if __name__ == '__main__': main()