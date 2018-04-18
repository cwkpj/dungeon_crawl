import pygame, random
from enemies import *
from tiles import *


class Level(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        # groups
        self.walls = pygame.sprite.Group()
        self.floor = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.messages = pygame.sprite.Group()
        self.player = player
        self.game_map = []
        self.chest = Chest("images/chest.gif", (0, 0))
        self.walls.add(self.chest)
        self.start_pos = (0, 0)
        self.end_pos = (0, 0)
        self.exit = None
        self.start = None

    def update(self):
        self.enemies.update()
        self.messages.update()
        return self.player.update()
    
    def draw(self, screen):
        self.floor.draw(screen)
        self.enemies.draw(screen)
        self.player.draw(screen)
        self.walls.draw(screen)
        self.messages.draw(screen)

    def save(self):
        for e in self.enemies:
            e.save()
        for f in self.floor:
            f.save()
        for w in self.walls:
            w.save()
        for m in self.messages:
            m.save()
        self.player = None

    def load(self, player):
        for e in self.enemies:
            e.load(self)
        for f in self.floor:
            f.load()
        for w in self.walls:
            w.load()
        for m in self.messages:
            m.load()
        self.player = player


class RandomLevel(Level):
    def __init__(self, player, images, mult, enemy_num):
        super().__init__(player)

        self.generate_level(images, mult, enemy_num)

    def draw(self, screen):
        super().draw(screen)

    def place_player(self):
        for i in range(len(self.game_map)):
            for j in range(1, len(self.game_map[0])):
                if self.game_map[i][j] == "f":
                    self.start_pos = (i * 32, j * 32)
                    self.game_map[i][j - 1] = "s"
                    return

    def place_exit(self):
        for i in range(len(self.game_map) - 2, 0, -1):
            for j in range(1, len(self.game_map[0]) - 1):
                if self.game_map[i][j + 1] == "f":
                    self.end_pos = (i * 32, (j + 1) * 32)
                    self.game_map[i][j] = "e"
                    return
    
    def generate_level(self, images, mult, enemy_num):
        screen_info = pygame.display.Info()
        for i in range((screen_info.current_w // 32) + 1):
            self.game_map.append(["w"] * ((screen_info.current_h // 32) + 1))
        fnum = int((len(self.game_map) * len(self.game_map[0])) * mult)
        count = 0
        #tile = [random.randint(2, len(self.game_map)-3), random.randint(2, len(self.game_map[0])-3)]
        tile = [len(self.game_map)//2, len(self.game_map[0])//2]
        while count < fnum:
            if self.game_map[tile[0]][tile[1]] != "f":
                self.game_map[tile[0]][tile[1]] = "f"
                count += 1
            move = random.randint(1, 4)
            if move == 1 and tile[0] > 1:  # move north
                tile[0] -= 1
            elif move == 2 and tile[0] < (len(self.game_map) - 3):  # move south
                tile[0] += 1
            elif move == 3 and tile[1] < (len(self.game_map[0]) - 3):  # move east
                tile[1] += 1
            elif move == 4 and tile[1] > 1:  # move west
                tile[1] -= 1
        self.place_player()
        self.place_exit()
        for i in range(len(self.game_map)):
            for j in range(len(self.game_map[i])):
                if self.game_map[i][j] == "w":
                    self.walls.add(Tile(images["w"], (i * 32, j * 32)))
                elif self.game_map[i][j] == "f":
                    self.floor.add(Tile(images["f"], (i * 32, j * 32)))
                elif self.game_map[i][j] == "s":
                    self.start = Door(images["s"], (i * 32, j * 32), True)
                    self.walls.add(self.start)
                elif self.game_map[i][j] == "e":
                    self.exit = Door(images["e"], (i * 32, j * 32), False)
                    self.walls.add(self.exit)
        for i in range(enemy_num):
            self.enemies.add(Enemy("images/monsters/bat.gif", random.choice(self.floor.sprites()).rect.center, self))
        self.chest.rect.center = random.choice(self.floor.sprites()).rect.center
