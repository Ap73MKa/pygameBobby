import pygame as pg

from pygame import Color, Surface, SurfaceType, Rect
from pygame.font import Font
from pygame.image import load

from game.misc import Config, PathManager
from .state import State
from .stage_utils import GameState


class Pause(State):
    def __init__(self) -> None:
        super().__init__()
        self.bg_tile = load(PathManager.get("assets/graphics/hud/grass.png")).convert()
        self.font = Font(PathManager.get("assets/graphics/hud/font.ttf"), 10)
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
                self.handle_action()

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

    def render(self, game_screen: Surface) -> None:
        if not self.is_drawn_once:
            self.is_drawn_once = True
            dark = Surface((Config.WIDTH, Config.HEIGHT))
            dark.fill((0, 0, 0))
            dark.set_alpha(100)
            game_screen.blit(dark, (0, 0))

        # Options
        for index, _ in enumerate(self.options):
            text_render = self.render_text(index, (0, 0, 0))
            pos = self.get_text_position(text_render, index)
            game_screen.blit(text_render, (pos[0] + 1, pos[1] + 1))
            text_render = self.render_text(index)
            game_screen.blit(text_render, pos)
