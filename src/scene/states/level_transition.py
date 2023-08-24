import pygame as pg
from pygame.event import Event
from pygame.surface import Surface

from src.config import configure
from src.scene.states.stage_utils import GameState
from src.scene.states.state import State


class LevelTransition(State):
    def __init__(self) -> None:
        super().__init__()
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

    def handle_event(self, event: Event) -> None:
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.KEYUP:
            if self.level > configure.MAX_LEVEL:
                self.next_state = GameState.MENU
            else:
                self.persist = {"level": self.level}
            self.done = True

    def blit_text_center(self, surface: Surface, text: str, y_pos: int) -> None:
        pos = self.font_manager.get_text_center_x_pos(surface, text, y_pos)
        self.font_manager.render_text(surface, text, pos)

    def render_dark_overlay(self, surface: Surface):
        dark = Surface((configure.WIDTH, configure.HEIGHT))
        dark.fill((0, 0, 0))
        dark.set_alpha(100)
        surface.blit(dark, (0, 0))

    def render(self, game_surface: Surface) -> None:
        if not self.is_drawn:
            self.is_drawn = True
            self.render_dark_overlay(game_surface)
            self.blit_text_center(game_surface, "SUCCESS", 50)
            for index, text in enumerate(self.stats_text):
                self.blit_text_center(
                    game_surface,
                    text,
                    82 + (index * 20),
                )
