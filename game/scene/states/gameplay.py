from pygame.image import load
from pytmx import TiledMap
from pytmx.util_pygame import load_pygame
from pygame import Surface, Vector2, KEYUP, K_ESCAPE, QUIT
from pygame.sprite import Group
from pygame.time import get_ticks

from game.misc import Config, PathManager
from game.objects import Carrot, Player, Trap, Trigger, Tile, Water
from game.scene.ui import UI
from game.scene.camera import CameraGroup
from game.scene.states.stage_utils import GameState
from game.scene.states.state import State


class Gameplay(State):
    def __init__(self) -> None:
        super().__init__()
        self.corner = Vector2(Config.WIDTH, Config.HEIGHT)
        self.next_state = GameState.TRANSITION

        self.player: Player | None = None
        self.tmx_data: TiledMap | None = None
        self.carrots_count = self.found_carrots = 0
        self.start_pos = (0, 0)
        self.index_map = 1
        self.is_player_died = False
        self.die_time = get_ticks()

        self.visible_sprites = CameraGroup()
        self.collision_sprites = Group()
        self.level_triggers_group = Group()
        self.carrots_group = Group()
        self.traps_group = Group()
        self.ui = UI()

        self.load_data()

    def startup(self, persistent: dict) -> None:
        self.next_state = GameState.TRANSITION
        index = persistent.get('level', self.index_map)
        reload = persistent.get('reload', False)
        if self.index_map != index or reload:
            self.index_map = index
            self.reset_data()
            self.load_data()

    def reset_data(self):
        self.visible_sprites.empty()
        self.collision_sprites.empty()
        self.level_triggers_group.empty()
        self.carrots_group.empty()
        self.traps_group.empty()
        self.carrots_count = self.found_carrots = 0
        self.is_player_died = False
        self.player = None
        self.ui.set_start_time(get_ticks())

    def load_data(self) -> None:
        self.tmx_data = load_pygame(str(PathManager.get(f"assets/maps/map{self.index_map}.tmx")))
        self.corner = Vector2(self.tmx_data.width, self.tmx_data.height) * Config.TITLE_SIZE
        self.load_map()
        self.player = Player(self.start_pos, self.visible_sprites, self.collision_sprites)

    def load_map(self) -> None:
        layer = self.tmx_data.get_layer_by_name("background")
        if hasattr(layer, "data"):
            for x, y, surf in layer.tiles():
                pos = (x * Config.TITLE_SIZE, y * Config.TITLE_SIZE)
                Water(pos, [self.visible_sprites])

        for layer in self.tmx_data.visible_layers:
            if not hasattr(layer, "data"):
                break
            for x, y, surf in layer.tiles():
                pos = (x * Config.TITLE_SIZE, y * Config.TITLE_SIZE)
                Tile(pos, surf, [self.visible_sprites])

        layer = self.tmx_data.get_layer_by_name("traps")
        if hasattr(layer, "data"):
            for x, y, surf in layer.tiles():
                pos = (x * Config.TITLE_SIZE, y * Config.TITLE_SIZE)
                Trap(pos, [self.traps_group, self.visible_sprites])

        layer = self.tmx_data.get_layer_by_name("spawn_point")
        if hasattr(layer, "data"):
            for x, y, surf in layer.tiles():
                pos = (x * Config.TITLE_SIZE, y * Config.TITLE_SIZE)
                surf = load(
                    PathManager.get("assets/graphics/objects/spawn_trigger.png")
                )
                Tile(pos, surf, [self.visible_sprites])
                self.start_pos = pos

        layer = self.tmx_data.get_layer_by_name("exit_point")
        if hasattr(layer, "data"):
            for x, y, surf in layer.tiles():
                pos = (x * Config.TITLE_SIZE, y * Config.TITLE_SIZE)
                Trigger(pos, [self.level_triggers_group, self.visible_sprites])

        layer = self.tmx_data.get_layer_by_name("carrots")
        if hasattr(layer, "data"):
            for x, y, surf in layer.tiles():
                self.carrots_count += 1
                pos = (x * Config.TITLE_SIZE, y * Config.TITLE_SIZE)
                Carrot(pos, [self.carrots_group, self.visible_sprites])

        layer = self.tmx_data.get_layer_by_name("border")
        if hasattr(layer, "data"):
            for x, y, surf in layer.tiles():
                pos = (x * Config.TITLE_SIZE, y * Config.TITLE_SIZE)
                Tile(
                    pos,
                    Surface((Config.TITLE_SIZE, Config.TITLE_SIZE)),
                    [self.collision_sprites],
                )

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
            self.sound_manager.play_sound('exit_sound')
            self.done = True

        for carrot in self.carrots_group:
            if carrot.rect.topleft == self.player.pos and not carrot.activated:
                self.found_carrots += 1
                self.sound_manager.play_sound('carrot_sound')
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
            self.sound_manager.play_sound('hit_sound')
            self.is_player_died = True
            self.die_time = get_ticks()
        if get_ticks() - self.die_time >= 500:
            self.reset_data()
            self.load_data()
            self.sound_manager.play_sound('spawn_sound')

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
        self.visible_sprites.update_camera_pos(self.player, self.corner, delta)
        self.visible_sprites.update(delta)
        self.check_end()
        self.ui.update(self.carrots_count - self.found_carrots)

    def render(self, game_surface: Surface) -> None:
        self.visible_sprites.custom_render(game_surface)
        self.ui.render(game_surface)
