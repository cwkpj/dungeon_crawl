import pygame


class SpriteSheet:

    def __init__(self, img_path):
        # load sprite sheet in
        self.sprite_sheet = pygame.image.load(img_path).convert()

    def get_image(self, x, y, width, height):
        # create a blank image
        img = pygame.Surface([width, height]).convert()
        img.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        img.set_colorkey(img.get_at((0, 0)))
        return img
