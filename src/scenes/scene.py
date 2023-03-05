import pygame.sprite
from pygame.display import get_surface
from pytmx.util_pygame import load_pygame

from src.misc.config import Config
from src.misc.path import PathManager
from src.objects.player import Player
from src.scenes.tile import Tile


class Scene:
    def __init__(self):
        self.player: Player | None = None
        self.tmx_data = load_pygame(PathManager.get('assets/maps/map1.tmx'))
        self.display_surface = get_surface()
        self.all_sprites = pygame.sprite.Group()
        self.load_map()
        self.on_init()

    def on_init(self):
        self.player = Player((Config.TITLE_SIZE * 8, Config.TITLE_SIZE * 9), self.all_sprites)

    def load_map(self):
        for layer in self.tmx_data.visible_layers:
            if not hasattr(layer, 'data'):
                break
            for x, y, surf in layer.tiles():
                pos = (x * Config.TITLE_SIZE, y * Config.TITLE_SIZE)
                Tile(pos, surf, [self.all_sprites])

    def update(self, delta: float):
        self.all_sprites.update(delta)

    def render(self):
        self.display_surface.fill('black')
        self.all_sprites.draw(self.display_surface)

