from pygame.image import load
from pygame.sprite import Group, Sprite

from game.misc import PathManager


class Carrot(Sprite):
    def __init__(self, pos: tuple[int, int], groups: list[Group]) -> None:
        super().__init__(*groups)
        self.image = load(PathManager.get("assets/graphics/objects/carrot.png"))
        self.rect = self.image.get_rect(topleft=pos)
        self.activated = False

    def activate(self) -> None:
        if not self.activated:
            self.image = load(
                PathManager.get("assets/graphics/objects/carrot_hole.png")
            )
            self.activated = True
