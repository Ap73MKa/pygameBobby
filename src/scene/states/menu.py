from pygame import (
    Color,
    QUIT,
    KEYUP,
    K_UP,
    K_DOWN,
    K_RIGHT,
    K_LEFT,
    K_RETURN,
    Surface,
    SurfaceType,
    Rect,
)
from pygame.font import Font
from pygame.image import load

from src.misc import PathManager, Config
from .state import State
from .stage_utils import GameState


class Menu(State):
    def __init__(self) -> None:
        super().__init__()
        self.level_index = 1
        self.bg_tile = load(PathManager.get("assets/graphics/hud/grass.png")).convert()
        self.font = Font(PathManager.get("assets/graphics/hud/font.ttf"), 10)
        self.center = (Config.WIDTH // 2, Config.HEIGHT // 2)
        self.active_index = 0
        self.options = [
            "New game",
            f"Choose level <{self.level_index}>",
            "Credit",
            "Quit",
        ]
        self.next_state = GameState.GAMEPLAY
        self.persist = {}

    def __str__(self):
        return "menu"

    def render_text(self, index, custom_color=None) -> Surface | SurfaceType:
        color = (
            Color((255, 255, 255))
            if index == self.active_index
            else Color((100, 100, 100))
        )
        return self.font.render(
            self.options[index], False, custom_color if custom_color else color
        )

    def get_text_position(self, text, index) -> Rect:
        center = (self.center[0], self.center[1] + (index * 20))
        return text.get_rect(center=center)

    def handle_action(self) -> None:
        if self.active_index == 0:
            self.persist = {"level": 1, "reload": True}
            self.done = True
        if self.active_index == 1:
            self.persist = {"level": self.level_index, "reload": True}
            self.done = True
        elif self.active_index == 3:
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
                self.handle_action()

    def render(self, game_screen: Surface) -> None:
        for x in range(Config.WIDTH // Config.TITLE_SIZE):
            for y in range(Config.HEIGHT // Config.TITLE_SIZE):
                game_screen.blit(
                    self.bg_tile, (x * Config.TITLE_SIZE, y * Config.TITLE_SIZE)
                )
        dark = Surface((Config.WIDTH, Config.HEIGHT))
        dark.fill((0, 0, 0))
        dark.set_alpha(100)
        game_screen.blit(dark, (0, 0))
        game_screen.blit(
            self.font.render("Bobby Carrot", False, (0, 0, 0)), (75 + 1, 60 + 1)
        )
        game_screen.blit(
            self.font.render("Bobby Carrot", False, (255, 255, 255)), (75, 60)
        )
        for index, _ in enumerate(self.options):
            text_render = self.render_text(index, (0, 0, 0))
            pos = self.get_text_position(text_render, index)
            game_screen.blit(text_render, (pos[0] + 1, pos[1] + 1))
            text_render = self.render_text(index)
            game_screen.blit(text_render, pos)
