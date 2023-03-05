import pygame.sprite
from pygame.transform import scale

from src.misc.config import Config
from src.misc.path import PathManager
from src.misc.spritesheet import SpriteSheet


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group: pygame.sprite.Group, collision_group: pygame.sprite.Group):
        super().__init__(group)
        self.status = 'idle'
        self.frame = 0
        self.frame_speed = 30
        self.sprites = {}
        self.import_animations()
        self.image = self.sprites['down'][self.frame]
        self.player_state = 'idle'
        self.image = pygame.image.load(PathManager.get('assets/graphics/player/idle1.png')).convert_alpha()
        self.image = scale(self.image, (self.image.get_size()[0] * 3, self.image.get_size()[1] * 3))
        # self.image = pygame.Surface((Config.TITLE_SIZE, Config.TITLE_SIZE))
        # self.image.fill('red')
        self.image_offset_y = self.image.get_size()[1] - Config.TITLE_SIZE
        self.image_offset_x = self.image.get_size()[0] - Config.TITLE_SIZE
        self.rect = self.image.get_rect(center=pos)
        self.rect = self.rect.inflate(-self.image_offset_x, -self.image_offset_y)
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
        self.target_pos = pygame.math.Vector2(self.rect.center)
        self.rect.y -= self.image_offset_y
        self.speed = 4
        self.dx = self.dy = 0
        self.import_animations()
        self.inactive_timer = pygame.time.get_ticks()
        self.last_tick = pygame.time.get_ticks()
        self.inactive_time = 0
        self.collision_group = collision_group

    def import_animations(self):
        self.sprites = {
            'up': self.upscale_spritesheet(SpriteSheet(PathManager.get('assets/graphics/player/up.png'), (18, 25))),
            'down': self.upscale_spritesheet(SpriteSheet(PathManager.get('assets/graphics/player/down.png'), (18, 25))),
            'left': self.upscale_spritesheet(SpriteSheet(PathManager.get('assets/graphics/player/left.png'), (18, 25))),
            'right': self.upscale_spritesheet(SpriteSheet(PathManager.get('assets/graphics/player/right.png'), (18, 25))),
            'idle': self.upscale_spritesheet(SpriteSheet(PathManager.get('assets/graphics/player/idle.png'), (18, 25))),
            'fading': self.upscale_spritesheet(SpriteSheet(PathManager.get('assets/graphics/player/fading.png'), (18, 25))),
            'dying': self.upscale_spritesheet(SpriteSheet(PathManager.get('assets/graphics/player/dying.png'), (18, 25))),
        }

    def upscale_spritesheet(self, spritesheet: SpriteSheet):
        return [scale(image, (image.get_size()[0] * 3, image.get_size()[1] * 3)) for image in spritesheet[0]]

    def input(self):
        if not(self.is_target_pos() and self.dx == self.dy == 0):
            return
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.direction.y = -1
            self.status = 'up'
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
            self.status = 'down'
        else:
            self.direction.y = 0

        if keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.status = 'left'
        elif keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.status = 'right'
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
            self.dx = (self.target_pos.x - self.pos.x) / self.speed * delta * 10
            self.dy = (self.target_pos.y - self.pos.y) / self.speed * delta * 10
        self.rect.x = self.pos.x - self.image_offset_x // 2
        self.rect.y = self.pos.y - self.image_offset_y

    def animate(self, delta):
        animation = self.sprites[self.status]
        self.frame += self.frame_speed * delta / 2
        if self.player_state == 'idle' and self.status != 'idle':
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
                print(self.rect, self.pos, self.target_pos, sprite.rect)
                self.direction.x = 0
                self.direction.y = 0
                self.target_pos.x = self.pos.x
                self.target_pos.y = self.pos.y

    def check_inactive(self):
        if self.player_state == 'walk':
            self.inactive_time = 0
            return
        if self.inactive_time >= 5000:
            self.inactive_time = 0
            self.status = 'idle'
        else:
            self.inactive_time += pygame.time.get_ticks() - self.last_tick
            self.last_tick = pygame.time.get_ticks()

    def check_state(self):
        self.player_state = 'idle' if self.direction == self.direction * 0 else 'walk'

    def update(self, delta: float):
        self.input()
        self.set_target_pos()
        self.collision()
        self.check_inactive()
        self.move(delta)
        self.check_state()
        self.animate(delta)
