import pygame.sprite
from pygame.display import get_surface

from src.misc.config import Config
from src.objects.player import Player


class Scene:
    def __init__(self):
        self.player: Player | None = None
        self.display_surface = get_surface()
        self.all_sprites = pygame.sprite.Group()
        self.on_init()

    def on_init(self):
        self.player = Player((Config.TITLE_SIZE * 8, Config.TITLE_SIZE * 10), self.all_sprites)

    def update(self, delta: float):
        self.all_sprites.update(delta)

    def render(self):
        self.display_surface.fill('black')
        self.all_sprites.draw(self.display_surface)

