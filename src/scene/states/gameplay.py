from typing import Protocol

from pygame import K_ESCAPE, KEYUP, QUIT, Surface, Vector2
from pygame.event import Event
from pygame.sprite import Group
from pygame.time import get_ticks
from pytmx import TiledMap
from pytmx.util_pygame import load_pygame

from src.config import configure
from src.misc import PathManager
from src.objects import Player, Trigger
from src.scene import CameraGroup, Interface
from src.scene.map_loader import MapLoader
from src.scene.states.state import GameState, State


class Gameplay(State):
    def __init__(self) -> None:
        super().__init__()
        self.corner = Vector2(configure.WIDTH, configure.HEIGHT)
        self.next_state = GameState.TRANSITION

        self.player: Player | None = None
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
        self.ui = Interface()

        self.commands: dict[str, CommandProtocol] = self.get_commands()

        self.load_data(self.get_tmx_data())

    @staticmethod
    def get_commands() -> dict:
        return {
            "carrot": CarrotCommand(),
            "level_trigger": LevelTriggerCommand(),
            "trap": TrapCommand(),
        }

    def startup(self, persistent: dict) -> None:
        self.next_state = GameState.TRANSITION
        index = persistent.get("level", self.index_map)
        reload = persistent.get("reload", False)
        if reload:
            self.reset_data()
        if self.index_map != index:
            self.index_map = index
            self.load_data(self.get_tmx_data())

    def get_tmx_data(self) -> TiledMap:
        return load_pygame(str(PathManager.get(f"assets/maps/map{self.index_map}.tmx")))

    def reset_data(self):
        self.reset_objects()
        self.carrots_count = len(self.carrots_group)
        self.visible_sprites.remove(self.player)
        self.found_carrots = 0
        self.is_player_died = False
        self.player = Player(
            self.start_pos, self.visible_sprites, self.collision_sprites
        )
        self.ui.reset()

    def reset_objects(self):
        for carrot in self.carrots_group:
            carrot.deactivate()
        for trap in self.traps_group:
            trap.deactivate()
        for level_trigger in self.level_triggers_group:
            level_trigger.deactivate()

    def complete_level(self) -> None:
        self.persist = {
            "level": self.index_map + 1,
            "time": self.ui.get_time(),
            "steps": self.player.get_step_count(),
        }
        self.sound_manager.play_sound("exit_sound")
        self.done = True

    def load_data(self, tmx_data: TiledMap) -> None:
        map_loader = MapLoader()
        self.corner = Vector2(tmx_data.width, tmx_data.height) * configure.TITLE_SIZE
        (
            self.start_pos,
            self.visible_sprites,
            self.collision_sprites,
            self.level_triggers_group,
            self.carrots_group,
            self.traps_group,
        ) = map_loader.load_data(tmx_data)
        self.player = Player(
            self.start_pos, self.visible_sprites, self.collision_sprites
        )
        self.carrots_count = len(self.carrots_group)
        self.found_carrots = 0
        self.ui.reset()

    def check_collide(self) -> None:
        for command in self.commands.values():
            command.execute(self)

    def timeout_death(self) -> None:
        self.player.die()
        if not self.is_player_died:
            self.sound_manager.play_sound("hit_sound")
            self.is_player_died = True
            self.die_time = get_ticks()
        if get_ticks() - self.die_time >= 500:
            self.reset_data()
            self.sound_manager.play_sound("spawn_sound")

    def check_end(self) -> None:
        if self.carrots_count == self.found_carrots:
            trigger: Trigger = self.level_triggers_group.sprites()[0]
            trigger.activate()

    def handle_event(self, event: Event) -> None:
        self.quit = event.type == QUIT
        if event.type == KEYUP and event.key == K_ESCAPE:
            self.next_state = GameState.PAUSE
            self.done = True

    def update(self, delta: float) -> None:
        self.check_collide()
        self.visible_sprites.update(delta)
        self.visible_sprites.custom_update(self.player, self.corner, delta)
        self.check_end()
        self.ui.update(self.carrots_count - self.found_carrots)

    def render(self, game_surface: Surface) -> None:
        self.visible_sprites.custom_render(game_surface)
        self.ui.render(game_surface)


class CommandProtocol(Protocol):
    def execute(self, gameplay: Gameplay, *args, **kwargs) -> None:
        ...


class CarrotCommand(CommandProtocol):
    def execute(self, scene: Gameplay, *args, **kwargs) -> None:
        for carrot in scene.carrots_group:
            is_touched = carrot.rect.topleft == scene.player.pos
            if is_touched and not carrot.activated:
                scene.found_carrots += 1
                scene.sound_manager.play_sound("carrot_pickup")
                carrot.activate()


class LevelTriggerCommand(CommandProtocol):
    def execute(self, scene: Gameplay, *args, **kwargs) -> None:
        level_trigger: Trigger = scene.level_triggers_group.sprites()[0]
        is_touched = level_trigger.rect.topleft == scene.player.pos
        if is_touched and scene.carrots_count == scene.found_carrots:
            scene.complete_level()


class TrapCommand(CommandProtocol):
    def execute(self, scene: Gameplay, *args, **kwargs) -> None:
        for trap in scene.traps_group:
            if trap.rect.topleft == scene.player.pos:
                trap.is_touched = True
                if trap.is_activated:
                    scene.timeout_death()
            elif trap.is_touched and not trap.is_activated:
                trap.activate_trap()