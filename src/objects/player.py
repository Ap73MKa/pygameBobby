import pygame.sprite
from src.misc.config import Config
from src.misc.path import PathManager


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group: pygame.sprite.Group):
        super().__init__(group)
        self.image = pygame.image.load(PathManager.get('assets/graphics/player/idle.png'))
        self.image = pygame.transform.scale2x(self.image)
        self.rect = self.image.get_rect(center=pos)
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
        self.target_pos = pygame.math.Vector2(self.rect.center)
        self.speed = 5
        self.dx = self.dy = 0

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0

    def is_target_pos(self) -> bool:
        return abs(self.pos.x - self.target_pos.x) <= 2 and abs(self.pos.y - self.target_pos.y) <= 2

    def set_target_pos(self):
        if self.is_target_pos():
            if (self.direction.x != 0) != (self.direction.y != 0):
                self.target_pos += self.direction * Config.TITLE_SIZE

    def move(self, delta: float):
        if self.dx != 0 or self.dy != 0:
            if self.is_target_pos():
                self.dx = self.dy = 0
                self.pos.x = round(self.pos.x / Config.TITLE_SIZE) * Config.TITLE_SIZE
                self.pos.y = round(self.pos.y / Config.TITLE_SIZE) * Config.TITLE_SIZE
            else:
                self.pos.x += self.dx
                self.pos.y += self.dy
        else:
            self.dx = (self.target_pos.x - self.pos.x) / self.speed * delta * 10
            self.dy = (self.target_pos.y - self.pos.y) / self.speed * delta * 10
        self.rect = self.pos

    def update(self, delta: float):
        self.input()
        self.set_target_pos()
        self.move(delta)
