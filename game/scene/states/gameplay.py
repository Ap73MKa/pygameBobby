from pytmx import TiledMap
from pytmx.util_pygame import load_pygame
from pygame import Surface, Vector2, KEYUP, K_ESCAPE, QUIT
from pygame.display import get_surface
from pygame.sprite import Group
from pygame.time import get_ticks

from game.misc import Config, PathManager
from game.objects import Carrot, Player, Trap, Trigger, Tile
from game.scene.ui import UI
from game.scene.camera import CameraGroup
from .stage_utils import GameState
from .state import State
from ...objects.player import AnimEnum


class Gameplay(State):
    def __init__(self) -> None:
        super().__init__()
        self.player: Player | None = None
        self.tmx_data: TiledMap | None = None
        self.carrots_count = self.found_carrots = 0
        self.start_pos = (0, 0)
        self.index_map = 1
        self.corner = Vector2(Config.WIDTH, Config.HEIGHT)
        self.next_state = GameState.TRANSITION
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

        self.on_load()

    def startup(self, persistent: dict) -> None:
        self.next_state = GameState.TRANSITION
        index = self.index_map
        reload = False
        for key, item in persistent.items():
            if key == "level":
                index = item
            if key == "reload":
                reload = item
        if self.index_map != index or reload:
            self.index_map = index
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
                Carrot(pos, [self.carrots_group, self.visible_sprites])

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
            self.persist = {
                "level": self.index_map + 1,
                "time": self.ui.timer_text,
                "steps": self.player.get_step_count(),
            }
            self.player.anim_state = AnimEnum.FADING
            self.done = True

        for carrot in self.carrots_group:
            if carrot.rect.topleft == self.player.pos and not carrot.activated:
                self.found_carrots += 1
                carrot.activate()

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
        self.quit = e.type == QUIT
        if e.type == KEYUP and e.key == K_ESCAPE:
            self.next_state = GameState.PAUSE
            self.done = True

    def update(self, delta: float) -> None:
        self.check_collide()
        self.visible_sprites.custom_update(self.player, self.corner, delta)
        self.visible_sprites.update(delta)
        self.check_end()
        self.ui.update(self.carrots_count - self.found_carrots)

    def render(self, game_screen: Surface) -> None:
        self.visible_sprites.custom_render(game_screen)
        self.ui.render(game_screen)
