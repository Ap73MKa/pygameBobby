from enum import IntEnum, auto

from pygame import Vector2, K_UP, K_w, K_DOWN, K_s, K_LEFT, K_RIGHT, K_a, K_d
from pygame.key import get_pressed
from pygame.sprite import Sprite, Group

from game.misc import Config, PathManager, SpriteSheet


class AnimEnum(IntEnum):
    RIGHT = 0
    DOWN = auto()
    LEFT = auto()
    UP = auto()
    DYING = auto()


class IdleAnimEnum(IntEnum):
    RIGHT = 0
    DOWN = auto()
    LEFT = auto()
    UP = auto()


class Player(Sprite):
    def __init__(self, pos, group: Group, collision_group: Group):
        super().__init__(group)
        # animation
        self.frame = 0
        self.frame_speed = 20
        self.anim_state: AnimEnum = AnimEnum.DOWN
        self.is_inactive = False
        self.sprites = SpriteSheet(PathManager.get('assets/graphics/player/walk.png'), (16, 17))
        self.idle_sprites = SpriteSheet(PathManager.get('assets/graphics/player/idle.png'), (16, 17))
        self.image = self.sprites[self.anim_state][self.frame]

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
        self.move_speed = 6
        self.dx = self.dy = 0.0

        self.is_dying = False
        self.collision_group = collision_group
        self.step_count = 0

    def input(self):
        if not (
            self.is_target_pos() and self.dx == self.dy == 0
        ) or self.anim_state == AnimEnum.DYING:
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

        if keys[K_LEFT] or keys[K_a]:
            self.direction.x = -1
            self.anim_state = AnimEnum.LEFT
        elif keys[K_RIGHT] or keys[K_d]:
            self.direction.x = 1
            self.anim_state = AnimEnum.RIGHT
        else:
            self.direction.x = 0

        if (self.direction.x != 0) != (
            self.direction.y != 0
        ) and self.direction != self.direction * 0:
            self.step_count += 1
            self.target_pos += self.direction * Config.TITLE_SIZE

    def is_target_pos(self) -> bool:
        return (
            abs(self.pos.x - self.target_pos.x) <= 1
            and abs(self.pos.y - self.target_pos.y) <= 1
        )

    def get_step_count(self):
        step_count = self.step_count
        self.step_count = 0
        return step_count

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
        if self.is_inactive and self.anim_state != AnimEnum.DYING:
            animation = self.idle_sprites[self.anim_state]
        if self.frame >= len(animation):
            if self.anim_state == AnimEnum.DYING:
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
        self.is_inactive = self.direction == self.direction * 0

    def update(self, delta: float):
        self.input()
        self.collision()
        self.check_inactive()
        self.move(delta)
        self.animate(delta)
