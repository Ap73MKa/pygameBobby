from pygame import mixer
from pygame.sprite import Group, Sprite

from game.misc import PathManager, SpriteSheet


class Trigger(Sprite):
    def __init__(self, pos: tuple[int, int], groups: list[Group]):
        super().__init__(*groups)
        self.sprites = SpriteSheet(
            PathManager.get("assets/graphics/objects/exit_trigger.png"), (16, 16)
        )[0]
        self.open_exit_sound = mixer.Sound(
            PathManager.get("assets/sounds/open_exit.wav")
        )
        self.frame = 0.0
        self.frame_speed = 15
        self.image = self.sprites[int(self.frame)]
        self.rect = self.image.get_rect(topleft=pos)
        self.activated = False

    def activate(self):
        if not self.activated:
            self.activated = True
            self.open_exit_sound.play()

    def animate(self, delta: float):
        self.frame += self.frame_speed * delta / 2
        if self.frame >= len(self.sprites):
            self.frame = 0
        self.image = self.sprites[int(self.frame)]

    def update(self, delta: float):
        if self.activated:
            self.animate(delta)
