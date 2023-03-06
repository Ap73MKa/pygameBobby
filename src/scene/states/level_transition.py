import pygame as pg
from pygame import Surface
from pygame.font import Font

from . import GameState
from .state import State
from src.misc import PathManager, Config


class LevelTransition(State):
    def __init__(self) -> None:
        super().__init__()
        self.font = Font(PathManager.get("assets/graphics/hud/font.ttf"), 10)
        self.next_state = GameState.GAMEPLAY
        self.is_drawn_once = False
        self.level = 1
        self.time = "00:00"
        self.steps = 0
        self.persist = {}

    def startup(self, persistent: dict) -> None:
        self.is_drawn_once = False
        for key, item in persistent.items():
            if key == "level":
                self.level = item
            elif key == "time":
                self.time = item
            elif key == "steps":
                self.steps = item

    def get_event(self, e) -> None:
        if e.type == pg.QUIT:
            self.quit = True
        elif e.type == pg.KEYUP:
            if self.level >= Config.MAX_LEVEL:
                self.next_state = GameState.MENU
            else:
                self.persist = {"level": self.level}
            self.done = True

    def render(self, game_screen: Surface) -> None:
        if not self.is_drawn_once:
            self.is_drawn_once = True
            dark = Surface((Config.WIDTH, Config.HEIGHT))
            dark.fill((0, 0, 0))
            dark.set_alpha(100)
            game_screen.blit(dark, (0, 0))

        game_screen.blit(
            self.font.render("SUCCESS", False, (0, 0, 0)), (80 + 1, 60 + 1)
        )
        game_screen.blit(self.font.render("SUCCESS", False, (255, 255, 255)), (80, 60))

        game_screen.blit(
            self.font.render(f"Time: {self.time}", False, (0, 0, 0)), (80 + 1, 80 + 1)
        )
        game_screen.blit(
            self.font.render(f"Time: {self.time}", False, (255, 255, 255)), (80, 80)
        )

        game_screen.blit(
            self.font.render(f"Steps: {self.steps}", False, (0, 0, 0)),
            (80 + 1, 100 + 1),
        )
        game_screen.blit(
            self.font.render(f"Steps: {self.steps}", False, (255, 255, 255)), (80, 100)
        )

        game_screen.blit(
            self.font.render("Press any key to continue", False, (0, 0, 0)),
            (40 + 1, 120 + 1),
        )
        game_screen.blit(
            self.font.render("Press any key to continue", False, (255, 255, 255)),
            (40, 120),
        )
