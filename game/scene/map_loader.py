from pygame import Surface, Vector2
from pygame.image import load
from pygame.sprite import Group
from pytmx import load_pygame

from game.misc import Config, PathManager
from game.objects import Water, Tile, Trap, Trigger, Carrot
from .camera import CameraGroup


class MapLoader:
    def __init__(self):
        self.start_pos = (0, 0)
        self.visible_sprites = CameraGroup()
        self.collision_sprites = Group()
        self.level_triggers_group = Group()
        self.carrots_group = Group()
        self.traps_group = Group()

    def load_map(self, tmx_data):
        layer = tmx_data.get_layer_by_name("background")
        if hasattr(layer, "data"):
            for x, y, surf in layer.tiles():
                pos = (x * Config.TITLE_SIZE, y * Config.TITLE_SIZE)
                Water(pos, [self.visible_sprites])

        for layer in tmx_data.visible_layers:
            if not hasattr(layer, "data"):
                break
            for x, y, surf in layer.tiles():
                pos = (x * Config.TITLE_SIZE, y * Config.TITLE_SIZE)
                Tile(pos, surf, [self.visible_sprites])

        layer = tmx_data.get_layer_by_name("traps")
        if hasattr(layer, "data"):
            for x, y, surf in layer.tiles():
                pos = (x * Config.TITLE_SIZE, y * Config.TITLE_SIZE)
                Trap(pos, [self.traps_group, self.visible_sprites])

        layer = tmx_data.get_layer_by_name("spawn_point")
        if hasattr(layer, "data"):
            for x, y, surf in layer.tiles():
                pos = (x * Config.TITLE_SIZE, y * Config.TITLE_SIZE)
                surf = load(
                    PathManager.get("assets/graphics/objects/spawn_trigger.png")
                )
                Tile(pos, surf, [self.visible_sprites])
                self.start_pos = pos

        layer = tmx_data.get_layer_by_name("exit_point")
        if hasattr(layer, "data"):
            for x, y, surf in layer.tiles():
                pos = (x * Config.TITLE_SIZE, y * Config.TITLE_SIZE)
                Trigger(pos, [self.level_triggers_group, self.visible_sprites])

        layer = tmx_data.get_layer_by_name("carrots")
        if hasattr(layer, "data"):
            for x, y, surf in layer.tiles():
                pos = (x * Config.TITLE_SIZE, y * Config.TITLE_SIZE)
                Carrot(pos, [self.carrots_group, self.visible_sprites])

        layer = tmx_data.get_layer_by_name("border")
        if hasattr(layer, "data"):
            for x, y, surf in layer.tiles():
                pos = (x * Config.TITLE_SIZE, y * Config.TITLE_SIZE)
                Tile(
                    pos,
                    Surface((Config.TITLE_SIZE, Config.TITLE_SIZE)),
                    [self.collision_sprites],
                )

    def load_data(self, tmx_data):
        self.load_map(tmx_data)
        return (
            self.start_pos,
            self.visible_sprites,
            self.collision_sprites,
            self.level_triggers_group,
            self.carrots_group,
            self.traps_group,
        )
