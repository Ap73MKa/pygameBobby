import pygame
from pygame.transform import scale

from .base import BaseState
from pygame.image import load
from src.scenes.stages.stage_utils import GameStage
from src.misc.path import PathManager
from ...misc.config import Config


class Menu(BaseState):
    def __init__(self):
        super().__init__()
        self.bg_tile = load(PathManager.get('assets/graphics/hud/grass.png')).convert()
        self.bg_tile = scale(self.bg_tile, (self.bg_tile.get_size()[0] * 3, self.bg_tile.get_size()[1] * 3))
        self.active_index = 0
        self.options = ["New game", "Choose level", "Credit", "Quit"]
        self.next_state = GameStage.GAMEPLAY

    def render_text(self, index):
        color = pygame.Color("red") if index == self.active_index else pygame.Color("white")
        return self.font.render(self.options[index], True, color)

    def get_text_position(self, text, index):
        center = (self.screen_rect.center[0], self.screen_rect.center[1] + (index * 50))
        return text.get_rect(center=center)

    def handle_action(self):
        if self.active_index == 0:
            self.done = True
        elif self.active_index == 3:
            self.quit = True

    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.quit = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                self.active_index = 1 if self.active_index <= 0 else 0
            elif event.key == pygame.K_DOWN:
                self.active_index = 0 if self.active_index >= 1 else 1
            elif event.key == pygame.K_RETURN:
                self.handle_action()

    def render(self):
        for x in range(Config.WIDTH // Config.TITLE_SIZE):
            for y in range(Config.HEIGHT // Config.TITLE_SIZE):
                self.surface.blit(self.bg_tile, (x * Config.TITLE_SIZE, y * Config.TITLE_SIZE))
        for index, option in enumerate(self.options):
            text_render = self.render_text(index)
            self.surface.blit(text_render, self.get_text_position(text_render, index))
