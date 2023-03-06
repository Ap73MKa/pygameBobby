from pygame.image import load
from pygame.sprite import Group, Sprite
from pygame.transform import scale

from src.misc.config import Config
from src.misc.path import PathManager


class Trap(Sprite):
    def __init__(self, pos: tuple[int, int], groups: list[Group]):
        super().__init__(*groups)
        self.image = load(
            PathManager.get("assets/graphics/objects/trap_deactivated.png")
        )
        self.image = scale(self.image, (Config.TITLE_SIZE, Config.TITLE_SIZE))
        self.rect = self.image.get_rect(topleft=pos)
        self.activate = self.touched = False

    def activate_trap(self):
        self.activate = True
        self.image = load(PathManager.get("assets/graphics/objects/trap_activated.png"))
        self.image = scale(self.image, (Config.TITLE_SIZE, Config.TITLE_SIZE))
