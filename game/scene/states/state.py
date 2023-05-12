from pygame import Color, Surface
from pygame.font import Font
from pygame.display import get_surface
from pygame.event import Event

from .stage_utils import GameState
from game.misc import PathManager


class State:
    def __init__(self) -> None:
        self.done = self.quit = False
        self.next_state: GameState | None = None
        self.screen_rect = get_surface().get_rect()
        self.font = Font(PathManager.get("assets/graphics/hud/font.ttf"), 10)
        self.persist: dict = {}

    def startup(self, persistent: dict) -> None:
        self.persist = persistent

    def render_text(self, game_screen: Surface, text: str, position: tuple[int, int],
                    color: Color = (255, 255, 255), shadow: bool = True) -> None:
        if shadow:
            text_shadow = self.font.render(text, False, (0, 0, 0))
            game_screen.blit(text_shadow, (position[0] + 1, position[1] + 1))
        text_surface = self.font.render(text, False, color)
        game_screen.blit(text_surface, position)

    @staticmethod
    def get_screen_center(surface: Surface) -> tuple[int, int]:
        return surface.get_rect().center

    def get_event(self, e: Event) -> None:
        pass

    def update(self, delta: float) -> None:
        pass

    def render(self, game_surface: Surface) -> None:
        pass
