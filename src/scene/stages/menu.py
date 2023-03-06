from pygame import Color, QUIT, KEYUP, K_UP, K_DOWN, K_RIGHT, K_LEFT, K_RETURN, Surface, SurfaceType, Rect
from pygame.font import Font
from pygame.transform import scale
from pygame.image import load

from src.scene.stages.base import BaseState
from src.scene.stages.stage_utils import GameStage
from src.misc.path import PathManager
from src.misc.config import Config


class Menu(BaseState):
    def __init__(self) -> None:
        super().__init__()
        self.level_index = 1
        self.bg_tile = load(PathManager.get("assets/graphics/hud/grass.png")).convert()
        self.bg_tile = scale(
            self.bg_tile,
            (self.bg_tile.get_size()[0] * 3, self.bg_tile.get_size()[1] * 3),
        )
        self.font = Font(PathManager.get("assets/graphics/hud/font.ttf"), 28)
        self.active_index = 0
        self.options = [
            "New game",
            f"Choose level <{self.level_index}>",
            "Credit",
            "Quit",
        ]
        self.next_state = GameStage.GAMEPLAY

    def render_text(self, index, custom_color=None) -> Surface | SurfaceType:
        color = (
            Color((255, 255, 255))
            if index == self.active_index
            else Color((100, 100, 100))
        )
        return self.font.render(
            self.options[index], True, custom_color if custom_color else color
        )

    def get_text_position(self, text, index) -> Rect:
        center = (self.screen_rect.center[0], self.screen_rect.center[1] + (index * 50))
        return text.get_rect(center=center)

    def handle_action(self) -> None:
        if self.active_index == 0:
            self.done = True
        if self.active_index == 1:
            self.done = True
        elif self.active_index == 3:
            self.quit = True

    def get_event(self, e) -> None:
        if e.type == QUIT:
            self.quit = True
        elif e.type == KEYUP:
            if e.key == K_UP:
                self.active_index -= 1
                if self.active_index < 0:
                    self.active_index = len(self.options) - 1
            elif e.key == K_DOWN:
                self.active_index += 1
                self.active_index %= len(self.options)
            elif e.key == K_RIGHT and self.active_index == 1:
                self.level_index += 1
                if self.level_index > Config.MAX_LEVEL:
                    self.level_index = 1
                self.options[1] = f"Choose level <{self.level_index}>"
            elif e.key == K_LEFT and self.active_index == 1:
                self.level_index -= 1
                if self.level_index == 0:
                    self.level_index = Config.MAX_LEVEL
                self.options[1] = f"Choose level <{self.level_index}>"
            elif e.key == K_RETURN:
                self.handle_action()

    def render(self) -> None:
        for x in range(Config.WIDTH // Config.TITLE_SIZE):
            for y in range(Config.HEIGHT // Config.TITLE_SIZE):
                self.surface.blit(
                    self.bg_tile, (x * Config.TITLE_SIZE, y * Config.TITLE_SIZE)
                )
        dark = Surface((Config.WIDTH, Config.HEIGHT))
        dark.fill((0, 0, 0))
        dark.set_alpha(100)
        self.surface.blit(dark, (0, 0))
        self.surface.blit(
            self.font.render("Bobby Carrot", True, (0, 0, 0)), (240 + 3, 180 + 3)
        )
        self.surface.blit(
            self.font.render("Bobby Carrot", True, (255, 255, 255)), (240, 180)
        )
        for index, _ in enumerate(self.options):
            text_render = self.render_text(index, (0, 0, 0))
            pos = self.get_text_position(text_render, index)
            self.surface.blit(text_render, (pos[0] + 3, pos[1] + 3))
            text_render = self.render_text(index)
            self.surface.blit(text_render, pos)
