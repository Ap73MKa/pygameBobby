from pygame.image import load
from pygame.sprite import Group, Sprite

from game.misc import PathManager

activated_image = load(PathManager.get("assets/graphics/objects/hole.png"))
deactivated_image = load(PathManager.get("assets/graphics/objects/carrot.png"))


class Carrot(Sprite):
    def __init__(self, pos: tuple[int, int], groups: list[Group]) -> None:
        super().__init__(*groups)
        self.image = deactivated_image
        self.rect = self.image.get_rect(topleft=pos)
        self.activated = False

    def deactivate(self):
        self.activated = False
        self.image = deactivated_image

    def activate(self) -> None:
        if self.activated:
            return
        self.image = activated_image
        self.activated = True
