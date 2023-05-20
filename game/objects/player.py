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


direction_mapping = {
    (0, -1, AnimEnum.UP): [K_UP, K_w],
    (0, 1, AnimEnum.DOWN): [K_DOWN, K_s],
    (-1, 0, AnimEnum.LEFT): [K_LEFT, K_a],
    (1, 0, AnimEnum.RIGHT): [K_RIGHT, K_d],
}


class Player(Sprite):
    def __init__(self, pos, group: Group, collision_group: Group):
        super().__init__(group)
        # animation
        self.frame = 0
        self.frame_speed = 10
        self.anim_state: AnimEnum = AnimEnum.DOWN
        self.sprites = SpriteSheet(
            str(PathManager.get("assets/graphics/player/walk.png")), (16, 17)
        )
        self.idle_sprites = SpriteSheet(
            str(PathManager.get("assets/graphics/player/idle.png")), (16, 17)
        )
        self.image = self.sprites[self.anim_state][self.frame]

        # movement
        self.image_offset = Vector2(*self.image.get_size()) - Vector2(Config.TITLE_SIZE)
        self.rect = self.image.get_rect(topleft=pos).inflate(*-self.image_offset)
        self.pos = Vector2(self.rect.topleft)
        self.target_pos = Vector2(self.rect.topleft)
        self.direction = Vector2()
        self.move_speed = 30

        self.is_dying = False
        self.is_inactive = False
        self.collision_group = collision_group
        self.step_count = 0

    @staticmethod
    def get_direction():
        keys = get_pressed()
        direction = Vector2()
        anim_state = AnimEnum.DOWN
        for dir, key_list in direction_mapping.items():
            for key in key_list:
                if keys[key]:
                    direction = Vector2(*dir[:2])
                    anim_state = dir[2]
                    break
        return direction, anim_state

    def input(self):
        if self.anim_state == AnimEnum.DYING or self.direction:
            return
        self.direction, state = self.get_direction()
        if self.direction:
            self.anim_state = state
            self.target_pos += self.direction * Config.TITLE_SIZE

    def get_step_count(self):
        step_count = self.step_count
        self.step_count = 0
        return step_count

    def move(self, delta: float):
        if not self.direction:
            return
        if self.pos == self.target_pos:
            self.direction *= 0
            self.step_count += 1
        else:
            move_vector = self.direction * self.move_speed * delta
            distance = self.pos.distance_to(self.target_pos)
            if distance > 0:
                speed_factor = move_vector.length() / distance
                speed_factor = min(speed_factor, 1)
                self.pos = self.pos.lerp(self.target_pos, speed_factor)
        self.rect.topleft = round(self.pos - self.image_offset)

    def animate(self, delta):
        animation = self.sprites[self.anim_state]
        if self.is_inactive and self.anim_state != AnimEnum.DYING:
            animation = self.idle_sprites[self.anim_state]
        self.frame += self.frame_speed * delta
        self.frame = self.frame % len(animation)
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
                self.direction.x *= 0
                self.target_pos = self.pos.copy()

    def check_inactive(self):
        self.is_inactive = not self.direction

    def update(self, delta: float):
        self.input()
        self.collision()
        self.check_inactive()
        self.move(delta)
        self.animate(delta)
