from pygame import mixer
from pygame.image import load
from pygame.sprite import Group, Sprite

from game.misc import PathManager


class Trap(Sprite):
    def __init__(self, pos: tuple[int, int], groups: list[Group]) -> None:
        super().__init__(*groups)
        self.image = load(
            PathManager.get("assets/graphics/objects/trap_deactivated.png")
        )
        self.open_trap = mixer.Sound(PathManager.get("assets/sounds/open_trap.wav"))
        self.rect = self.image.get_rect(topleft=pos)
        self.activate = self.touched = False

    def activate_trap(self) -> None:
        self.activate = True
        self.image = load(PathManager.get("assets/graphics/objects/trap_activated.png"))
        self.open_trap.play()
