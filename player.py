import pygame, random
from message import *

class Player(pygame.sprite.Sprite):
    def __init__(self, path, pos, facing_r):
        super().__init__()
        self.path = path
        self.facing_r = facing_r
        self.image = pygame.image.load(self.path)
        if not self.facing_r:
            self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.movement = [0, 0]
        self.level = None
        self.inventory = {}
        self.health = 100
        self.attack_damage = 5
        self.defense = 1
        self.enemies = None
        self.facing = 'R'

    def update(self):
        if self.facing == 'R':
            self.image = pygame.image.load(self.path)
            if not self.facing_r:
                self.image = pygame.transform.flip(self.image, True, False)
        else:
            self.image = pygame.image.load(self.path)
            if self.facing_r:
                self.image = pygame.transform.flip(self.image, True, False)
        self.rect.move_ip(self.movement)
        if len(pygame.sprite.spritecollide(self, self.level.walls, False)) >= 1:
            if pygame.sprite.collide_rect(self, self.level.exit)and self.level.exit.unlocked:
                return 1
            if pygame.sprite.collide_rect(self, self.level.start):
                return -1
            if pygame.sprite.collide_rect(self, self.level.chest):
                self.level.messages.add(Message(self.level.chest.give_bonus(self), self.level.chest.rect.center))
            else:
                self.movement[0] *= -1
                self.movement[1] *= -1
                self.rect.move_ip(self.movement)
        self.enemies = pygame.sprite.spritecollide(self, self.level.enemies, False)
        self.movement[0] = 0
        self.movement[1] = 0

    def attack(self):
        if len(self.enemies) > 0:
            random.choice(self.enemies).defend(self.attack_damage)

    def defend(self, damage):
        if random.randint(1, 20) > self.defense:
            self.health -= damage
            self.level.messages.add(Message("-{}".format(damage), self.rect.topleft, (255, 0, 0)))
            if self.health <= 0:
                return True

    def up_level(self, level):
        self.movement = [0, 0]
        self.level = level
        self.rect.topleft = level.start_pos

    def back_level(self, level):
        self.movement = [0, 0]
        self.level = level
        self.rect.topleft = level.end_pos

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def change_x(self, change):
        self.movement[0] = change
        if change > 0:
            self.facing = 'R'
        else:
            self.facing = 'L'

    def change_y(self, change):
        self.movement[1] = change
