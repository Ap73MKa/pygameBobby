from pygame.sprite import Group, Sprite

from game.misc import PathManager, SpriteSheet
from game.scene.sound_manager import SoundManager


class Trigger(Sprite):
    def __init__(self, pos: tuple[int, int], groups: list[Group]):
        super().__init__(*groups)
        self.sprites = SpriteSheet(
            str(PathManager.get("assets/graphics/objects/exit_trigger.png")), (16, 16)
        )[0]
        self.sound_manager = SoundManager()
        self.frame = 0.0
        self.frame_speed = 15
        self.image = self.sprites[int(self.frame)]
        self.rect = self.image.get_rect(topleft=pos)
        self.is_activated = False

    def activate(self):
        if self.is_activated:
            return
        self.is_activated = True
        self.sound_manager.play_sound("open_exit")

    def deactivate(self):
        self.is_activated = False
        self.image = self.sprites[0]

    def animate(self, delta: float):
        self.frame += self.frame_speed * delta / 2
        if self.frame >= len(self.sprites):
            self.frame = 0
        self.image = self.sprites[int(self.frame)]

    def update(self, delta: float):
        if self.is_activated:
            self.animate(delta)
