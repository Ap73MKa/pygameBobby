import pygame as pg

from pygame import Color
from .base import BaseState
from src.scene.stages.stage_utils import GameStage


class Pause(BaseState):
    def __init__(self) -> None:
        super().__init__()
        self.title = self.font.render("Game Over", True, Color("white"))
        self.title_rect = self.title.get_rect(center=self.screen_rect.center)
        text = "Press space to start again, or enter to go to the menu"
        self.instructions = self.font.render(text, True, Color("white"))
        instructions_center = (
            self.screen_rect.center[0],
            self.screen_rect.center[1] + 50,
        )
        self.instructions_rect = self.instructions.get_rect(center=instructions_center)

    def get_event(self, e) -> None:
        if e.type == pg.QUIT:
            self.quit = True
        elif e.type == pg.KEYUP:
            if e.key == pg.K_RETURN:
                self.next_state = GameStage.MENU
                self.done = True
            elif e.key == pg.K_SPACE:
                self.next_state = GameStage.GAMEPLAY
                self.done = True
            elif e.key == pg.K_ESCAPE:
                self.quit = True

    def render(self) -> None:
        self.surface.fill(Color("black"))
        self.surface.blit(self.title, self.title_rect)
        self.surface.blit(self.instructions, self.instructions_rect)
