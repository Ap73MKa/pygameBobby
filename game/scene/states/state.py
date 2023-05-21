from pygame import Surface
from pygame.event import Event

from game.misc import FontManager, SoundManager
from . import GameState


class State:
    def __init__(self):
        self.sound_manager = SoundManager()
        self.font_manager = FontManager()
        self.next_state: GameState | None = None
        self.done = self.quit = False
        self.persist: dict = {}

    def startup(self, persistent: dict) -> None:
        self.persist = persistent

    def handle_event(self, event: Event) -> None:
        pass

    def update(self, delta: float) -> None:
        pass

    def render(self, game_surface: Surface) -> None:
        pass
