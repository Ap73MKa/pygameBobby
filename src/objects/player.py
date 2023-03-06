from enum import IntEnum, auto

import pygame.sprite
from pygame import Vector2
from pygame.time import get_ticks
from pygame.transform import scale

from src.misc.config import Config
from src.misc.path import PathManager
from src.misc.spritesheet import SpriteSheet


class AnimEnum(IntEnum):
    RIGHT = 0
    DOWN = auto()
    LEFT = auto()
    UP = auto()
    IDLE = auto()
    DYING = auto()
    FADING = auto()


class Player(pygame.sprite.Sprite):
    def __init__(
        self, pos, group: pygame.sprite.Group, collision_group: pygame.sprite.Group
    ):
        super().__init__(group)
        # animation
        self.frame = 0
        self.frame_speed = 35
        self.anim_state: AnimEnum = AnimEnum.IDLE
        self.is_inactive = False
        self.sprites = self.import_animations()
        self.image = self.sprites[AnimEnum.DOWN][self.frame]

        # movement
        image_size = self.image.get_size()
        self.image_offset = Vector2(
            image_size[0] - Config.TITLE_SIZE, image_size[1] - Config.TITLE_SIZE
        )
        self.rect = self.image.get_rect(center=pos).inflate(
            -self.image_offset.x, -self.image_offset.y
        )
        self.pos = Vector2(self.rect.center)
        self.target_pos = Vector2(self.rect.center)
        self.direction = Vector2()
        self.move_speed = 4
        self.dx = self.dy = .0

        self.inactive_start = pygame.time.get_ticks()
        self.collision_group = collision_group

    @staticmethod
    def upscale(sprite_sheet: SpriteSheet):
        return [
            scale(image, (image.get_size()[0] * 3, image.get_size()[1] * 3))
            for image in sprite_sheet[0]
        ]

    def import_animations(self):
        anim_names = "right down left up idle fading dying".strip().split()
        anim_path = "assets/graphics/player"
        return [
            self.upscale(
                SpriteSheet(PathManager.get(f"{anim_path}/{anim}.png"), (18, 25))
            )
            for anim in anim_names
        ]

    def input(self):
        if not (self.is_target_pos() and self.dx == self.dy == 0):
            return

        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.direction.y = -1
            self.anim_state = AnimEnum.UP
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
            self.anim_state = AnimEnum.DOWN
        else:
            self.direction.y = 0

        if keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.anim_state = AnimEnum.LEFT
        elif keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.anim_state = AnimEnum.RIGHT
        else:
            self.direction.x = 0

        if (self.direction.x != 0) != (self.direction.y != 0):
            self.target_pos += self.direction * Config.TITLE_SIZE

    def is_target_pos(self) -> bool:
        return (
            abs(self.pos.x - self.target_pos.x) <= 2
            and abs(self.pos.y - self.target_pos.y) <= 2
        )

    def move(self, delta: float):
        if self.dx != 0 or self.dy != 0:
            if self.is_target_pos():
                self.dx = self.dy = 0
                self.pos.x = round(self.pos.x / Config.TITLE_SIZE) * Config.TITLE_SIZE
                self.pos.y = round(self.pos.y / Config.TITLE_SIZE) * Config.TITLE_SIZE
            else:
                self.pos += Vector2(self.dx, self.dy)
        else:
            self.dx = (self.target_pos.x - self.pos.x) / self.move_speed * delta * 10
            self.dy = (self.target_pos.y - self.pos.y) / self.move_speed * delta * 10
        self.rect.topleft = Vector2(
            self.pos.x - self.image_offset.x // 2, self.pos.y - self.image_offset.y
        )

    def animate(self, delta):
        animation = self.sprites[self.anim_state]
        self.frame += self.frame_speed * delta / 2
        if self.is_inactive and self.anim_state != AnimEnum.IDLE:
            self.frame = 0
            self.image = animation[self.frame]
            return
        if self.frame >= len(animation):
            self.frame = 0
        self.image = animation[int(self.frame)]

    def collision(self):
        test_rect = self.rect.copy()
        test_rect.topleft = self.target_pos.copy()
        for sprite in self.collision_group:
            if sprite.rect.colliderect(test_rect):
                self.direction.x = self.direction.y = 0
                self.target_pos = self.pos.copy()

    def check_inactive(self):
        self.is_inactive = True if self.direction == self.direction * 0 else False
        if not self.is_inactive:
            self.inactive_start = get_ticks()
            return
        if get_ticks() - self.inactive_start >= 5000:
            self.anim_state = AnimEnum.IDLE

    def update(self, delta: float):
        self.input()
        self.collision()
        self.check_inactive()
        self.move(delta)
        self.animate(delta)
