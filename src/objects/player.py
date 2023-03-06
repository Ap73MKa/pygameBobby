from enum import IntEnum, auto

from pygame import Vector2, K_UP, K_w, K_DOWN, K_s, K_LEFT, K_l, K_RIGHT, K_r
from pygame.key import get_pressed
from pygame.sprite import Sprite, Group
from pygame.time import get_ticks

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
    UNFADING = auto()


class Player(Sprite):
    def __init__(self, pos, group: Group, collision_group: Group):
        super().__init__(group)
        # animation
        self.frame = 0
        self.frame_speed = 35
        self.anim_state: AnimEnum = AnimEnum.UNFADING
        self.is_inactive = False
        self.sprites = self.import_animations()
        self.image = self.sprites[AnimEnum.UNFADING][self.frame]

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
        self.dx = self.dy = 0.0

        self.is_dying = False
        self.inactive_start = get_ticks()
        self.collision_group = collision_group

    @staticmethod
    def import_animations():
        anim_names = "right down left up idle dying fading unfading".strip().split()
        anim_path = "assets/graphics/player"
        return [
            SpriteSheet(
                PathManager.get(f"{anim_path}/{anim}.png"),
                (18, 25) if anim != "dying" else (22, 27),
            )[0]
            for anim in anim_names
        ]

    def input(self):
        if not (
            self.is_target_pos() and self.dx == self.dy == 0
        ) or self.anim_state in [AnimEnum.DYING, AnimEnum.FADING]:
            return

        keys = get_pressed()

        if keys[K_UP] or keys[K_w]:
            self.direction.y = -1
            self.anim_state = AnimEnum.UP
        elif keys[K_DOWN] or keys[K_s]:
            self.direction.y = 1
            self.anim_state = AnimEnum.DOWN
        else:
            self.direction.y = 0

        if keys[K_LEFT] or keys[K_l]:
            self.direction.x = -1
            self.anim_state = AnimEnum.LEFT
        elif keys[K_RIGHT] or keys[K_r]:
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
        if self.is_inactive and self.anim_state not in [
            AnimEnum.IDLE,
            AnimEnum.DYING,
            AnimEnum.FADING,
            AnimEnum.UNFADING,
        ]:
            self.frame = 0
            self.image = animation[self.frame]
            return
        if self.frame >= len(animation):
            if self.anim_state in [AnimEnum.DYING, AnimEnum.FADING, AnimEnum.UNFADING]:
                self.frame = len(animation) - 1
            else:
                self.frame = 0
        self.image = animation[int(self.frame)]

    def die(self):
        self.anim_state = AnimEnum.DYING
        if not self.is_dying:
            self.frame = 0
            self.is_dying = True

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
        if get_ticks() - self.inactive_start >= 8000:
            self.anim_state = AnimEnum.IDLE

    def update(self, delta: float):
        self.input()
        self.collision()
        self.check_inactive()
        self.move(delta)
        self.animate(delta)
