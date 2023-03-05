from enum import IntEnum, auto

import pygame.sprite
from pygame import Vector2
from pygame.time import get_ticks
from pygame.transform import scale

from src.misc.config import Config
from src.misc.path import PathManager
from src.misc.spritesheet import SpriteSheet


class AnimEnum(IntEnum):
    UP = 0
    LEFT = auto()
    DOWN = auto()
    RIGHT = auto()
    DYING = auto()
    FADING = auto()


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group: pygame.sprite.Group, collision_group: pygame.sprite.Group):
        super().__init__(group)
        self.anim_state = 'idle'
        self.is_inactive = False
        # self.player_state = 'idle'
        self.frame = 0
        self.frame_speed = 35
        self.sprites = self.import_animations()

        # image and rect
        self.image = self.sprites['down'][self.frame]
        image_size = self.image.get_size()
        self.image_offset = Vector2(image_size[0] - Config.TITLE_SIZE, image_size[1] - Config.TITLE_SIZE)
        self.rect = self.image.get_rect(center=pos)
        self.rect = self.rect.inflate(-self.image_offset.x, -self.image_offset.y)
        self.pos = Vector2(self.rect.center)
        self.target_pos = Vector2(self.rect.center)
        self.direction = Vector2()
        self.dx = self.dy = 0

        self.move_speed = 4
        self.inactive_start = pygame.time.get_ticks()
        self.collision_group = collision_group

    def import_animations(self) -> dict:
        return {
            'up': self.upscale_spritesheet(SpriteSheet(PathManager.get('assets/graphics/player/up.png'), (18, 25))),
            'down': self.upscale_spritesheet(SpriteSheet(PathManager.get('assets/graphics/player/down.png'), (18, 25))),
            'left': self.upscale_spritesheet(SpriteSheet(PathManager.get('assets/graphics/player/left.png'), (18, 25))),
            'right': self.upscale_spritesheet(
                SpriteSheet(PathManager.get('assets/graphics/player/right.png'), (18, 25))),
            'idle': self.upscale_spritesheet(SpriteSheet(PathManager.get('assets/graphics/player/idle.png'), (18, 25))),
            'fading': self.upscale_spritesheet(
                SpriteSheet(PathManager.get('assets/graphics/player/fading.png'), (18, 25))),
            'dying': self.upscale_spritesheet(
                SpriteSheet(PathManager.get('assets/graphics/player/dying.png'), (18, 25))),
        }

    @staticmethod
    def upscale_spritesheet(spritesheet: SpriteSheet):
        return [scale(image, (image.get_size()[0] * 3, image.get_size()[1] * 3)) for image in spritesheet[0]]

    def input(self):
        if not (self.is_target_pos() and self.dx == self.dy == 0):
            return
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.direction.y = -1
            self.anim_state = 'up'
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
            self.anim_state = 'down'
        else:
            self.direction.y = 0

        if keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.anim_state = 'left'
        elif keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.anim_state = 'right'
        else:
            self.direction.x = 0

    def is_target_pos(self) -> bool:
        return abs(self.pos.x - self.target_pos.x) <= 2 and abs(self.pos.y - self.target_pos.y) <= 2

    def set_target_pos(self):
        if self.is_target_pos() and self.dx == self.dy == 0:
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
            self.dx = (self.target_pos.x - self.pos.x) / self.move_speed * delta * 10
            self.dy = (self.target_pos.y - self.pos.y) / self.move_speed * delta * 10
        self.rect.x = self.pos.x - self.image_offset.x // 2
        self.rect.y = self.pos.y - self.image_offset.y

    def animate(self, delta):
        animation = self.sprites[self.anim_state]
        self.frame += self.frame_speed * delta / 2
        if self.is_inactive and self.anim_state != 'idle':
            self.frame = 0
            self.image = animation[self.frame]
            return
        if self.frame >= len(animation):
            self.frame = 0
        self.image = animation[int(self.frame)]

    def collision(self):
        test_rect: pygame.Rect = self.rect.copy()
        test_rect.x = self.target_pos.x
        test_rect.y = self.target_pos.y
        for sprite in self.collision_group:
            if sprite.rect.colliderect(test_rect):
                self.direction.x = 0
                self.direction.y = 0
                self.target_pos.x = self.pos.x
                self.target_pos.y = self.pos.y

    def check_inactive(self):
        if not self.is_inactive:
            self.inactive_start = get_ticks()
            return
        if get_ticks() - self.inactive_start >= 5000:
            self.anim_state = 'idle'

    def check_state(self):
        self.is_inactive = True if self.direction == self.direction * 0 else False

    def update(self, delta: float):
        self.input()
        self.set_target_pos()
        self.collision()
        self.move(delta)
        self.check_state()
        self.check_inactive()
        self.animate(delta)
