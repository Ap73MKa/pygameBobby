from pygame import Surface
from pygame.display import get_surface
from pygame.event import Event

from .stage_utils import GameState
from ..sound_manager import SoundManager


class State:
    def __init__(self) -> None:
        self.sound_manager = SoundManager()
        self.done = self.quit = False
        self.next_state: GameState | None = None
        self.screen_rect = get_surface().get_rect()
        self.persist: dict = {}

    def startup(self, persistent: dict) -> None:
        self.persist = persistent

    @staticmethod
    def get_screen_center(surface: Surface) -> tuple[int, int]:
        return surface.get_rect().center

    def get_event(self, e: Event) -> None:
        pass

    def update(self, delta: float) -> None:
        pass

    def render(self, game_surface: Surface) -> None:
        pass
