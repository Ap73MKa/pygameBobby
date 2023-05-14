import pygame as pg
from pygame.surface import Surface
from pygame.font import Font

from game.misc import PathManager, Config, get_text_center_x_pos
from .stage_utils import GameState
from .state import State


class LevelTransition(State):
    def __init__(self) -> None:
        super().__init__()
        self.font = Font(PathManager.get("assets/graphics/hud/font.ttf"), 10)
        self.next_state = GameState.GAMEPLAY
        self.is_drawn = False
        self.level = 1
        self.time = "00:00"
        self.steps = 0
        self.persist = {}
        self.stats_text = []

    def startup(self, persistent: dict) -> None:
        self.is_drawn = False
        self.level = persistent.get("level", 1)
        self.time = persistent.get("time", "00:00")
        self.steps = persistent.get("steps", 0)
        self.stats_text = [
            f"Time: {self.time}",
            f"Steps: {self.steps}",
            "Press any key to continue",
        ]

    def get_event(self, e) -> None:
        if e.type == pg.QUIT:
            self.quit = True
        elif e.type == pg.KEYUP:
            if self.level > Config.MAX_LEVEL:
                self.next_state = GameState.MENU
            else:
                self.persist = {"level": self.level}
            self.done = True

    def blit_text_center(self, surface: Surface, text: str, y_pos: int) -> None:
        pos = get_text_center_x_pos(surface, self.font, text, y_pos)
        self.render_text(surface, text, pos)

    def render_dark_overlay(self, surface: Surface):
        dark = Surface((Config.WIDTH, Config.HEIGHT))
        dark.fill((0, 0, 0))
        dark.set_alpha(100)
        surface.blit(dark, (0, 0))

    def render(self, game_screen: Surface) -> None:
        if not self.is_drawn:
            self.is_drawn = True
            self.render_dark_overlay(game_screen)
            self.blit_text_center(game_screen, "SUCCESS", 50)
            for index, text in enumerate(self.stats_text):
                self.blit_text_center(
                    game_screen,
                    text,
                    self.get_screen_center(game_screen)[1] - 10 + (index * 20),
                )
