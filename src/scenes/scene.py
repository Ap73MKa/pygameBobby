import pygame.time
from pygame import Surface, Vector2
from pygame.display import get_surface
from pygame.image import load
from pygame.sprite import Group
from pytmx import TiledMap
from pytmx.util_pygame import load_pygame

from src.misc.config import Config
from src.misc.path import PathManager
from src.objects.player import Player
from src.objects.trap import Trap
from src.scenes.camera import CameraGroup
from src.objects.tile import Tile
from src.scenes.ui import UI


class Scene:
    def __init__(self):
        self.player: Player | None = None
        self.tmx_data: TiledMap | None = None
        self.carrots_count = self.found_carrots = 0
        self.start_pos = (0, 0)
        self.index_map = 1
        self.hole = load(PathManager.get('assets/graphics/objects/carrot_hole.png')).convert_alpha()
        self.corner = Vector2(Config.WIDTH, Config.HEIGHT)
        self.ui = UI()

        # Groups
        self.display_surface = get_surface()
        self.visible_sprites = CameraGroup()
        self.collision_sprites = Group()
        self.trap_sprites = Group()
        self.carrots_sprites = Group()
        self.trigger_group = Group()

        self.on_load()

    def on_load(self):
        self.tmx_data = load_pygame(PathManager.get(f'assets/maps/map{self.index_map}.tmx'))
        self.corner = Vector2(self.tmx_data.width * Config.TITLE_SIZE, self.tmx_data.height * Config.TITLE_SIZE)
        self.carrots_count = self.found_carrots = 0
        self.visible_sprites.empty()
        self.collision_sprites.empty()
        self.trigger_group.empty()
        self.trap_sprites.empty()
        self.ui.set_start_time(pygame.time.get_ticks())
        self.player = None
        self.load_map()
        self.player = Player(self.start_pos, self.visible_sprites, self.collision_sprites)

    def load_map(self):
        for layer in self.tmx_data.visible_layers:
            if not hasattr(layer, 'data'):
                break
            for x, y, surf in layer.tiles():
                pos = (x * Config.TITLE_SIZE, y * Config.TITLE_SIZE)
                Tile(pos, surf, [self.visible_sprites])

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
                Tile(pos, surf, [self.trigger_group, self.visible_sprites])

        layer = self.tmx_data.get_layer_by_name('carrots')
        if hasattr(layer, 'data'):
            for x, y, surf in layer.tiles():
                self.carrots_count += 1
                pos = (x * Config.TITLE_SIZE, y * Config.TITLE_SIZE)
                Tile(pos, surf, [self.carrots_sprites, self.visible_sprites])

        layer = self.tmx_data.get_layer_by_name('trap')
        if hasattr(layer, 'data'):
            for x, y, surf in layer.tiles():
                pos = (x * Config.TITLE_SIZE, y * Config.TITLE_SIZE)
                Trap(pos, surf, [self.trap_sprites, self.visible_sprites])

    def check_collide(self):
        for sprite in self.trigger_group:
            if sprite.rect.collidepoint(self.player.pos.x, self.player.pos.y):
                if self.carrots_count == self.found_carrots:
                    self.index_map += 1
                    self.on_load()

        for carrot in list(filter(lambda sprite: sprite.rect.topleft == self.player.pos, self.carrots_sprites)):
            self.found_carrots += 1
            carrot.kill()

        for sprite in self.trap_sprites:
            sprite: Trap
            if sprite.rect.x == self.player.pos.x and sprite.rect.y == self.player.pos.y:
                sprite.touched = True
                if sprite.activate:
                    self.on_load()
            elif sprite.touched:
                if not sprite.activate:
                    sprite.activate_trap()

    def update(self, delta: float):
        self.check_collide()
        self.visible_sprites.custom_update(self.player, self.corner, delta)
        self.visible_sprites.update(delta)
        self.ui.update(self.carrots_count - self.found_carrots)

    def render(self):
        self.visible_sprites.custom_render()
        self.ui.render()
