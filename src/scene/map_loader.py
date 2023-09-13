from pygame import Surface, image
from pygame.sprite import Group

from src.config import configure
from src.misc import PathManager
from src.objects import Carrot, Tile, Trap, Trigger, Water

from . import CameraGroup

# todo type hint, dict function mapping


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
                pos = (x * configure.TITLE_SIZE, y * configure.TITLE_SIZE)
                Water(pos, [self.visible_sprites])

        for layer in tmx_data.visible_layers:
            if hasattr(layer, "data"):
                for x, y, surf in layer.tiles():
                    pos = (x * configure.TITLE_SIZE, y * configure.TITLE_SIZE)
                    Tile(pos, surf, [self.visible_sprites])

        layer = tmx_data.get_layer_by_name("traps")
        if hasattr(layer, "data"):
            for x, y, surf in layer.tiles():
                pos = (x * configure.TITLE_SIZE, y * configure.TITLE_SIZE)
                Trap(pos, [self.traps_group, self.visible_sprites])

        layer = tmx_data.get_layer_by_name("spawn_point")
        if hasattr(layer, "data"):
            for x, y, surf in layer.tiles():
                pos = (x * configure.TITLE_SIZE, y * configure.TITLE_SIZE)
                surf = image.load(
                    PathManager.get("assets/graphics/objects/spawn_trigger.png")
                )
                Tile(pos, surf, [self.visible_sprites])
                self.start_pos = pos

        layer = tmx_data.get_layer_by_name("exit_point")
        if hasattr(layer, "data"):
            for x, y, surf in layer.tiles():
                pos = (x * configure.TITLE_SIZE, y * configure.TITLE_SIZE)
                Trigger(pos, [self.level_triggers_group, self.visible_sprites])

        layer = tmx_data.get_layer_by_name("carrots")
        if hasattr(layer, "data"):
            for x, y, surf in layer.tiles():
                pos = (x * configure.TITLE_SIZE, y * configure.TITLE_SIZE)
                Carrot(pos, [self.carrots_group, self.visible_sprites])

        layer = tmx_data.get_layer_by_name("border")
        if hasattr(layer, "data"):
            for x, y, surf in layer.tiles():
                pos = (x * configure.TITLE_SIZE, y * configure.TITLE_SIZE)
                Tile(
                    pos,
                    Surface((configure.TITLE_SIZE, configure.TITLE_SIZE)),
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


# class MapLoader:
#     def __init__(self):
#         self.start_pos = (0, 0)
#         self.visible_sprites = CameraGroup()
#         self.collision_sprites = Group()
#         self.level_triggers_group = Group()
#         self.carrots_group = Group()
#         self.traps_group = Group()
#         self.layer_mapping = {
#             "background": (self.load_background_layer, [self.visible_sprites]),
#             "traps": (self.load_traps_layer, [self.traps_group, self.visible_sprites]),
#             "spawn_point": (self.load_spawn_layer, [self.visible_sprites]),
#             "exit_point": (self.load_exit_layer, [self.level_triggers_group, self.visible_sprites]),
#             "carrots": (self.load_carrots_layer, [self.carrots_group, self.visible_sprites]),
#             "border": (self.load_border_layer, [self.collision_sprites])
#         }
#
#     def load_map(self, tmx_data):
#         for layer_name, (load_func, groups) in self.layer_mapping.items():
#             layer = tmx_data.get_layer_by_name(layer_name)
#             if hasattr(layer, "data"):
#                 for x, y, surf in layer.tiles():
#                     pos = (x * configure.TITLE_SIZE, y * configure.TITLE_SIZE)
#                     load_func(pos, surf, groups)
#
#     def load_background_layer(self, pos, surf, groups):
#         Water(pos, groups)
#
#     def load_traps_layer(self, pos, surf, groups):
#         Trap(pos, groups)
#
#     def load_spawn_layer(self, pos, surf, groups):
#         surf = image.load(
#             PathManager.get("assets/graphics/objects/spawn_trigger.png")
#         )
#         Tile(pos, surf, groups)
#         self.start_pos = pos
#
#     def load_exit_layer(self, pos, surf, groups):
#         Trigger(pos, groups)
#
#     def load_carrots_layer(self, pos, surf, groups):
#         Carrot(pos, groups)
#
#     def load_border_layer(self, pos, surf, groups):
#         Tile(
#             pos,
#             Surface((configure.TITLE_SIZE, configure.TITLE_SIZE)),
#             groups,
#         )
#
#     def load_data(self, tmx_data):
#         self.load_map(tmx_data)
#         return (
#             self.start_pos,
#             self.visible_sprites,
#             self.collision_sprites,
#             self.level_triggers_group,
#             self.carrots_group,
#             self.traps_group,
#         )
