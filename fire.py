import pygame
from sprite_loader import *


class Fire(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        ss = SpriteSheet("images/fire_sheet.png")
        self.images = []
        for i in range(7):
            self.images.append(pygame.transform.scale(ss.get_image(i*24, 0, 24, 24), (40, 40)))
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.midbottom = pos
        self.time = 0

    def update(self):
        frame = (pygame.time.get_ticks() // 200 % 7)
        self.image = self.images[frame]
        self.time += 1
        if self.time > 50:
            self.kill()

    def save(self):
        self.image = None
        self.images = None

    def load(self):
        ss = SpriteSheet("images/fire_sheet.png")
        self.images = []
        for i in range(7):
            self.images.append(pygame.transform.scale(ss.get_image(i * 24, 0, 24, 24), (40, 40)))
        self.image = self.images[0]


