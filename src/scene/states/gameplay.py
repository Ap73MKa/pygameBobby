from pytmx import TiledMap
from pytmx.util_pygame import load_pygame
from pygame import Surface, Vector2, KEYUP, K_ESCAPE
from pygame.display import get_surface
from pygame.sprite import Group
from pygame.time import get_ticks

from src.misc.config import Config
from src.misc.path import PathManager
from src.objects.player import Player
from src.objects.trap import Trap
from src.objects.trigger import Trigger
from src.scene.camera import CameraGroup
from src.objects.tile import Tile
from src.scene.states.stage_utils import GameStage
from src.scene.ui import UI
from src.scene.states.state import State


class Gameplay(State):
    def __init__(self) -> None:
        super().__init__()
        self.player: Player | None = None
        self.tmx_data: TiledMap | None = None
        self.carrots_count = self.found_carrots = 0
        self.start_pos = (0, 0)
        self.index_map = 1
        self.corner = Vector2(Config.WIDTH, Config.HEIGHT)
        self.next_state = GameStage.PAUSE
        self.is_player_died = False
        self.die_time = get_ticks()

        # Groups
        self.display_surface = get_surface()
        self.visible_sprites = CameraGroup()
        self.collision_sprites = Group()
        self.level_triggers_group = Group()
        self.carrots_group = Group()
        self.traps_group = Group()
        self.ui = UI()

    def startup(self, persistent: dict) -> None:
        try:
            self.index_map = persistent["level"]
        except:
            pass
        self.on_load()

    def on_load(self) -> None:
        # Reset
        self.visible_sprites.empty()
        self.collision_sprites.empty()
        self.level_triggers_group.empty()
        self.carrots_group.empty()
        self.traps_group.empty()

        self.carrots_count = self.found_carrots = 0
        self.is_player_died = False
        self.player = None
        self.ui.set_start_time(get_ticks())

        # Load
        self.tmx_data = load_pygame(
            PathManager.get(f"assets/maps/map{self.index_map}.tmx")
        )
        self.corner = (
            Vector2(self.tmx_data.width, self.tmx_data.height) * Config.TITLE_SIZE
        )
        self.load_map()
        self.player = Player(
            self.start_pos, self.visible_sprites, self.collision_sprites
        )

    def load_map(self) -> None:
        for layer in self.tmx_data.visible_layers:
            if not hasattr(layer, "data"):
                break
            for x, y, surf in layer.tiles():
                pos = (x * Config.TITLE_SIZE, y * Config.TITLE_SIZE)
                Tile(pos, surf, [self.visible_sprites])

        layer = self.tmx_data.get_layer_by_name("border")
        if hasattr(layer, "data"):
            for x, y, surf in layer.tiles():
                pos = (x * Config.TITLE_SIZE, y * Config.TITLE_SIZE)
                Tile(
                    pos,
                    Surface((Config.TITLE_SIZE, Config.TITLE_SIZE)),
                    [self.collision_sprites],
                )

        layer = self.tmx_data.get_layer_by_name("player")
        if hasattr(layer, "data"):
            for x, y, surf in layer.tiles():
                pos = (x * Config.TITLE_SIZE, y * Config.TITLE_SIZE)
                self.start_pos = pos

        layer = self.tmx_data.get_layer_by_name("level_trigger")
        if hasattr(layer, "data"):
            for x, y, surf in layer.tiles():
                pos = (x * Config.TITLE_SIZE, y * Config.TITLE_SIZE)
                surf.fill("black")
                Trigger(pos, [self.level_triggers_group, self.visible_sprites])

        layer = self.tmx_data.get_layer_by_name("carrots")
        if hasattr(layer, "data"):
            for x, y, surf in layer.tiles():
                self.carrots_count += 1
                pos = (x * Config.TITLE_SIZE, y * Config.TITLE_SIZE)
                Tile(pos, surf, [self.carrots_group, self.visible_sprites])

        layer = self.tmx_data.get_layer_by_name("trap")
        if hasattr(layer, "data"):
            for x, y, surf in layer.tiles():
                pos = (x * Config.TITLE_SIZE, y * Config.TITLE_SIZE)
                Trap(pos, [self.traps_group, self.visible_sprites])

    def check_collide(self) -> None:
        level_trigger: Trigger = self.level_triggers_group.sprites()[0]
        if (
            level_trigger.rect.topleft == self.player.pos
            and self.carrots_count == self.found_carrots
        ):
            if self.index_map >= Config.MAX_LEVEL:
                self.done = True
                return
            self.index_map += 1
            self.on_load()

        for carrot in self.carrots_group:
            if carrot.rect.topleft == self.player.pos:
                self.found_carrots += 1
                carrot.kill()

        for trap in self.traps_group:
            if trap.rect.topleft == self.player.pos:
                trap.touched = True
                if trap.activate:
                    self.timeout_death()
            elif trap.touched and not trap.activate:
                trap.activate_trap()

    def timeout_death(self) -> None:
        self.player.die()
        if not self.is_player_died:
            self.is_player_died = True
            self.die_time = get_ticks()
        if get_ticks() - self.die_time >= 500:
            self.on_load()

    def check_end(self) -> None:
        if self.carrots_count == self.found_carrots:
            trigger: Trigger = self.level_triggers_group.sprites()[0]
            trigger.activate()

    def get_event(self, e) -> None:
        self.done = e.type == KEYUP and e.key == K_ESCAPE

    def update(self, delta: float) -> None:
        self.check_collide()
        self.visible_sprites.custom_update(self.player, self.corner, delta)
        self.visible_sprites.update(delta)
        self.check_end()
        self.ui.update(self.carrots_count - self.found_carrots)

    def render(self) -> None:
        self.visible_sprites.custom_render()
        self.ui.render()
