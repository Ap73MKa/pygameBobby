from pygame.image import load
from pygame.sprite import Group, Sprite

from game.misc import PathManager
from game.scene.sound_manager import SoundManager


activated_image = load(PathManager.get("assets/graphics/objects/trap_activated.png"))
deactivated_image = load(
    PathManager.get("assets/graphics/objects/trap_deactivated.png")
)


class Trap(Sprite):
    def __init__(self, pos: tuple[int, int], groups: list[Group]) -> None:
        super().__init__(*groups)
        self.image = deactivated_image
        self.sound_manager = SoundManager()
        self.rect = self.image.get_rect(topleft=pos)
        self.is_activated = self.is_touched = False

    def deactivate(self) -> None:
        self.is_activated = self.is_touched = False
        self.image = deactivated_image

    def activate_trap(self) -> None:
        self.is_activated = True
        self.image = activated_image
        self.sound_manager.play_sound("open_trap")
