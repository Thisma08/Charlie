import pygame
from constants_file import *

def ask(ecran):
    bg = pygame.Surface((2000, 1100))
    bg.set_alpha(128)
    bg.fill((0, 0, 0))
    ecran.blit(bg, (0, 0))

    inputbox_border_surf = pygame.Surface((270, 120))
    inputbox_border_surf.fill(WHITE)
    inputbox_border_rect = inputbox_border_surf.get_rect()
    inputbox_border_rect.center = (SCREEN_W // 2, SCREEN_H // 2)
    ecran.blit(inputbox_border_surf, inputbox_border_rect)

    inputbox_surf = pygame.Surface((250, 100))
    inputbox_rect = inputbox_surf.get_rect()
    inputbox_rect.center = (SCREEN_W // 2, SCREEN_H // 2)
    ecran.blit(inputbox_surf, inputbox_rect)

    font = pygame.font.Font(pygame.font.match_font(FONT_NAME), 80)

    lettres = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U",
               "V", "W", "X", "Y", "Z"]
    i1 = 0
    i2 = 0
    i3 = 0

    lettre1 = lettres[i1]
    lettre2 = lettres[i2]
    lettre3 = lettres[i3]

    lettre_mod = 1

    message_a = font.render("Joli score ! Quel est votre nom ?", False, WHITE)
    message_rect = message_a.get_rect()
    message_rect.center = (SCREEN_W // 2, SCREEN_H // 3)
    ecran.blit(message_a, message_rect)

    lettre1_a = font.render(lettre1, False, WHITE)
    lettre1_rect = lettre1_a.get_rect()
    lettre1_rect.center = (SCREEN_W // 2 - 80, SCREEN_H // 2)
    ecran.blit(lettre1_a, lettre1_rect)

    lettre2_a = font.render(lettre2, False, WHITE)
    lettre2_rect = lettre2_a.get_rect()
    lettre2_rect.center = (SCREEN_W // 2, SCREEN_H // 2)
    ecran.blit(lettre2_a, lettre2_rect)

    lettre3_a = font.render(lettre3, False, WHITE)
    lettre3_rect = lettre3_a.get_rect()
    lettre3_rect.center = (SCREEN_W // 2 + 80, SCREEN_H // 2)
    ecran.blit(lettre3_a, lettre3_rect)

    joystick = pygame.joystick.Joystick(0)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.JOYBUTTONDOWN:
                if joystick.get_button(13):
                    if lettre_mod > 1:
                        lettre_mod -= 1
                    else:
                        lettre_mod = 1

                if joystick.get_button(14):
                    if lettre_mod < 3:
                        lettre_mod += 1
                    else:
                        lettre_mod = 3

                if joystick.get_button(11):
                    if lettre_mod == 1:
                        i1 += 1
                        if i1 < 26:
                            lettre1 = lettres[i1]
                            lettre1_a = font.render(lettre1, False, WHITE)
                            lettre1_rect = lettre1_a.get_rect()
                            lettre1_rect.center = (SCREEN_W // 2 - 80, SCREEN_H // 2)
                            ecran.blit(inputbox_surf, inputbox_rect)
                            ecran.blit(lettre1_a, lettre1_rect)
                            ecran.blit(lettre2_a, lettre2_rect)
                            ecran.blit(lettre3_a, lettre3_rect)
                        else:
                            i1 = 0
                            lettre1 = lettres[i1]
                            lettre1_a = font.render(lettre1, False, WHITE)
                            lettre1_rect = lettre1_a.get_rect()
                            lettre1_rect.center = (SCREEN_W // 2 - 80, SCREEN_H // 2)
                            ecran.blit(inputbox_surf, inputbox_rect)
                            ecran.blit(lettre1_a, lettre1_rect)
                            ecran.blit(lettre2_a, lettre2_rect)
                            ecran.blit(lettre3_a, lettre3_rect)

                    elif lettre_mod == 2:
                        i2 += 1
                        if i2 < 26:
                            lettre2 = lettres[i2]
                            lettre2_a = font.render(lettre2, False, WHITE)
                            lettre2_rect = lettre2_a.get_rect()
                            lettre2_rect.center = (SCREEN_W // 2, SCREEN_H // 2)
                            ecran.blit(inputbox_surf, inputbox_rect)
                            ecran.blit(lettre1_a, lettre1_rect)
                            ecran.blit(lettre2_a, lettre2_rect)
                            ecran.blit(lettre3_a, lettre3_rect)
                        else:
                            i2 = 0
                            lettre2 = lettres[i2]
                            lettre2_a = font.render(lettre2, False, WHITE)
                            lettre2_rect = lettre2_a.get_rect()
                            lettre2_rect.center = (SCREEN_W // 2, SCREEN_H // 2)
                            ecran.blit(inputbox_surf, inputbox_rect)
                            ecran.blit(lettre1_a, lettre1_rect)
                            ecran.blit(lettre2_a, lettre2_rect)
                            ecran.blit(lettre3_a, lettre3_rect)

                    elif lettre_mod == 3:
                        i3 += 1
                        if i3 < 26:
                            lettre3 = lettres[i3]
                            lettre3_a = font.render(lettre3, False, WHITE)
                            lettre3_rect = lettre3_a.get_rect()
                            lettre3_rect.center = (SCREEN_W // 2 + 80, SCREEN_H // 2)
                            ecran.blit(inputbox_surf, inputbox_rect)
                            ecran.blit(lettre1_a, lettre1_rect)
                            ecran.blit(lettre2_a, lettre2_rect)
                            ecran.blit(lettre3_a, lettre3_rect)
                        else:
                            i3 = 0
                            lettre3 = lettres[i3]
                            lettre3_a = font.render(lettre3, False, WHITE)
                            lettre3_rect = lettre3_a.get_rect()
                            lettre3_rect.center = (SCREEN_W // 2 + 80, SCREEN_H // 2)
                            ecran.blit(inputbox_surf, inputbox_rect)
                            ecran.blit(lettre1_a, lettre1_rect)
                            ecran.blit(lettre2_a, lettre2_rect)
                            ecran.blit(lettre3_a, lettre3_rect)

                if joystick.get_button(12):
                    if lettre_mod == 1:
                        i1 -= 1
                        if i1 >= 0:
                            lettre1 = lettres[i1]
                            lettre1_a = font.render(lettre1, False, WHITE)
                            lettre1_rect = lettre1_a.get_rect()
                            lettre1_rect.center = (SCREEN_W // 2 - 80, SCREEN_H // 2)
                            ecran.blit(inputbox_surf, inputbox_rect)
                            ecran.blit(lettre1_a, lettre1_rect)
                            ecran.blit(lettre2_a, lettre2_rect)
                            ecran.blit(lettre3_a, lettre3_rect)
                        else:
                            i1 = 25
                            lettre1 = lettres[i1]
                            lettre1_a = font.render(lettre1, False, WHITE)
                            lettre1_rect = lettre1_a.get_rect()
                            lettre1_rect.center = (SCREEN_W // 2 - 80, SCREEN_H // 2)
                            ecran.blit(inputbox_surf, inputbox_rect)
                            ecran.blit(lettre1_a, lettre1_rect)
                            ecran.blit(lettre2_a, lettre2_rect)
                            ecran.blit(lettre3_a, lettre3_rect)

                    elif lettre_mod == 2:
                        i2 -= 1
                        if i2 >= 0:
                            lettre2 = lettres[i2]
                            lettre2_a = font.render(lettre2, False, WHITE)
                            lettre2_rect = lettre2_a.get_rect()
                            lettre2_rect.center = (SCREEN_W // 2, SCREEN_H // 2)
                            ecran.blit(inputbox_surf, inputbox_rect)
                            ecran.blit(lettre1_a, lettre1_rect)
                            ecran.blit(lettre2_a, lettre2_rect)
                            ecran.blit(lettre3_a, lettre3_rect)
                        else:
                            i2 = 25
                            lettre2 = lettres[i2]
                            lettre2_a = font.render(lettre2, False, WHITE)
                            lettre2_rect = lettre2_a.get_rect()
                            lettre2_rect.center = (SCREEN_W // 2, SCREEN_H // 2)
                            ecran.blit(inputbox_surf, inputbox_rect)
                            ecran.blit(lettre1_a, lettre1_rect)
                            ecran.blit(lettre2_a, lettre2_rect)
                            ecran.blit(lettre3_a, lettre3_rect)

                    elif lettre_mod == 3:
                        i3 -= 1
                        if i3 >= 0:
                            lettre3 = lettres[i3]
                            lettre3_a = font.render(lettre3, False, WHITE)
                            lettre3_rect = lettre3_a.get_rect()
                            lettre3_rect.center = (SCREEN_W // 2 + 80, SCREEN_H // 2)
                            ecran.blit(inputbox_surf, inputbox_rect)
                            ecran.blit(lettre1_a, lettre1_rect)
                            ecran.blit(lettre2_a, lettre2_rect)
                            ecran.blit(lettre3_a, lettre3_rect)
                        else:
                            i3 = 25
                            lettre3 = lettres[i3]
                            lettre3_a = font.render(lettre3, False, WHITE)
                            lettre3_rect = lettre3_a.get_rect()
                            lettre3_rect.center = (SCREEN_W // 2 + 80, SCREEN_H // 2)
                            ecran.blit(inputbox_surf, inputbox_rect)
                            ecran.blit(lettre1_a, lettre1_rect)
                            ecran.blit(lettre2_a, lettre2_rect)
                            ecran.blit(lettre3_a, lettre3_rect)

                if joystick.get_button(15):
                    nom = lettre1 + lettre2 + lettre3
                    return nom

        pygame.display.flip()
