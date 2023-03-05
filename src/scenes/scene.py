from pygame import Surface
from pygame.display import get_surface
from pygame.image import load
from pygame.sprite import Group
from pytmx import TiledMap
from pytmx.util_pygame import load_pygame

from src.misc.config import Config
from src.misc.path import PathManager
from src.objects.player import Player
from src.scenes.tile import Tile


class Scene:
    def __init__(self):
        self.player: Player | None = None
        self.tmx_data: TiledMap | None = None
        self.carrots_count = self.found_carrots = 0
        self.start_pos = (0, 0)
        self.index_map = 1
        self.hole = load(PathManager.get('assets/graphics/objects/carrot_hole.png')).convert_alpha()
        # Groups
        self.display_surface = get_surface()
        self.all_sprites = Group()
        self.collision_sprites = Group()
        self.carrots_sprites = Group()
        self.trigger_group = Group()
        self.on_init()

    def on_init(self):
        self.tmx_data = load_pygame(PathManager.get(f'assets/maps/map{self.index_map}.tmx'))
        self.carrots_count = self.found_carrots = 0
        self.all_sprites.empty()
        self.collision_sprites.empty()
        self.trigger_group.empty()
        self.player = None
        self.unpack_map()
        self.player = Player(self.start_pos, self.all_sprites, self.collision_sprites)

    def unpack_map(self):
        for layer in self.tmx_data.visible_layers:
            if not hasattr(layer, 'data'):
                break
            for x, y, surf in layer.tiles():
                pos = (x * Config.TITLE_SIZE, y * Config.TITLE_SIZE)
                Tile(pos, surf, [self.all_sprites])

        layer = self.tmx_data.get_layer_by_name('border')
        if hasattr(layer, 'data'):
            for x, y, surf in layer.tiles():
                pos = (x * Config.TITLE_SIZE, y * Config.TITLE_SIZE)
                Tile(pos, Surface((Config.TITLE_SIZE, Config.TITLE_SIZE)), [self.collision_sprites])

        layer = self.tmx_data.get_layer_by_name('player')
        if hasattr(layer, 'data'):
            for x, y, surf in layer.tiles():
                pos = (x * Config.TITLE_SIZE, y * Config.TITLE_SIZE)
                self.start_pos = pos

        layer = self.tmx_data.get_layer_by_name('level_trigger')
        if hasattr(layer, 'data'):
            for x, y, surf in layer.tiles():
                pos = (x * Config.TITLE_SIZE, y * Config.TITLE_SIZE)
                Tile(pos, surf, [self.trigger_group, self.all_sprites])

        layer = self.tmx_data.get_layer_by_name('carrots')
        if hasattr(layer, 'data'):
            for x, y, surf in layer.tiles():
                self.carrots_count += 1
                pos = (x * Config.TITLE_SIZE, y * Config.TITLE_SIZE)
                Tile(pos, surf, [self.carrots_sprites, self.all_sprites])

    def check_collide(self):
        for sprite in self.trigger_group:
            if sprite.rect.collidepoint(self.player.pos.x, self.player.pos.y):
                if self.carrots_count == self.found_carrots:
                    self.index_map += 1
                    self.on_init()

        for sprite in self.carrots_sprites:
            if sprite.rect.x == self.player.pos.x and sprite.rect.y == self.player.pos.y:
                self.found_carrots += 1
                sprite.kill()

    def update(self, delta: float):
        self.check_collide()
        self.all_sprites.update(delta)

    def render(self):
        self.display_surface.fill('black')
        self.all_sprites.draw(self.display_surface)
