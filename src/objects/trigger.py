from pygame.sprite import Group, Sprite
from pygame.transform import scale

from src.misc.path import PathManager
from src.misc.spritesheet import SpriteSheet


class Trigger(Sprite):
    def __init__(self, pos: tuple[int, int], groups: list[Group]):
        super().__init__(*groups)
        self.sprites = SpriteSheet(
            PathManager.get("assets/graphics/objects/trigger.png"), (16, 16)
        )
        self.sprites = [
            scale(sprite, (sprite.get_size()[0] * 3, sprite.get_size()[1] * 3))
            for sprite in self.sprites[0]
        ]
        self.frame = 0
        self.frame_speed = 35
        self.image = self.sprites[self.frame]
        self.rect = self.image.get_rect(topleft=pos)
        self.activated = False

    def activate(self):
        self.activated = True

    def animate(self, delta: float):
        self.frame += self.frame_speed * delta / 2
        if self.frame >= len(self.sprites):
            self.frame = 0
        self.image = self.sprites[int(self.frame)]

    def update(self, delta: float):
        if self.activated:
            self.animate(delta)
