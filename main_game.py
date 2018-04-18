import math
import pygame
import random
import pickle
import os.path
from pygame.locals import *
from tiles import *
from player import *
from enemies import *
from level import *

import sys

pygame.init()

size = (width, height) = (pygame.display.Info().current_w, pygame.display.Info().current_h)

screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
color = (0, 0, 0)
images = {"w": "images/tiles/wall12.gif", "f": "images/tiles/floor13.gif",
          "s": {True: "images/tiles/openDoor31.gif", False: "images/tiles/door31.gif"},
          "e": {True: "images/tiles/openDoor12.gif", False: "images/tiles/door12.gif"}}
player = Player("images/player/superhero.gif", (16, 16), False)
levels = []
level_num = 0
current_level = None
'''for font in pygame.font.get_fonts():
    print(font)'''
font = pygame.font.SysFont('oldenglishtext', 32)


def change_level(change):
    global level_num, current_level
    if change == 1:
        if level_num == len(levels) - 1:
            levels.append(RandomLevel(player, images, .5, 2 + 2 * level_num))
        level_num += 1
        current_level = levels[level_num]
        player.up_level(current_level)
    elif change == -1:
        if level_num > 0:
            level_num -= 1
            current_level = levels[level_num]
            player.back_level(current_level)


def load_game():
    global player, levels, level_num, current_level
    if os.path.isfile("save"):
        f = open("save", "rb")
        player = pickle.load(f)
        player.load()
        level_num = pickle.load(f)
        levels = pickle.load(f)
        for l in levels:
            l.load(player)
        current_level = levels[level_num]
        player.level = current_level
        return True
    else:
        return False


def save_game():
    f = open("save", "wb")
    player.save()
    pickle.dump(player, f)
    pickle.dump(level_num, f)
    for level in levels:
        level.save()
    pickle.dump(levels, f)
    f.close()


def restart():
    global player, levels, level_num, current_level
    player = Player("images/player/superhero.gif", (16, 16), False)
    levels = [RandomLevel(player, images, .5, 2)]
    level_num = 0
    current_level = levels[level_num]
    player.up_level(current_level)


def main():
    global screen, level_num, current_level
    if not load_game():
        restart()
    restart_pressed = False
    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == QUIT:
                save_game()
                sys.exit()
            if event.type == KEYDOWN:
                if restart_pressed:
                    if event.key == K_RETURN:
                        restart()
                        restart_pressed = False
                    elif event.key == K_ESCAPE:
                        restart_pressed = False
                    continue
                if event.key == K_f:
                    screen = pygame.display.set_mode(size, FULLSCREEN)
                elif event.key == K_ESCAPE:
                    screen = pygame.display.set_mode(size)
                elif event.key == K_UP:
                    player.change_y(-32)
                elif event.key == K_DOWN:
                    player.change_y(32)
                elif event.key == K_RIGHT:
                    player.change_x(32)
                elif event.key == K_LEFT:
                    player.change_x(-32)
                elif event.key == K_a:
                    player.attack()
                elif event.key == K_r:
                    restart_pressed = True
                # Go up one level
                elif event.key == K_w:
                    if level_num == len(levels)-1:
                        levels.append(RandomLevel(player, images, .5, 2 + 2 * level_num))
                    level_num += 1
                    current_level = levels[level_num]
                    player.up_level(current_level)
                # Go down one level
                elif event.key == K_s:
                    if level_num > 0:
                        level_num -= 1
                        current_level = levels[level_num]
                        player.back_level(current_level)
        if not restart_pressed:
            change_level(current_level.update())
        screen.fill(color)
        current_level.draw(screen)
        text = font.render("Level: {}    Health: {}    Attack LvL: {}    Defense LvL: {}".format(
            level_num+1, player.health, player.attack_damage, player.defense), True, (230, 230, 230))
        text_rect = text.get_rect()
        text_rect.bottomright = (width, height)
        screen.blit(text, text_rect)
        if restart_pressed:
            text = font.render("Press Enter to restart, press ESC to cancel", True, (230, 230, 230))
            text_rect = text.get_rect()
            text_rect.center = (width//2, height//2)
            screen.blit(text, text_rect)
        pygame.display.flip()


if __name__ == "__main__":
    main()
