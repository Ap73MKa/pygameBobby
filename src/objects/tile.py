from pygame import Surface
from pygame.sprite import Group, Sprite
from pygame.transform import scale

from src.config import configure


class Tile(Sprite):
    def __init__(self, pos: tuple[int, int], surface: Surface, groups: list[Group]):
        super().__init__(*groups)
        self.image = surface.convert_alpha()
        self.image = scale(self.image, (configure.TITLE_SIZE, configure.TITLE_SIZE))
        self.rect = self.image.get_rect(topleft=pos)
