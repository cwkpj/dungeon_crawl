import pygame


class Message(pygame.sprite.Sprite):
    def __init__(self, text, pos, color=(230, 230, 230)):
        super().__init__()
        font = pygame.font.SysFont('oldenglishtext', 25)
        self.image = font.render(text, True, color)
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.time = 0

    def update(self):
        self.time += 1
        self.rect.move_ip((0, -1))
        if self.time > 120:
            self.kill()
