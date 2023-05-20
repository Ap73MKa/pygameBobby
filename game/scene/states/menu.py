from pygame import Color, QUIT, KEYUP, K_UP, K_DOWN, K_RIGHT, K_LEFT, K_RETURN, Surface
from pygame.image import load
from pytmx import load_pygame
from pygame.sprite import Group

from game.misc import PathManager, Config, FontManager
from .state import State
from .stage_utils import GameState
from ...objects import Tile, Water


class Menu(State):
    def __init__(self) -> None:
        super().__init__()
        self.level_index = 1
        self.font_manager = FontManager()
        self.bg_tile = load(PathManager.get("assets/graphics/hud/grass.png")).convert()
        self.tmx_data = load_pygame(str(PathManager.get("assets/maps/menu.tmx")))
        self.visible_sprites = Group()
        self.center = (Config.WIDTH // 2, Config.HEIGHT // 2)
        self.active_index = 0
        self.options = [
            "New game",
            f"Choose level <{self.level_index}>",
            "Quit",
        ]
        self.next_state = GameState.GAMEPLAY
        self.persist = {}

        self.on_load()

    def on_load(self):
        self.visible_sprites.empty()

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

    def handle_action(self) -> None:
        if self.active_index == 0:
            self.persist = {"level": 1, "reload": True}
            self.done = True
        if self.active_index == 1:
            self.persist = {"level": self.level_index, "reload": True}
            self.done = True
        elif self.active_index == 2:
            self.quit = True

    def handle_option_index(self, move: int = 0):
        self.active_index += move
        if self.active_index < 0:
            self.active_index = len(self.options) - 1
        self.active_index %= len(self.options)

    def handle_level_index(self, move: int = 0):
        self.level_index += move
        if self.level_index > Config.MAX_LEVEL:
            self.level_index = 1
        elif self.level_index <= 0:
            self.level_index = Config.MAX_LEVEL
        self.options[1] = f"Choose level <{self.level_index}>"

    def get_event(self, e) -> None:
        if e.type == QUIT:
            self.quit = True
        elif e.type == KEYUP:
            if e.key == K_UP:
                self.handle_option_index(-1)
            elif e.key == K_DOWN:
                self.handle_option_index(1)
            elif e.key == K_RIGHT and self.active_index == 1:
                self.handle_level_index(1)
            elif e.key == K_LEFT and self.active_index == 1:
                self.handle_level_index(-1)
            elif e.key == K_RETURN:
                self.sound_manager.play_sound("menu_sound")
                self.handle_action()

    def update(self, delta: float) -> None:
        self.visible_sprites.update(delta)

    def render_menu_text(
        self, surface: Surface, index, y_pos: int, color: Color = (255, 255, 255)
    ):
        color = (150, 150, 150) if index != self.active_index else color
        pos = self.get_menu_text_position(surface, y_pos, self.options[index], index)
        self.font_manager.render_text(surface, self.options[index], pos, color)

    def get_menu_text_position(
        self, surface: Surface, y_pos: int, text: str, index: int
    ) -> tuple[int, int]:
        pos = self.font_manager.get_text_center_x_pos(surface, text, y_pos)
        return pos[0], pos[1] + (index * 20)

    def render(self, game_surface: Surface) -> None:
        self.visible_sprites.draw(game_surface)
        self.font_manager.render_text(
            game_surface,
            "Bobby Carrot",
            self.font_manager.get_text_center_x_pos(game_surface, "Bobby Carrot", 55),
        )
        for index in range(len(self.options)):
            self.render_menu_text(
                game_surface, index, game_surface.get_rect().centery - 10
            )
