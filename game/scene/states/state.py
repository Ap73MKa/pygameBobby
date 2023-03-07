from pygame import Surface
from pygame.font import Font
from pygame.display import get_surface
from pygame.event import Event

from .stage_utils import GameState


class State:
    def __init__(self) -> None:
        self.done = self.quit = False
        self.next_state: GameState | None = None
        self.screen_rect = get_surface().get_rect()
        self.persist: dict = {}
        self.font = Font(None, 24)

    def startup(self, persistent: dict) -> None:
        self.persist = persistent

    def get_event(self, e: Event) -> None:
        pass

    def update(self, delta: float) -> None:
        pass

    def render(self, game_surface: Surface) -> None:
        pass
