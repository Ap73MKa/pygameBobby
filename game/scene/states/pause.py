import pygame as pg

from pygame import Color, Surface, Rect
from pygame.image import load

from game.misc import Config, PathManager, FontManager
from .state import State
from .stage_utils import GameState


class Pause(State):
    def __init__(self) -> None:
        super().__init__()
        self.font_manager = FontManager()
        self.bg_tile = load(PathManager.get("assets/graphics/hud/grass.png")).convert()
        self.center = (Config.WIDTH // 2, Config.HEIGHT // 2)
        self.active_index = 0
        self.options = ["Continue", "Reload level", "Back to menu", "Exit"]
        self.is_drawn_once = False
        self.persist = {}

    def startup(self, persistent: dict) -> None:
        self.active_index = 0
        self.is_drawn_once = False

    def handle_action(self) -> None:
        if self.active_index == 0:
            self.persist = {"reload": False}
            self.next_state = GameState.GAMEPLAY
            self.done = True
        if self.active_index == 1:
            self.next_state = GameState.GAMEPLAY
            self.persist = {"reload": True}
            self.done = True
        if self.active_index == 2:
            self.next_state = GameState.MENU
            self.done = True
        elif self.active_index == 3:
            self.quit = True

    def handle_option_index(self, move: int = 0):
        self.active_index += move
        if self.active_index < 0:
            self.active_index = len(self.options) - 1
        self.active_index %= len(self.options)

    def get_event(self, e) -> None:
        if e.type == pg.QUIT:
            self.quit = True
        elif e.type == pg.KEYUP:
            if e.key == pg.K_UP:
                self.handle_option_index(-1)
            elif e.key == pg.K_DOWN:
                self.handle_option_index(1)
            elif e.key == pg.K_RETURN:
                self.sound_manager.play_sound("menu_sound")
                self.handle_action()

    def render_menu_text(
        self, surface: Surface, index, y_pos: int, color: Color = (255, 255, 255)
    ):
        color = (100, 100, 100) if index != self.active_index else color
        pos = self.get_menu_text_position(surface, y_pos, self.options[index], index)
        self.font_manager.render_text(surface, self.options[index], pos, color)

    def get_menu_text_position(
        self, surface: Surface, y_pos: int, text: str, index: int
    ) -> tuple[int, int]:
        pos = self.font_manager.get_text_center_x_pos(surface, text, y_pos)
        return pos[0], pos[1] + (index * 20)

    def get_text_position(self, text, index) -> Rect:
        center = (self.center[0], self.center[1] - 30 + (index * 20))
        return text.get_rect(center=center)

    def render(self, game_screen: Surface) -> None:
        if not self.is_drawn_once:
            self.is_drawn_once = True
            dark = Surface((Config.WIDTH, Config.HEIGHT))
            dark.fill((0, 0, 0))
            dark.set_alpha(100)
            game_screen.blit(dark, (0, 0))

        for index in range(len(self.options)):
            self.render_menu_text(
                game_screen, index, game_screen.get_rect().centery - 30
            )
