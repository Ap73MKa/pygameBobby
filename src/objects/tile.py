from pygame import Surface
from pygame.sprite import Sprite, Group
from pygame.transform import scale

from src.misc.config import Config


class Tile(Sprite):
    def __init__(self, pos: tuple[int, int], surface: Surface, groups: list[Group]):
        super().__init__(*groups)
        self.image = surface.convert_alpha()
        self.image = scale(self.image, (Config.TITLE_SIZE, Config.TITLE_SIZE))
        self.rect = self.image.get_rect(topleft=pos)
